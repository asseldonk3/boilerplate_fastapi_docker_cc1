# SAFE Framework - Search-Augmented Factuality Evaluation

This document details the implementation of the SAFE framework for fact-checking LLM outputs using external search verification.

## The Problem: Closed-Loop Hallucination

An LLM cannot reliably verify facts it doesn't know. If you ask an LLM to check whether its own output is factually correct, it will:
- Confidently validate incorrect information (hallucinate confirmation)
- Have no way to access information beyond its training cutoff
- Be unable to distinguish between "I don't know" and "this is false"

**The solution:** Break the closed loop by using external evidence retrieval.

## SAFE Framework Overview

SAFE (Search-Augmented Factuality Evaluator) was developed by Google DeepMind and represents the state-of-the-art in automated fact-checking.

### Key Statistics
- **Cost:** ~$0.19 per response vs ~$4.00 for human annotation (20x cheaper)
- **Agreement with humans:** 72%
- **When SAFE disagrees with humans:** SAFE is correct 76% of the time

### The 5-Step SAFE Workflow

```
┌─────────────────────────────────────────────────────────────────┐
│                    SAFE FRAMEWORK WORKFLOW                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  STEP 1: DECOMPOSITION                                         │
│  ├─ Take the full text to verify                               │
│  ├─ Break it into individual "atomic facts"                    │
│  └─ Each atomic fact = one verifiable claim                    │
│                                                                 │
│  STEP 2: RELEVANCE FILTERING                                   │
│  ├─ Filter out facts irrelevant to the user's query            │
│  └─ Focus evaluation on core information need                  │
│                                                                 │
│  STEP 3: SEARCH QUERY GENERATION                               │
│  ├─ For each atomic fact, generate specific search queries     │
│  └─ Multiple queries per fact for better coverage              │
│                                                                 │
│  STEP 4: EVIDENCE RETRIEVAL                                    │
│  ├─ Execute searches via web search API                        │
│  ├─ Collect snippets from authoritative sources                │
│  └─ Quality-check the evidence (avoid SEO spam, forums)        │
│                                                                 │
│  STEP 5: ADJUDICATION                                          │
│  ├─ Compare each atomic fact against retrieved evidence        │
│  ├─ Label: SUPPORTED / NOT SUPPORTED / IRRELEVANT              │
│  └─ Calculate FactScore                                        │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## Detailed Implementation

### Step 1: Decomposition into Atomic Facts

**Goal:** Break complex statements into individually verifiable claims.

**Input:**
```
"Tesla was founded in 2003 by Elon Musk in San Carlos, California,
and released its first car, the Roadster, in 2008."
```

**Output (Atomic Facts):**
```
1. Tesla was founded in 2003
2. Tesla was founded by Elon Musk
3. Tesla was founded in San Carlos, California
4. Tesla's first car was called the Roadster
5. The Tesla Roadster was released in 2008
```

**Decomposition Prompt:**
```
You are a fact extraction expert. Break down the following text into
individual atomic facts. Each atomic fact should:
- Contain exactly ONE verifiable claim
- Be self-contained (understandable without the original context)
- Be as specific as possible

Text to decompose:
{text}

Output each atomic fact on a new line, numbered.
```

### Step 2: Relevance Filtering

**Goal:** Remove facts that are:
- Subjective opinions (not verifiable)
- Irrelevant to the user's original query
- Trivial/common knowledge that doesn't need verification

**Filtering Prompt:**
```
Given the user's original query and the following atomic facts,
identify which facts are RELEVANT to answering the query and
which are IRRELEVANT or UNVERIFIABLE.

Original query: {query}

Atomic facts:
{facts}

For each fact, output:
- RELEVANT: [fact] - if it directly helps answer the query
- IRRELEVANT: [fact] - if it's tangential
- UNVERIFIABLE: [fact] - if it's subjective/opinion
```

### Step 3: Search Query Generation

**Goal:** Create effective search queries that will retrieve evidence for/against each fact.

**Query Generation Prompt:**
```
Generate 2-3 search queries to verify the following claim.
The queries should:
- Be specific enough to find relevant information
- Use different phrasings to maximize coverage
- Target authoritative sources (Wikipedia, official sites, news)

Claim to verify: {atomic_fact}

Output queries, one per line:
```

**Example:**
```
Claim: "Tesla was founded in 2003"

Generated queries:
1. "Tesla Motors founding year"
2. "When was Tesla Inc founded"
3. "Tesla company history 2003"
```

### Step 4: Evidence Retrieval

**Implementation using mcp__gemini-cli__gemini_google_web_search:**

```python
async def retrieve_evidence(queries: list[str]) -> list[dict]:
    """
    Execute search queries and collect evidence.
    """
    evidence = []

    for query in queries:
        # Use the MCP Gemini web search
        results = await mcp__gemini-cli__gemini_google_web_search(query=query)

        for result in results:
            evidence.append({
                "query": query,
                "source": result.get("url", ""),
                "snippet": result.get("snippet", ""),
                "title": result.get("title", "")
            })

    return evidence
```

**Evidence Quality Check:**
Prioritize sources in this order:
1. Wikipedia, official company/government sites
2. Major news outlets (Reuters, AP, BBC)
3. Academic sources
4. Industry publications
5. (Avoid) Forums, SEO content farms, social media

### Step 5: Adjudication

**Goal:** Compare each atomic fact against the retrieved evidence and render a verdict.

**Adjudication Prompt:**
```
You are a fact-checker. Compare the following claim against the
provided evidence and determine if it is supported.

CLAIM: {atomic_fact}

EVIDENCE:
{evidence_snippets}

Based ONLY on the evidence provided, determine:

1. Is this claim SUPPORTED by the evidence?
2. Is this claim NOT SUPPORTED (contradicted or no evidence)?
3. Is there INSUFFICIENT evidence to determine?

Output format:
VERDICT: [SUPPORTED | NOT_SUPPORTED | INSUFFICIENT]
CONFIDENCE: [HIGH | MEDIUM | LOW]
REASONING: [Explain what evidence supports or contradicts the claim]
```

**Example Adjudication:**
```
CLAIM: "Tesla was founded by Elon Musk"

EVIDENCE:
- Wikipedia: "Tesla, Inc. was founded in July 2003 by Martin Eberhard
  and Marc Tarpenning... Elon Musk joined as chairman in 2004..."

VERDICT: NOT_SUPPORTED
CONFIDENCE: HIGH
REASONING: The evidence clearly states Tesla was founded by Martin
Eberhard and Marc Tarpenning, not Elon Musk. Musk joined later as
an investor and chairman. The claim conflates founder with early
investor.
```

## FactScore Calculation

```
FactScore = (Number of SUPPORTED facts) / (Total RELEVANT facts)
```

**Example:**
```
Total atomic facts: 10
Irrelevant/filtered: 2
Relevant facts: 8

Results:
- SUPPORTED: 6
- NOT_SUPPORTED: 1
- INSUFFICIENT: 1

FactScore = 6/8 = 75%

Interpretation:
- 75%+ : Generally accurate
- 50-75%: Mixed accuracy, needs review
- <50%: Significant hallucination issues
```

## Complete Implementation Example

```python
async def safe_evaluate(text: str, original_query: str) -> dict:
    """
    Full SAFE framework evaluation.
    """
    # Step 1: Decompose
    atomic_facts = await decompose_to_atomic_facts(text)

    # Step 2: Filter
    relevant_facts = await filter_relevant_facts(atomic_facts, original_query)

    results = []

    for fact in relevant_facts:
        # Step 3: Generate queries
        queries = await generate_search_queries(fact)

        # Step 4: Retrieve evidence
        evidence = await retrieve_evidence(queries)

        # Step 5: Adjudicate
        verdict = await adjudicate_fact(fact, evidence)

        results.append({
            "fact": fact,
            "queries": queries,
            "evidence_count": len(evidence),
            "verdict": verdict["verdict"],
            "confidence": verdict["confidence"],
            "reasoning": verdict["reasoning"]
        })

    # Calculate FactScore
    supported = sum(1 for r in results if r["verdict"] == "SUPPORTED")
    total = len(results)

    return {
        "fact_score": supported / total if total > 0 else 0,
        "total_facts": total,
        "supported": supported,
        "not_supported": sum(1 for r in results if r["verdict"] == "NOT_SUPPORTED"),
        "insufficient": sum(1 for r in results if r["verdict"] == "INSUFFICIENT"),
        "details": results
    }
```

## When to Use SAFE

**Ideal for:**
- Research summaries
- Data extraction tasks
- Claim verification
- Technical specifications
- Historical facts
- Statistics and numbers

**Not suitable for:**
- Subjective assessments (quality, beauty, etc.)
- Future predictions
- Opinions and preferences
- Creative writing evaluation

## Comparison: Faithfulness vs. Factuality

| Metric | Faithfulness | Factuality (SAFE) |
|--------|--------------|-------------------|
| **Question** | Is it consistent with provided context? | Is it true in reality? |
| **Reference** | The input documents | External world knowledge |
| **Use case** | RAG systems | General fact-checking |
| **Closed-loop?** | Yes (checks internal consistency) | No (requires external search) |

**Example:**
- Context says: "The sky is green"
- LLM output: "The sky is green"
- Faithfulness: PASS (matches context)
- Factuality: FAIL (sky is blue in reality)

## Holmes Framework Enhancement

The Holmes framework (2024) improves on SAFE by:

1. **Better query generation:** Uses specialized models for search queries
2. **Evidence quality assessment:** Scores evidence reliability before using it
3. **Multi-hop reasoning:** Can follow chains of facts
4. **Source summarization:** Condenses evidence before adjudication

Consider Holmes for:
- Complex, multi-fact claims
- When search results are noisy
- High-stakes verification needs

## Integration Notes

When using SAFE in the llm-judge skill:

1. **Scenario detection:** Trigger SAFE when output contains factual claims
2. **Cost consideration:** Each fact requires 2-3 searches; batch for efficiency
3. **Caching:** Cache search results for repeated queries
4. **Confidence threshold:** Flag facts with INSUFFICIENT evidence for human review
5. **Source citation:** Include source URLs in the evaluation report
