#!/usr/bin/env python3
"""
LLM Judge - Evaluation Script

Implements LLM-as-a-Judge methodology with bias mitigation.
Supports pointwise, pairwise, and G-Eval evaluation modes.

Usage:
    python evaluate.py --mode pointwise --input output.json --rubric rubric.yaml
    python evaluate.py --mode pairwise --input-a a.json --input-b b.json
    python evaluate.py --mode g-eval --input output.json --dimensions accuracy,clarity
"""

import argparse
import json
import math
import os
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

import yaml

# Optional: for API calls
try:
    import anthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False

try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False


@dataclass
class EvaluationResult:
    """Result of an evaluation."""
    mode: str
    score: Optional[float]
    scores_by_dimension: Optional[dict]
    reasoning: str
    winner: Optional[str] = None  # For pairwise
    consistency: Optional[str] = None  # For pairwise
    confidence: str = "MEDIUM"
    raw_response: str = ""
    metadata: dict = None

    def to_dict(self) -> dict:
        return {
            "mode": self.mode,
            "score": self.score,
            "scores_by_dimension": self.scores_by_dimension,
            "reasoning": self.reasoning,
            "winner": self.winner,
            "consistency": self.consistency,
            "confidence": self.confidence,
            "metadata": self.metadata or {}
        }

    def __str__(self) -> str:
        lines = [f"=== {self.mode.upper()} Evaluation Result ==="]
        if self.score is not None:
            lines.append(f"Score: {self.score:.2f}")
        if self.winner:
            lines.append(f"Winner: {self.winner}")
        if self.consistency:
            lines.append(f"Consistency: {self.consistency}")
        lines.append(f"Confidence: {self.confidence}")
        if self.scores_by_dimension:
            lines.append("Dimension Scores:")
            for dim, score in self.scores_by_dimension.items():
                lines.append(f"  - {dim}: {score:.2f}")
        lines.append(f"\nReasoning:\n{self.reasoning}")
        return "\n".join(lines)


class LLMJudge:
    """LLM-as-a-Judge evaluator with bias mitigation."""

    SKILL_DIR = Path(__file__).parent.parent

    def __init__(
        self,
        model: str = "claude-sonnet-4-20250514",
        provider: str = "anthropic",
        temperature: float = 0.0
    ):
        self.model = model
        self.provider = provider
        self.temperature = temperature
        self._client = None

    @property
    def client(self):
        """Lazy initialization of API client."""
        if self._client is None:
            if self.provider == "anthropic":
                if not ANTHROPIC_AVAILABLE:
                    raise ImportError("anthropic package not installed. Run: pip install anthropic")
                self._client = anthropic.Anthropic()
            elif self.provider == "openai":
                if not OPENAI_AVAILABLE:
                    raise ImportError("openai package not installed. Run: pip install openai")
                self._client = openai.OpenAI()
            else:
                raise ValueError(f"Unknown provider: {self.provider}")
        return self._client

    def _call_model(self, prompt: str, max_tokens: int = 2000) -> str:
        """Call the LLM and return response text."""
        if self.provider == "anthropic":
            response = self.client.messages.create(
                model=self.model,
                max_tokens=max_tokens,
                temperature=self.temperature,
                messages=[{"role": "user", "content": prompt}]
            )
            return response.content[0].text
        elif self.provider == "openai":
            response = self.client.chat.completions.create(
                model=self.model,
                max_tokens=max_tokens,
                temperature=self.temperature,
                messages=[{"role": "user", "content": prompt}]
            )
            return response.choices[0].message.content
        else:
            raise ValueError(f"Unknown provider: {self.provider}")

    def load_rubric(self, rubric_path: str) -> dict:
        """Load a rubric from YAML file."""
        path = Path(rubric_path)
        if not path.is_absolute():
            # Check in skill's rubrics directory
            skill_rubric = self.SKILL_DIR / "rubrics" / rubric_path
            if skill_rubric.exists():
                path = skill_rubric

        with open(path) as f:
            return yaml.safe_load(f)

    def pointwise_evaluate(
        self,
        prompt: str,
        response: str,
        rubric: dict,
        reference: Optional[str] = None
    ) -> EvaluationResult:
        """
        Pointwise evaluation with thinking protocol.

        Args:
            prompt: The original prompt/instruction
            response: The response to evaluate
            rubric: Rubric dictionary with dimensions and scales
            reference: Optional reference answer for anchoring
        """
        # Build evaluation prompt with thinking protocol
        rubric_text = self._format_rubric(rubric)
        reference_section = ""
        if reference:
            reference_section = f"""
## Reference Answer (use as quality anchor)
{reference}

Note: Compare the candidate's information coverage and accuracy to the reference.
A concise response that covers the same information is BETTER than a verbose one.
"""

        eval_prompt = f"""You are an expert evaluator. Before judging, think step-by-step.

## Rubric
{rubric_text}

## Original Prompt
{prompt}
{reference_section}
## Response to Evaluate
{response}

## Instructions
Evaluate using the J1 "Thinking Judge" protocol:

1. **Analyze User Intent**: What is being asked? Identify implicit constraints.
2. **Fact-Check**: Verify key claims in the response.
3. **Critique**: List specific strengths and weaknesses for each dimension.
4. **Scores**: Assign a score (1-5) for each dimension based on the rubric.
5. **Overall**: Calculate weighted average if weights provided.

IMPORTANT: Penalize unnecessary verbosity. Prefer concise, accurate responses.

Output format:
ANALYSIS:
[Your detailed step-by-step analysis]

DIMENSION_SCORES:
[dimension_name]: [score]
[dimension_name]: [score]
...

OVERALL_SCORE: [weighted average or simple average]

REASONING: [1-2 sentence summary justification]
"""

        raw_response = self._call_model(eval_prompt)
        return self._parse_pointwise_response(raw_response, rubric)

    def pairwise_evaluate(
        self,
        prompt: str,
        response_a: str,
        response_b: str,
        criteria: list[str],
        use_swap_and_pool: bool = True
    ) -> EvaluationResult:
        """
        Pairwise evaluation with position bias mitigation.

        Args:
            prompt: The original prompt
            response_a: First response
            response_b: Second response
            criteria: List of evaluation criteria
            use_swap_and_pool: Whether to run both orderings (recommended)
        """
        criteria_text = "\n".join(f"- {c}" for c in criteria)

        def make_comparison_prompt(first: str, second: str) -> str:
            return f"""Compare the following two responses.

## Original Prompt
{prompt}

## Response A
{first}

## Response B
{second}

## Evaluation Criteria
{criteria_text}

## Instructions
Using the J1 "Thinking Judge" protocol:

1. **Analyze** both responses against each criterion
2. **Compare** directly: which better satisfies each criterion?
3. **Identify** key differentiators
4. **Verdict**: Which response is better overall?

Output format:
ANALYSIS:
[Detailed comparative analysis]

VERDICT: [A_BETTER | B_BETTER | TIE]
CONFIDENCE: [HIGH | MEDIUM | LOW]
REASONING: [Brief justification]
"""

        # Forward pass
        forward_prompt = make_comparison_prompt(response_a, response_b)
        forward_raw = self._call_model(forward_prompt)
        forward_result = self._parse_pairwise_response(forward_raw)

        if not use_swap_and_pool:
            return EvaluationResult(
                mode="pairwise",
                score=None,
                scores_by_dimension=None,
                reasoning=forward_result["reasoning"],
                winner=forward_result["verdict"],
                confidence=forward_result["confidence"],
                raw_response=forward_raw
            )

        # Reverse pass (swap A and B)
        reverse_prompt = make_comparison_prompt(response_b, response_a)
        reverse_raw = self._call_model(reverse_prompt)
        reverse_result = self._parse_pairwise_response(reverse_raw)

        # Pool results
        pooled = self._pool_pairwise(forward_result, reverse_result)

        return EvaluationResult(
            mode="pairwise",
            score=None,
            scores_by_dimension=None,
            reasoning=f"Forward: {forward_result['reasoning']}\nReverse: {reverse_result['reasoning']}",
            winner=pooled["winner"],
            consistency=pooled["consistency"],
            confidence=pooled["confidence"],
            metadata={
                "forward_verdict": forward_result["verdict"],
                "reverse_verdict": reverse_result["verdict"],
                "position_bias_detected": pooled.get("position_bias_detected", False)
            },
            raw_response=f"FORWARD:\n{forward_raw}\n\nREVERSE:\n{reverse_raw}"
        )

    def g_eval(
        self,
        prompt: str,
        response: str,
        dimensions: list[str],
        rubric: Optional[dict] = None
    ) -> EvaluationResult:
        """
        G-Eval: Probabilistic continuous scoring.

        Note: Full G-Eval requires logprobs access. This implementation
        uses Chain-of-Thought with explicit probability estimation.

        Args:
            prompt: Original prompt
            response: Response to evaluate
            dimensions: List of dimensions to evaluate (e.g., ["coherence", "factuality"])
            rubric: Optional rubric with dimension definitions
        """
        results = {}

        for dimension in dimensions:
            dimension_rubric = ""
            if rubric and "dimensions" in rubric and dimension in rubric["dimensions"]:
                dim_info = rubric["dimensions"][dimension]
                dimension_rubric = f"""
Rubric for {dimension}:
{yaml.dump(dim_info.get('scale', {}), default_flow_style=False)}
"""

            eval_prompt = f"""Evaluate the following response for {dimension.upper()}.

{dimension_rubric}

## Original Prompt
{prompt}

## Response to Evaluate
{response}

## Instructions
1. Provide detailed analysis of the response's {dimension}
2. Consider specific examples from the response
3. Estimate your confidence in each possible score (1-5)
4. Assign final score

Output format:
ANALYSIS:
[Detailed analysis of {dimension}]

SCORE_PROBABILITIES:
1: [probability 0-100%]
2: [probability 0-100%]
3: [probability 0-100%]
4: [probability 0-100%]
5: [probability 0-100%]

EXPECTED_SCORE: [calculated as sum of score * probability]

REASONING: [Brief justification]
"""

            raw_response = self._call_model(eval_prompt)
            results[dimension] = self._parse_g_eval_response(raw_response, dimension)

        # Calculate aggregate
        if results:
            aggregate = sum(r["expected_score"] for r in results.values()) / len(results)
        else:
            aggregate = 0

        return EvaluationResult(
            mode="g-eval",
            score=aggregate,
            scores_by_dimension={dim: r["expected_score"] for dim, r in results.items()},
            reasoning="\n\n".join(
                f"**{dim}** (Score: {r['expected_score']:.2f}):\n{r['reasoning']}"
                for dim, r in results.items()
            ),
            confidence=self._aggregate_confidence(results),
            metadata={"dimension_details": results}
        )

    def _format_rubric(self, rubric: dict) -> str:
        """Format rubric for prompt inclusion."""
        lines = []
        if "dimensions" in rubric:
            for dim_name, dim_info in rubric["dimensions"].items():
                weight = dim_info.get("weight", 1.0)
                desc = dim_info.get("description", "")
                lines.append(f"\n### {dim_name} (weight: {weight})")
                lines.append(f"{desc}")
                if "scale" in dim_info:
                    lines.append("Scale:")
                    for score, meaning in dim_info["scale"].items():
                        lines.append(f"  {score}: {meaning}")
        return "\n".join(lines)

    def _parse_pointwise_response(self, raw: str, rubric: dict) -> EvaluationResult:
        """Parse pointwise evaluation response."""
        lines = raw.split("\n")
        scores = {}
        overall = None
        reasoning = ""
        analysis = ""

        current_section = None
        for line in lines:
            line_stripped = line.strip()

            if line_stripped.startswith("ANALYSIS:"):
                current_section = "analysis"
                continue
            elif line_stripped.startswith("DIMENSION_SCORES:"):
                current_section = "scores"
                continue
            elif line_stripped.startswith("OVERALL_SCORE:"):
                try:
                    overall = float(line_stripped.split(":")[-1].strip())
                except ValueError:
                    pass
                current_section = None
                continue
            elif line_stripped.startswith("REASONING:"):
                current_section = "reasoning"
                reasoning = line_stripped.replace("REASONING:", "").strip()
                continue

            if current_section == "analysis":
                analysis += line + "\n"
            elif current_section == "scores":
                if ":" in line_stripped:
                    parts = line_stripped.split(":")
                    dim = parts[0].strip().lower()
                    try:
                        score = float(parts[1].strip())
                        scores[dim] = score
                    except ValueError:
                        pass
            elif current_section == "reasoning":
                reasoning += " " + line_stripped

        # Calculate overall if not provided
        if overall is None and scores:
            if "dimensions" in rubric:
                total_weight = 0
                weighted_sum = 0
                for dim, score in scores.items():
                    weight = rubric["dimensions"].get(dim, {}).get("weight", 1.0)
                    weighted_sum += score * weight
                    total_weight += weight
                overall = weighted_sum / total_weight if total_weight > 0 else sum(scores.values()) / len(scores)
            else:
                overall = sum(scores.values()) / len(scores) if scores else 0

        return EvaluationResult(
            mode="pointwise",
            score=overall,
            scores_by_dimension=scores,
            reasoning=reasoning.strip() or analysis.strip(),
            raw_response=raw
        )

    def _parse_pairwise_response(self, raw: str) -> dict:
        """Parse pairwise evaluation response."""
        result = {
            "verdict": "TIE",
            "confidence": "MEDIUM",
            "reasoning": ""
        }

        for line in raw.split("\n"):
            line_stripped = line.strip()
            if line_stripped.startswith("VERDICT:"):
                verdict = line_stripped.split(":")[-1].strip().upper()
                if "A" in verdict and "BETTER" in verdict:
                    result["verdict"] = "A_BETTER"
                elif "B" in verdict and "BETTER" in verdict:
                    result["verdict"] = "B_BETTER"
                else:
                    result["verdict"] = "TIE"
            elif line_stripped.startswith("CONFIDENCE:"):
                conf = line_stripped.split(":")[-1].strip().upper()
                if conf in ["HIGH", "MEDIUM", "LOW"]:
                    result["confidence"] = conf
            elif line_stripped.startswith("REASONING:"):
                result["reasoning"] = line_stripped.replace("REASONING:", "").strip()

        return result

    def _pool_pairwise(self, forward: dict, reverse: dict) -> dict:
        """Pool forward and reverse pairwise results."""
        # Normalize reverse (A and B are swapped)
        reverse_normalized_verdict = {
            "A_BETTER": "B_BETTER",
            "B_BETTER": "A_BETTER",
            "TIE": "TIE"
        }.get(reverse["verdict"], "TIE")

        # Check consistency
        if forward["verdict"] == reverse_normalized_verdict:
            return {
                "winner": forward["verdict"],
                "consistency": "CONSISTENT",
                "confidence": "HIGH",
                "position_bias_detected": False
            }

        # Both prefer first position = position bias
        if forward["verdict"] == "A_BETTER" and reverse["verdict"] == "A_BETTER":
            return {
                "winner": "TIE",
                "consistency": "POSITION_BIASED",
                "confidence": "LOW",
                "position_bias_detected": True
            }

        # Other disagreement
        return {
            "winner": "TIE",
            "consistency": "INCONSISTENT",
            "confidence": "LOW",
            "position_bias_detected": False
        }

    def _parse_g_eval_response(self, raw: str, dimension: str) -> dict:
        """Parse G-Eval response with probability estimates."""
        result = {
            "expected_score": 3.0,  # Default
            "probabilities": {},
            "reasoning": "",
            "confidence": "MEDIUM"
        }

        current_section = None
        for line in raw.split("\n"):
            line_stripped = line.strip()

            if line_stripped.startswith("SCORE_PROBABILITIES:"):
                current_section = "probs"
                continue
            elif line_stripped.startswith("EXPECTED_SCORE:"):
                try:
                    result["expected_score"] = float(line_stripped.split(":")[-1].strip())
                except ValueError:
                    pass
                current_section = None
            elif line_stripped.startswith("REASONING:"):
                result["reasoning"] = line_stripped.replace("REASONING:", "").strip()

            if current_section == "probs" and ":" in line_stripped:
                parts = line_stripped.split(":")
                try:
                    score = int(parts[0].strip())
                    prob_str = parts[1].strip().replace("%", "")
                    prob = float(prob_str) / 100 if float(prob_str) > 1 else float(prob_str)
                    result["probabilities"][score] = prob
                except ValueError:
                    pass

        # Calculate expected score from probabilities if not provided
        if result["probabilities"] and result["expected_score"] == 3.0:
            total_prob = sum(result["probabilities"].values())
            if total_prob > 0:
                result["expected_score"] = sum(
                    score * (prob / total_prob)
                    for score, prob in result["probabilities"].items()
                )

        # Calculate confidence from probability distribution entropy
        if result["probabilities"]:
            probs = list(result["probabilities"].values())
            total = sum(probs)
            if total > 0:
                normalized = [p / total for p in probs]
                entropy = -sum(p * math.log(p) if p > 0 else 0 for p in normalized)
                max_entropy = math.log(5)
                normalized_entropy = entropy / max_entropy if max_entropy > 0 else 0

                if normalized_entropy < 0.3:
                    result["confidence"] = "HIGH"
                elif normalized_entropy < 0.6:
                    result["confidence"] = "MEDIUM"
                else:
                    result["confidence"] = "LOW"

        return result

    def _aggregate_confidence(self, results: dict) -> str:
        """Aggregate confidence across dimensions."""
        confidences = [r.get("confidence", "MEDIUM") for r in results.values()]
        conf_scores = {"HIGH": 3, "MEDIUM": 2, "LOW": 1}
        avg = sum(conf_scores[c] for c in confidences) / len(confidences) if confidences else 2

        if avg >= 2.5:
            return "HIGH"
        elif avg >= 1.5:
            return "MEDIUM"
        else:
            return "LOW"


def load_input(path: str) -> dict:
    """Load input from JSON file."""
    with open(path) as f:
        return json.load(f)


def main():
    parser = argparse.ArgumentParser(
        description="LLM Judge - Evaluate AI outputs using LLM-as-a-Judge methodology"
    )
    parser.add_argument(
        "--mode",
        choices=["pointwise", "pairwise", "g-eval"],
        required=True,
        help="Evaluation mode"
    )
    parser.add_argument(
        "--input",
        help="Path to input JSON file (for pointwise/g-eval)"
    )
    parser.add_argument(
        "--input-a",
        help="Path to first response JSON (for pairwise)"
    )
    parser.add_argument(
        "--input-b",
        help="Path to second response JSON (for pairwise)"
    )
    parser.add_argument(
        "--rubric",
        help="Path to rubric YAML file"
    )
    parser.add_argument(
        "--reference",
        help="Path to reference answer (for anchoring)"
    )
    parser.add_argument(
        "--dimensions",
        help="Comma-separated dimensions for G-Eval (e.g., 'accuracy,clarity')"
    )
    parser.add_argument(
        "--criteria",
        help="Comma-separated criteria for pairwise (e.g., 'accuracy,completeness')"
    )
    parser.add_argument(
        "--model",
        default="claude-sonnet-4-20250514",
        help="Model to use as judge"
    )
    parser.add_argument(
        "--provider",
        choices=["anthropic", "openai"],
        default="anthropic",
        help="API provider"
    )
    parser.add_argument(
        "--output",
        help="Output file for results (JSON)"
    )
    parser.add_argument(
        "--no-swap-and-pool",
        action="store_true",
        help="Disable swap-and-pool for pairwise (not recommended)"
    )

    args = parser.parse_args()

    # Initialize judge
    judge = LLMJudge(model=args.model, provider=args.provider)

    # Load rubric if provided
    rubric = None
    if args.rubric:
        rubric = judge.load_rubric(args.rubric)

    # Run evaluation based on mode
    result = None

    if args.mode == "pointwise":
        if not args.input:
            parser.error("--input required for pointwise mode")
        data = load_input(args.input)
        reference = None
        if args.reference:
            with open(args.reference) as f:
                reference = f.read()
        result = judge.pointwise_evaluate(
            prompt=data.get("prompt", ""),
            response=data.get("response", ""),
            rubric=rubric or {},
            reference=reference
        )

    elif args.mode == "pairwise":
        if not args.input_a or not args.input_b:
            parser.error("--input-a and --input-b required for pairwise mode")
        data_a = load_input(args.input_a)
        data_b = load_input(args.input_b)
        criteria = args.criteria.split(",") if args.criteria else ["accuracy", "completeness", "clarity"]
        result = judge.pairwise_evaluate(
            prompt=data_a.get("prompt", data_b.get("prompt", "")),
            response_a=data_a.get("response", ""),
            response_b=data_b.get("response", ""),
            criteria=criteria,
            use_swap_and_pool=not args.no_swap_and_pool
        )

    elif args.mode == "g-eval":
        if not args.input:
            parser.error("--input required for g-eval mode")
        data = load_input(args.input)
        dimensions = args.dimensions.split(",") if args.dimensions else ["accuracy", "clarity", "completeness"]
        result = judge.g_eval(
            prompt=data.get("prompt", ""),
            response=data.get("response", ""),
            dimensions=dimensions,
            rubric=rubric
        )

    # Output results
    if result:
        print(result)

        if args.output:
            with open(args.output, "w") as f:
                json.dump(result.to_dict(), f, indent=2)
            print(f"\nResults saved to {args.output}")


if __name__ == "__main__":
    main()
