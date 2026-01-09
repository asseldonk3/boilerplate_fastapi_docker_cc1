#!/usr/bin/env python3
"""
SAFE Framework - Search-Augmented Factuality Evaluation

Implements the SAFE framework for fact-checking LLM outputs using
external search verification. Based on Google DeepMind research.

This script provides the core logic for fact-checking. When used within
Claude Code, it leverages the mcp__gemini-cli__gemini_google_web_search tool for evidence retrieval.

Usage (standalone):
    python safe_factcheck.py --input "text to verify" --query "original user query"

Usage (as module):
    from safe_factcheck import SAFEEvaluator
    evaluator = SAFEEvaluator()
    result = evaluator.evaluate(text, original_query)
"""

import argparse
import json
import re
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class AtomicFact:
    """A single verifiable claim extracted from text."""
    id: str
    claim: str
    relevant: bool = True
    verdict: Optional[str] = None  # SUPPORTED, NOT_SUPPORTED, INSUFFICIENT
    confidence: str = "MEDIUM"
    reasoning: str = ""
    evidence: list = field(default_factory=list)
    search_queries: list = field(default_factory=list)


@dataclass
class SAFEResult:
    """Result of a SAFE evaluation."""
    fact_score: float
    total_facts: int
    supported: int
    not_supported: int
    insufficient: int
    irrelevant: int
    facts: list[AtomicFact]
    summary: str

    def to_dict(self) -> dict:
        return {
            "fact_score": self.fact_score,
            "total_facts": self.total_facts,
            "supported": self.supported,
            "not_supported": self.not_supported,
            "insufficient": self.insufficient,
            "irrelevant": self.irrelevant,
            "summary": self.summary,
            "facts": [
                {
                    "id": f.id,
                    "claim": f.claim,
                    "relevant": f.relevant,
                    "verdict": f.verdict,
                    "confidence": f.confidence,
                    "reasoning": f.reasoning,
                    "evidence_count": len(f.evidence)
                }
                for f in self.facts
            ]
        }

    def __str__(self) -> str:
        lines = [
            "=== SAFE Evaluation Result ===",
            f"FactScore: {self.fact_score:.1%}",
            f"Total Facts: {self.total_facts}",
            f"  - Supported: {self.supported}",
            f"  - Not Supported: {self.not_supported}",
            f"  - Insufficient Evidence: {self.insufficient}",
            f"  - Irrelevant (filtered): {self.irrelevant}",
            "",
            "Detailed Results:"
        ]

        for fact in self.facts:
            if fact.relevant:
                icon = {"SUPPORTED": "✓", "NOT_SUPPORTED": "✗", "INSUFFICIENT": "?"}.get(fact.verdict, "?")
                lines.append(f"  {icon} [{fact.verdict}] {fact.claim}")
                if fact.reasoning:
                    lines.append(f"      Reason: {fact.reasoning}")

        lines.append("")
        lines.append(f"Summary: {self.summary}")

        return "\n".join(lines)


class SAFEEvaluator:
    """
    SAFE Framework implementation for fact-checking.

    This class provides the logic for decomposition, query generation,
    and adjudication. Evidence retrieval is handled externally (via
    MCP web search or custom search API).
    """

    # Prompts for each step
    DECOMPOSITION_PROMPT = """You are a fact extraction expert. Break down the following text into
individual atomic facts. Each atomic fact should:
- Contain exactly ONE verifiable claim
- Be self-contained (understandable without context)
- Be as specific as possible
- Include any numbers, dates, names, or specific details

Text to decompose:
{text}

Output format - one fact per line:
1. [first atomic fact]
2. [second atomic fact]
..."""

    RELEVANCE_PROMPT = """Given the user's original query and the following atomic facts,
determine which facts are RELEVANT to answering the query.

Original query: {query}

Atomic facts:
{facts}

For each fact, output ONLY the number and verdict:
1: RELEVANT
2: IRRELEVANT
3: RELEVANT
..."""

    QUERY_GEN_PROMPT = """Generate 2-3 search queries to verify the following claim.
The queries should:
- Be specific enough to find relevant information
- Target authoritative sources (Wikipedia, official sites, news)
- Use different phrasings for better coverage

Claim to verify: {claim}

Output queries, one per line (no numbering):"""

    ADJUDICATION_PROMPT = """You are a fact-checker. Compare the following claim against the
provided evidence and determine if it is supported.

CLAIM: {claim}

EVIDENCE:
{evidence}

Based ONLY on the evidence provided, determine:

Output format:
VERDICT: [SUPPORTED | NOT_SUPPORTED | INSUFFICIENT]
CONFIDENCE: [HIGH | MEDIUM | LOW]
REASONING: [One sentence explaining your verdict]"""

    def __init__(self, model_callable=None):
        """
        Initialize the SAFE evaluator.

        Args:
            model_callable: Function to call LLM. Should accept (prompt: str) -> str
                           If None, prompts will be returned for external execution.
        """
        self.model_callable = model_callable

    def decompose(self, text: str) -> list[AtomicFact]:
        """
        Step 1: Decompose text into atomic facts.

        Args:
            text: The text to decompose

        Returns:
            List of AtomicFact objects
        """
        prompt = self.DECOMPOSITION_PROMPT.format(text=text)

        if self.model_callable:
            response = self.model_callable(prompt)
            return self._parse_decomposition(response)
        else:
            # Return prompt for external execution
            return prompt

    def _parse_decomposition(self, response: str) -> list[AtomicFact]:
        """Parse decomposition response into AtomicFact objects."""
        facts = []
        lines = response.strip().split("\n")

        for i, line in enumerate(lines):
            # Remove numbering (e.g., "1. ", "1) ", etc.)
            cleaned = re.sub(r"^\d+[\.\)]\s*", "", line.strip())
            if cleaned:
                facts.append(AtomicFact(
                    id=f"fact_{i+1:03d}",
                    claim=cleaned
                ))

        return facts

    def filter_relevant(self, facts: list[AtomicFact], query: str) -> list[AtomicFact]:
        """
        Step 2: Filter facts by relevance to original query.

        Args:
            facts: List of atomic facts
            query: Original user query

        Returns:
            Updated list with relevance flags set
        """
        facts_text = "\n".join(f"{i+1}. {f.claim}" for i, f in enumerate(facts))
        prompt = self.RELEVANCE_PROMPT.format(query=query, facts=facts_text)

        if self.model_callable:
            response = self.model_callable(prompt)
            return self._parse_relevance(facts, response)
        else:
            return prompt

    def _parse_relevance(self, facts: list[AtomicFact], response: str) -> list[AtomicFact]:
        """Parse relevance response and update facts."""
        for line in response.strip().split("\n"):
            match = re.match(r"(\d+):\s*(RELEVANT|IRRELEVANT)", line.strip(), re.IGNORECASE)
            if match:
                idx = int(match.group(1)) - 1
                is_relevant = match.group(2).upper() == "RELEVANT"
                if 0 <= idx < len(facts):
                    facts[idx].relevant = is_relevant

        return facts

    def generate_queries(self, fact: AtomicFact) -> list[str]:
        """
        Step 3: Generate search queries for a fact.

        Args:
            fact: The atomic fact to generate queries for

        Returns:
            List of search query strings
        """
        prompt = self.QUERY_GEN_PROMPT.format(claim=fact.claim)

        if self.model_callable:
            response = self.model_callable(prompt)
            queries = [q.strip() for q in response.strip().split("\n") if q.strip()]
            fact.search_queries = queries
            return queries
        else:
            return prompt

    def adjudicate(self, fact: AtomicFact, evidence: list[str]) -> AtomicFact:
        """
        Step 5: Adjudicate a fact against evidence.

        Args:
            fact: The atomic fact to adjudicate
            evidence: List of evidence snippets from search

        Returns:
            Updated AtomicFact with verdict
        """
        if not evidence:
            fact.verdict = "INSUFFICIENT"
            fact.confidence = "LOW"
            fact.reasoning = "No evidence retrieved"
            return fact

        evidence_text = "\n".join(f"- {e}" for e in evidence[:5])  # Limit to 5 snippets
        prompt = self.ADJUDICATION_PROMPT.format(claim=fact.claim, evidence=evidence_text)

        if self.model_callable:
            response = self.model_callable(prompt)
            return self._parse_adjudication(fact, response)
        else:
            return prompt

    def _parse_adjudication(self, fact: AtomicFact, response: str) -> AtomicFact:
        """Parse adjudication response and update fact."""
        for line in response.strip().split("\n"):
            line = line.strip()
            if line.startswith("VERDICT:"):
                verdict = line.replace("VERDICT:", "").strip().upper()
                if verdict in ["SUPPORTED", "NOT_SUPPORTED", "INSUFFICIENT"]:
                    fact.verdict = verdict
            elif line.startswith("CONFIDENCE:"):
                conf = line.replace("CONFIDENCE:", "").strip().upper()
                if conf in ["HIGH", "MEDIUM", "LOW"]:
                    fact.confidence = conf
            elif line.startswith("REASONING:"):
                fact.reasoning = line.replace("REASONING:", "").strip()

        return fact

    def calculate_score(self, facts: list[AtomicFact]) -> SAFEResult:
        """
        Calculate FactScore from evaluated facts.

        Args:
            facts: List of adjudicated AtomicFact objects

        Returns:
            SAFEResult with scores and summary
        """
        relevant_facts = [f for f in facts if f.relevant]

        supported = sum(1 for f in relevant_facts if f.verdict == "SUPPORTED")
        not_supported = sum(1 for f in relevant_facts if f.verdict == "NOT_SUPPORTED")
        insufficient = sum(1 for f in relevant_facts if f.verdict == "INSUFFICIENT")
        irrelevant = sum(1 for f in facts if not f.relevant)

        total_relevant = len(relevant_facts)
        fact_score = supported / total_relevant if total_relevant > 0 else 0

        # Generate summary
        if fact_score >= 0.9:
            summary = "Highly accurate - nearly all claims supported by evidence"
        elif fact_score >= 0.75:
            summary = "Generally accurate - most claims supported"
        elif fact_score >= 0.5:
            summary = "Mixed accuracy - significant unsupported claims"
        else:
            summary = "Low accuracy - majority of claims not supported"

        if not_supported > 0:
            unsupported_claims = [f.claim for f in relevant_facts if f.verdict == "NOT_SUPPORTED"]
            summary += f". Unsupported claims: {'; '.join(unsupported_claims[:3])}"

        return SAFEResult(
            fact_score=fact_score,
            total_facts=len(facts),
            supported=supported,
            not_supported=not_supported,
            insufficient=insufficient,
            irrelevant=irrelevant,
            facts=facts,
            summary=summary
        )


def main():
    """CLI entry point for standalone usage."""
    parser = argparse.ArgumentParser(
        description="SAFE Framework - Fact-check text using search verification"
    )
    parser.add_argument(
        "--input",
        required=True,
        help="Text to fact-check (or path to file)"
    )
    parser.add_argument(
        "--query",
        default="",
        help="Original user query (for relevance filtering)"
    )
    parser.add_argument(
        "--output",
        help="Output file for results (JSON)"
    )
    parser.add_argument(
        "--prompts-only",
        action="store_true",
        help="Only output prompts (for manual/external execution)"
    )

    args = parser.parse_args()

    # Load input text
    if args.input.endswith(".txt") or args.input.endswith(".md"):
        with open(args.input) as f:
            text = f.read()
    else:
        text = args.input

    evaluator = SAFEEvaluator()

    if args.prompts_only:
        # Output prompts for external execution
        print("=== STEP 1: Decomposition Prompt ===")
        print(evaluator.decompose(text))
        print("\n=== Next steps require decomposition results ===")
        print("Run decomposition, then use the results for Steps 2-5")
    else:
        print("Note: Full evaluation requires an LLM and search API.")
        print("Use --prompts-only to get prompts for external execution.")
        print("Or integrate this module with your LLM pipeline.")

    if args.output:
        print(f"\nResults would be saved to {args.output}")


if __name__ == "__main__":
    main()
