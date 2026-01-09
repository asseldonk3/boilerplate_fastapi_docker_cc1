# Evaluation Frameworks - Deep Dive

This reference provides detailed implementation guidance for each evaluation framework.

## 1. Pointwise Evaluation (Direct Assessment)

### Mathematical Foundation

The judge approximates a scoring function:

```
S = f(x, y, C)

where:
  x = prompt/instruction
  y = candidate response
  C = evaluation criteria/rubric
  S = scalar score or classification
```

### Implementation

```python
def pointwise_evaluate(prompt: str, response: str, rubric: dict) -> dict:
    """
    Pointwise evaluation using direct assessment.

    Args:
        prompt: The original instruction/query
        response: The candidate response to evaluate
        rubric: Dictionary defining scoring criteria

    Returns:
        dict with score, reasoning, and confidence
    """
    evaluation_prompt = f"""
You are an expert evaluator. Assess the following response using the provided rubric.

## Rubric
{format_rubric(rubric)}

## Original Prompt
{prompt}

## Response to Evaluate
{response}

## Instructions
1. First, analyze the response against each rubric criterion
2. Identify specific strengths and weaknesses
3. Assign a score based on the rubric
4. Provide brief reasoning for your score

Output format:
ANALYSIS: [Your detailed analysis]
SCORE: [Single integer from rubric scale]
REASONING: [1-2 sentence justification]
"""

    result = call_judge_model(evaluation_prompt)
    return parse_pointwise_result(result)
```

### Rubric Design Patterns

**Likert Scale (1-5):**
```yaml
scale:
  5: "Excellent - Fully correct, comprehensive, well-formatted"
  4: "Good - Mostly correct with minor issues"
  3: "Acceptable - Correct but incomplete or has some fluff"
  2: "Poor - Contains errors or significant omissions"
  1: "Unacceptable - Incorrect, harmful, or irrelevant"

criteria:
  - name: "Factual Accuracy"
    weight: 0.4
  - name: "Completeness"
    weight: 0.3
  - name: "Clarity"
    weight: 0.3
```

**Binary Classification:**
```yaml
labels:
  - "PASS": "Response meets all minimum quality criteria"
  - "FAIL": "Response fails one or more minimum criteria"

minimum_criteria:
  - "No factual errors"
  - "Addresses the user's question"
  - "No harmful content"
  - "Follows format instructions"
```

### Addressing Calibration Issues

**Problem:** LLMs exhibit grade inflation and score clustering.

**Solutions:**

1. **Anchor with examples:**
```python
few_shot_examples = [
    {"response": example_score_5, "score": 5, "reasoning": "..."},
    {"response": example_score_3, "score": 3, "reasoning": "..."},
    {"response": example_score_1, "score": 1, "reasoning": "..."},
]
```

2. **Force distribution:**
```python
# After batch evaluation, normalize scores
scores = normalize_to_distribution(raw_scores, target_mean=3.0, target_std=1.0)
```

3. **Relative anchoring:**
```
Compare to this reference answer (Score 4):
{reference}

Is the candidate response better, equal, or worse than the reference?
```

---

## 2. Pairwise Evaluation (Comparative Assessment)

### Mathematical Foundation

The judge determines preference between two responses:

```
P(A > B) = preference function

Aggregation via Bradley-Terry model:
P(i > j) = γᵢ / (γᵢ + γⱼ)

where γ represents latent skill parameters
```

### Implementation with Swap-and-Pool

```python
def pairwise_evaluate(prompt: str, response_a: str, response_b: str,
                      criteria: list[str]) -> dict:
    """
    Pairwise evaluation with position bias mitigation.

    CRITICAL: Always run both forward and reverse passes.
    """

    def make_comparison_prompt(resp_first: str, resp_second: str) -> str:
        return f"""
Compare the following two responses to the prompt.

## Original Prompt
{prompt}

## Response A
{resp_first}

## Response B
{resp_second}

## Evaluation Criteria
{format_criteria(criteria)}

## Instructions
1. Analyze both responses against each criterion
2. Identify the key differences
3. Determine which response is better overall
4. Provide your verdict with confidence

Output format:
ANALYSIS: [Comparative analysis]
VERDICT: [A_BETTER | B_BETTER | TIE]
CONFIDENCE: [HIGH | MEDIUM | LOW]
REASONING: [Brief justification]
"""

    # Forward pass: A first, B second
    forward_prompt = make_comparison_prompt(response_a, response_b)
    forward_result = call_judge_model(forward_prompt)

    # Reverse pass: B first, A second
    reverse_prompt = make_comparison_prompt(response_b, response_a)
    reverse_result = call_judge_model(reverse_prompt)

    # Pool results
    return pool_pairwise_results(forward_result, reverse_result)


def pool_pairwise_results(forward: dict, reverse: dict) -> dict:
    """
    Pool forward and reverse passes to mitigate position bias.

    Outcomes:
    - Consistent: Both passes agree on winner
    - Position-biased: Both prefer first position
    - Inconsistent: Other disagreements
    """
    forward_winner = forward["verdict"]
    reverse_winner = reverse["verdict"]

    # Normalize reverse result (swap A/B labels)
    if reverse_winner == "A_BETTER":
        reverse_normalized = "B_BETTER"
    elif reverse_winner == "B_BETTER":
        reverse_normalized = "A_BETTER"
    else:
        reverse_normalized = "TIE"

    # Check consistency
    if forward_winner == reverse_normalized:
        return {
            "winner": forward_winner,
            "consistency": "CONSISTENT",
            "confidence": "HIGH",
            "position_bias_detected": False
        }

    # Position bias: both prefer first position
    if forward_winner == "A_BETTER" and reverse_winner == "A_BETTER":
        return {
            "winner": "TIE",
            "consistency": "POSITION_BIASED",
            "confidence": "LOW",
            "position_bias_detected": True,
            "note": "Judge preferred first position in both passes"
        }

    # Other inconsistency
    return {
        "winner": "TIE",
        "consistency": "INCONSISTENT",
        "confidence": "LOW",
        "position_bias_detected": False,
        "note": f"Forward: {forward_winner}, Reverse: {reverse_winner}"
    }
```

### Elo Rating Calculation

For tournament-style model comparison:

```python
def update_elo(winner_elo: float, loser_elo: float, k: float = 32) -> tuple:
    """
    Update Elo ratings after a match.

    Args:
        winner_elo: Current Elo of winner
        loser_elo: Current Elo of loser
        k: K-factor (sensitivity)

    Returns:
        (new_winner_elo, new_loser_elo)
    """
    expected_winner = 1 / (1 + 10 ** ((loser_elo - winner_elo) / 400))
    expected_loser = 1 - expected_winner

    new_winner = winner_elo + k * (1 - expected_winner)
    new_loser = loser_elo + k * (0 - expected_loser)

    return new_winner, new_loser


def run_tournament(models: list, prompts: list, judge) -> dict:
    """
    Run round-robin tournament to rank models.
    """
    elos = {model: 1000.0 for model in models}

    for prompt in prompts:
        for i, model_a in enumerate(models):
            for model_b in models[i+1:]:
                response_a = model_a.generate(prompt)
                response_b = model_b.generate(prompt)

                result = pairwise_evaluate(prompt, response_a, response_b)

                if result["winner"] == "A_BETTER":
                    elos[model_a], elos[model_b] = update_elo(elos[model_a], elos[model_b])
                elif result["winner"] == "B_BETTER":
                    elos[model_b], elos[model_a] = update_elo(elos[model_b], elos[model_a])
                # TIE: no update

    return dict(sorted(elos.items(), key=lambda x: x[1], reverse=True))
```

---

## 3. G-Eval (Probabilistic Continuous Scoring)

### Mathematical Foundation

G-Eval extracts probability distributions over score tokens:

```
Score = Σ P(s) × s  for s in {1, 2, 3, 4, 5}

where P(s) is the probability of token s given the evaluation context
```

### Implementation

```python
def g_eval(prompt: str, response: str, dimension: str,
           rubric: dict, model: str = "gpt-4") -> dict:
    """
    G-Eval: Probabilistic continuous scoring.

    Key insight: Don't just take the most likely token,
    extract the probability distribution.
    """

    # Step 1: Chain-of-Thought evaluation
    cot_prompt = f"""
Evaluate the following response for {dimension}.

## Rubric for {dimension}
{rubric[dimension]}

## Original Prompt
{prompt}

## Response to Evaluate
{response}

## Instructions
First, provide a detailed analysis of the response's {dimension}.
Consider specific examples from the response.
Then, assign a score from 1-5 based on the rubric.

Analysis:"""

    # Get CoT reasoning
    cot_response = call_model(cot_prompt, max_tokens=500)

    # Step 2: Extract score with logprobs
    score_prompt = f"""
{cot_prompt}

{cot_response}

Based on this analysis, the score for {dimension} is:"""

    # Request logprobs for score tokens
    logprobs_response = call_model_with_logprobs(
        score_prompt,
        max_tokens=1,
        logprobs=5,  # Get top 5 token probabilities
        model=model
    )

    # Step 3: Calculate expected value
    score_probs = extract_score_probabilities(logprobs_response)
    expected_score = sum(score * prob for score, prob in score_probs.items())

    return {
        "dimension": dimension,
        "expected_score": expected_score,
        "score_distribution": score_probs,
        "reasoning": cot_response,
        "confidence": calculate_confidence(score_probs)
    }


def extract_score_probabilities(logprobs_response: dict) -> dict:
    """
    Extract probability distribution for valid score tokens.
    """
    valid_scores = {"1", "2", "3", "4", "5"}
    raw_probs = {}

    for token, logprob in logprobs_response["top_logprobs"].items():
        if token.strip() in valid_scores:
            raw_probs[int(token.strip())] = math.exp(logprob)

    # Normalize to sum to 1
    total = sum(raw_probs.values())
    return {score: prob / total for score, prob in raw_probs.items()}


def calculate_confidence(score_probs: dict) -> str:
    """
    Confidence based on entropy of distribution.
    High confidence = low entropy (one score dominates)
    """
    entropy = -sum(p * math.log(p) for p in score_probs.values() if p > 0)
    max_entropy = math.log(5)  # Maximum when uniform

    normalized_entropy = entropy / max_entropy

    if normalized_entropy < 0.3:
        return "HIGH"
    elif normalized_entropy < 0.6:
        return "MEDIUM"
    else:
        return "LOW"
```

### Multi-Dimension G-Eval

For comprehensive evaluation across multiple dimensions:

```python
def multi_dimension_g_eval(prompt: str, response: str,
                           dimensions: list[str], rubric: dict) -> dict:
    """
    Evaluate across multiple quality dimensions.

    Common dimensions:
    - Coherence: Logical flow and structure
    - Factuality: Accuracy of claims
    - Fluency: Language quality
    - Relevance: Alignment with prompt
    - Completeness: Coverage of required information
    """
    results = {}

    for dimension in dimensions:
        results[dimension] = g_eval(prompt, response, dimension, rubric)

    # Calculate aggregate score
    aggregate = sum(r["expected_score"] for r in results.values()) / len(dimensions)

    return {
        "dimensions": results,
        "aggregate_score": aggregate,
        "lowest_dimension": min(results.items(), key=lambda x: x[1]["expected_score"]),
        "highest_dimension": max(results.items(), key=lambda x: x[1]["expected_score"])
    }
```

### G-Eval vs Standard Pointwise

| Aspect | Standard Pointwise | G-Eval |
|--------|-------------------|--------|
| Output | Discrete (3 or 4) | Continuous (3.47) |
| Uncertainty | Hidden | Captured in distribution |
| Human correlation | Moderate | Higher |
| Compute cost | 1 call | 1-2 calls + logprobs |
| Granularity | Coarse | Fine |

---

## 4. Choosing the Right Framework

### Decision Tree

```
Is this a comparison task?
├── YES → Do you have ground truth?
│   ├── YES → Pointwise with reference
│   └── NO → Pairwise
└── NO → Is precision critical?
    ├── YES → G-Eval
    └── NO → Pointwise (faster)
```

### Hybrid Approaches

For production systems, combine frameworks:

```python
def hybrid_evaluate(prompt: str, responses: list[str],
                    ground_truth: str = None) -> dict:
    """
    Hybrid evaluation combining multiple frameworks.
    """
    # Stage 1: Quick filter with pointwise (binary pass/fail)
    passed = []
    for resp in responses:
        result = pointwise_evaluate(prompt, resp, MINIMUM_QUALITY_RUBRIC)
        if result["score"] >= 3:
            passed.append(resp)

    if len(passed) == 0:
        return {"winner": None, "note": "All responses failed quality gate"}

    if len(passed) == 1:
        return {"winner": passed[0], "method": "only_passing"}

    # Stage 2: Fine-grained comparison with G-Eval
    scores = {}
    for resp in passed:
        result = multi_dimension_g_eval(prompt, resp,
                                        ["accuracy", "completeness", "clarity"])
        scores[resp] = result["aggregate_score"]

    # Stage 3: If close scores, use pairwise for final decision
    sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    if sorted_scores[0][1] - sorted_scores[1][1] < 0.3:  # Close scores
        result = pairwise_evaluate(prompt, sorted_scores[0][0], sorted_scores[1][0])
        return {"winner": result["winner"], "method": "pairwise_tiebreak"}

    return {"winner": sorted_scores[0][0], "method": "g_eval", "scores": scores}
```
