# Bias Mitigation Strategies

LLM judges exhibit systematic biases that distort evaluations. This reference provides comprehensive mitigation strategies based on 2024-2025 research.

## Bias Overview

| Bias Type | Mechanism | Impact | Mitigation |
|-----------|-----------|--------|------------|
| Position | Primacy/Recency effect | 40% verdict flip rate | Swap-and-Pool |
| Verbosity | "Longer = Better" | Penalizes concise answers | Reference anchoring |
| Self-Preference | Stylistic alignment | Inflated scores for own outputs | Panel of judges |
| Sycophancy | Agreeableness | Aligns with input tone | Devil's Advocate |
| Anchoring | First information bias | Over-weights initial claims | Structured evaluation |

---

## 1. Position Bias

### The Problem

Position bias is the tendency to favor responses in a specific position (usually first) regardless of quality. Studies show GPT-4 can flip verdicts up to 40% of the time when identical responses are swapped.

**Root Cause:** Autoregressive attention patterns create structural preference for tokens processed first (primacy) or last (recency).

### Detection

```python
def detect_position_bias(judge, test_cases: list, n_repeats: int = 100) -> dict:
    """
    Detect position bias in a judge model.

    Run identical responses in both positions and measure consistency.
    """
    first_position_wins = 0
    second_position_wins = 0
    ties = 0

    for _ in range(n_repeats):
        for case in test_cases:
            # Use identical responses
            response = case["response"]

            result = judge.pairwise_evaluate(
                prompt=case["prompt"],
                response_a=response,
                response_b=response  # Same response in both positions
            )

            if result["winner"] == "A_BETTER":
                first_position_wins += 1
            elif result["winner"] == "B_BETTER":
                second_position_wins += 1
            else:
                ties += 1

    total = first_position_wins + second_position_wins + ties
    return {
        "first_position_rate": first_position_wins / total,
        "second_position_rate": second_position_wins / total,
        "tie_rate": ties / total,
        "bias_detected": abs(first_position_wins - second_position_wins) / total > 0.1,
        "bias_direction": "PRIMACY" if first_position_wins > second_position_wins else "RECENCY"
    }
```

### Mitigation: Swap-and-Pool Protocol

**Implementation:**

```python
class PositionDebiasedJudge:
    """Judge with automatic position bias mitigation."""

    def __init__(self, base_judge, strict_mode: bool = True):
        self.judge = base_judge
        self.strict_mode = strict_mode

    def evaluate(self, prompt: str, response_a: str, response_b: str) -> dict:
        # Forward pass
        forward = self.judge.pairwise_evaluate(prompt, response_a, response_b)

        # Reverse pass
        reverse = self.judge.pairwise_evaluate(prompt, response_b, response_a)

        # Pool results
        return self._pool(forward, reverse)

    def _pool(self, forward: dict, reverse: dict) -> dict:
        # Normalize reverse (A and B are swapped)
        reverse_normalized = self._normalize_reverse(reverse)

        # Check for consistency
        if forward["winner"] == reverse_normalized["winner"]:
            return {
                "winner": forward["winner"],
                "consistency": "CONSISTENT",
                "confidence": max(forward["confidence"], reverse_normalized["confidence"]),
                "forward_result": forward,
                "reverse_result": reverse_normalized
            }

        # Both prefer first position = position bias
        if forward["winner"] == "A_BETTER" and reverse["winner"] == "A_BETTER":
            if self.strict_mode:
                return {
                    "winner": "TIE",
                    "consistency": "POSITION_BIASED",
                    "confidence": "LOW",
                    "note": "Position bias detected - both passes preferred first position"
                }
            else:
                # Use probability-based pooling
                return self._probability_pool(forward, reverse)

        # Other disagreement
        return {
            "winner": "TIE",
            "consistency": "INCONSISTENT",
            "confidence": "LOW",
            "note": f"Disagreement: forward={forward['winner']}, reverse={reverse['winner']}"
        }

    def _probability_pool(self, forward: dict, reverse: dict) -> dict:
        """
        Pool using probability scores when available.
        Average the probability mass assigned to each response.
        """
        if "probability_a" not in forward:
            return {"winner": "TIE", "method": "fallback"}

        # Forward: P(A), P(B)
        # Reverse: P(A) is actually P(B) in original terms
        prob_a = (forward["probability_a"] + reverse["probability_b"]) / 2
        prob_b = (forward["probability_b"] + reverse["probability_a"]) / 2

        if prob_a > prob_b + 0.1:  # Threshold for clear winner
            return {"winner": "A_BETTER", "confidence": prob_a - prob_b}
        elif prob_b > prob_a + 0.1:
            return {"winner": "B_BETTER", "confidence": prob_b - prob_a}
        else:
            return {"winner": "TIE", "confidence": 0}

    def _normalize_reverse(self, reverse: dict) -> dict:
        """Swap A/B labels in reverse result."""
        mapping = {"A_BETTER": "B_BETTER", "B_BETTER": "A_BETTER", "TIE": "TIE"}
        return {
            **reverse,
            "winner": mapping.get(reverse["winner"], "TIE"),
            "probability_a": reverse.get("probability_b"),
            "probability_b": reverse.get("probability_a")
        }
```

---

## 2. Verbosity Bias

### The Problem

LLM judges consistently assign higher scores to longer, more verbose responses, even when shorter responses are more accurate and appropriate.

**Root Cause:** RLHF training where human annotators conflated length with comprehensiveness.

### Detection

```python
def detect_verbosity_bias(judge, test_cases: list) -> dict:
    """
    Test if judge prefers verbose responses over concise but correct ones.
    """
    verbose_wins = 0
    concise_wins = 0
    ties = 0

    for case in test_cases:
        # Create concise and verbose versions
        concise = case["concise_correct_response"]
        verbose = case["verbose_padded_response"]  # Same info but with fluff

        result = judge.pairwise_evaluate(case["prompt"], concise, verbose)

        if result["winner"] == "A_BETTER":
            concise_wins += 1
        elif result["winner"] == "B_BETTER":
            verbose_wins += 1
        else:
            ties += 1

    total = verbose_wins + concise_wins + ties
    return {
        "verbose_preference_rate": verbose_wins / total,
        "concise_preference_rate": concise_wins / total,
        "verbosity_bias_detected": verbose_wins / total > 0.4,
        "recommendation": "Apply reference anchoring" if verbose_wins / total > 0.4 else "OK"
    }
```

### Mitigation Strategies

#### Strategy 1: Reference Anchoring

Provide a concise "gold reference" to anchor the judge's expectations:

```python
def evaluate_with_reference(prompt: str, response: str,
                            reference: str, judge) -> dict:
    """
    Evaluate response using a reference answer as anchor.
    """
    evaluation_prompt = f"""
Evaluate the candidate response against the reference answer.

## Reference Answer (this is what a good response looks like)
{reference}

## Prompt
{prompt}

## Candidate Response
{response}

## Instructions
Compare the candidate to the reference in terms of:
1. Information coverage - Does it contain the same key information?
2. Accuracy - Is all information correct?
3. Efficiency - Does it avoid unnecessary content?

IMPORTANT: A response that covers the same information more concisely
is BETTER than one that adds unnecessary elaboration.

Score: [1-5 based on how well candidate matches reference quality]
"""
    return judge.evaluate(evaluation_prompt)
```

#### Strategy 2: Explicit Anti-Verbosity Instructions

```python
ANTI_VERBOSITY_PROMPT = """
EVALUATION GUIDELINES:
- Penalize unnecessary verbosity, filler phrases, and repetition
- Value precision and conciseness
- A shorter response that fully answers the question is BETTER than
  a longer response that adds irrelevant information
- Watch for: "In summary", "To elaborate", excessive bullet points,
  restating the question, generic conclusions

SCORING ADJUSTMENT:
- Subtract 1 point for significant unnecessary verbosity
- Add 1 point for achieving the same quality in fewer words
"""
```

#### Strategy 3: Word-Count Normalized Scoring

```python
def verbosity_adjusted_score(response: str, base_score: float,
                             reference_length: int) -> float:
    """
    Adjust score based on verbosity relative to reference.
    """
    response_length = len(response.split())
    length_ratio = response_length / reference_length

    # Penalize responses much longer than reference
    if length_ratio > 1.5:
        penalty = min(0.5, (length_ratio - 1.5) * 0.2)
        return base_score - penalty
    # Slight bonus for concise responses that maintain quality
    elif length_ratio < 0.8 and base_score >= 4:
        bonus = 0.2
        return min(5.0, base_score + bonus)

    return base_score
```

---

## 3. Self-Preference Bias

### The Problem

Models rate their own outputs (or outputs from their model family) higher than equivalent outputs from other models.

**Root Cause:** Models are fine-tuned to maximize probability of their own distribution, creating stylistic alignment.

### Detection

```python
def detect_self_preference(models: list, prompts: list) -> dict:
    """
    Test for self-preference bias across model families.
    """
    results = []

    for prompt in prompts:
        # Generate response from each model
        responses = {model.name: model.generate(prompt) for model in models}

        for judge_model in models:
            for target_model in models:
                # Have judge evaluate target's response
                score = judge_model.pointwise_evaluate(
                    prompt, responses[target_model.name]
                )

                results.append({
                    "judge": judge_model.name,
                    "target": target_model.name,
                    "score": score["score"],
                    "is_self": judge_model.name == target_model.name
                })

    # Analyze for self-preference
    df = pd.DataFrame(results)
    self_scores = df[df["is_self"]]["score"].mean()
    other_scores = df[~df["is_self"]]["score"].mean()

    return {
        "self_score_mean": self_scores,
        "other_score_mean": other_scores,
        "self_preference_detected": self_scores > other_scores + 0.3,
        "bias_magnitude": self_scores - other_scores
    }
```

### Mitigation: Panel of Judges

Use multiple judge models from different families and aggregate:

```python
class JudgePanel:
    """
    Panel of diverse judges to mitigate self-preference bias.
    """

    def __init__(self, judges: list[dict]):
        """
        Args:
            judges: List of {"name": str, "model": Judge, "weight": float}
        """
        self.judges = judges
        self._validate_diversity()

    def _validate_diversity(self):
        """Ensure judges are from different model families."""
        families = set()
        for judge in self.judges:
            family = judge.get("family", judge["name"].split("-")[0])
            if family in families:
                print(f"Warning: Multiple judges from {family} family")
            families.add(family)

    def evaluate(self, prompt: str, response: str,
                 target_model: str = None) -> dict:
        """
        Get consensus evaluation from judge panel.

        Args:
            target_model: If provided, exclude judges from same family
        """
        scores = []
        details = []

        for judge in self.judges:
            # Skip if same family as target (self-preference)
            if target_model:
                judge_family = judge.get("family", judge["name"].split("-")[0])
                target_family = target_model.split("-")[0]
                if judge_family.lower() == target_family.lower():
                    continue

            result = judge["model"].pointwise_evaluate(prompt, response)
            weighted_score = result["score"] * judge["weight"]

            scores.append(weighted_score)
            details.append({
                "judge": judge["name"],
                "score": result["score"],
                "weighted": weighted_score,
                "reasoning": result.get("reasoning")
            })

        # Aggregate
        total_weight = sum(j["weight"] for j in self.judges
                          if not self._should_skip(j, target_model))
        aggregate_score = sum(scores) / total_weight if total_weight > 0 else 0

        return {
            "aggregate_score": aggregate_score,
            "judge_scores": details,
            "agreement": self._calculate_agreement(details),
            "num_judges": len(details)
        }

    def _should_skip(self, judge: dict, target_model: str) -> bool:
        if not target_model:
            return False
        judge_family = judge.get("family", judge["name"].split("-")[0])
        target_family = target_model.split("-")[0]
        return judge_family.lower() == target_family.lower()

    def _calculate_agreement(self, details: list) -> str:
        """Calculate inter-judge agreement."""
        scores = [d["score"] for d in details]
        if not scores:
            return "N/A"

        std = np.std(scores)
        if std < 0.5:
            return "HIGH"
        elif std < 1.0:
            return "MEDIUM"
        else:
            return "LOW"


# Example usage
panel = JudgePanel([
    {"name": "claude-3-5-sonnet", "model": ClaudeJudge(), "weight": 1.0, "family": "claude"},
    {"name": "gpt-4o", "model": GPTJudge(), "weight": 1.0, "family": "gpt"},
    {"name": "llama-3-70b", "model": LlamaJudge(), "weight": 0.8, "family": "llama"},
])
```

---

## 4. Sycophancy Bias

### The Problem

Judges tend to align with the user's premise or the input prompt's tone, even when factually incorrect.

**Example:** If the prompt implies a response is good, the judge is more likely to rate it highly.

### Mitigation: Devil's Advocate Prompting

```python
DEVILS_ADVOCATE_PROMPT = """
You are an extremely critical evaluator. Your job is to find problems.

Before assigning any positive score, you must:
1. Actively search for errors, inaccuracies, or weaknesses
2. Question every claim made in the response
3. Consider how the response could mislead or fail the user
4. Look for what's MISSING, not just what's present

IMPORTANT: Do not assume the response is correct. Verify claims.
Do not be swayed by confident tone or professional formatting.

After your critical analysis, provide a fair score.
"""
```

### Mitigation: Fact-Checking Pipeline

```python
def evaluate_with_fact_check(prompt: str, response: str,
                             judge, fact_checker) -> dict:
    """
    Two-stage evaluation: fact-check then assess.
    """
    # Stage 1: Fact extraction and verification
    claims = fact_checker.extract_claims(response)
    verified_claims = fact_checker.verify(claims)

    factual_accuracy = sum(1 for c in verified_claims if c["verified"]) / len(verified_claims)

    # Stage 2: Quality assessment with fact-check context
    evaluation_prompt = f"""
Evaluate this response. Note: Fact-checking has been performed.

## Fact-Check Results
Accuracy: {factual_accuracy:.0%}
Verified claims: {len([c for c in verified_claims if c['verified']])}
Unverified/false claims: {len([c for c in verified_claims if not c['verified']])}

Details:
{format_fact_check_results(verified_claims)}

## Response to Evaluate
{response}

Given the fact-check results, assign an appropriate score.
"""
    return judge.evaluate(evaluation_prompt)
```

---

## 5. Comprehensive Bias Mitigation Pipeline

Combine all strategies into a single robust evaluation:

```python
class DebiasedEvaluator:
    """
    Complete bias-mitigated evaluation pipeline.
    """

    def __init__(self, config: dict):
        self.panel = JudgePanel(config["judges"])
        self.use_reference = config.get("use_reference", True)
        self.fact_check = config.get("fact_check", False)
        self.anti_verbosity = config.get("anti_verbosity", True)

    def evaluate(self, prompt: str, response: str,
                 reference: str = None,
                 target_model: str = None) -> dict:
        """
        Full debiased evaluation.
        """
        evaluation_context = {
            "prompt": prompt,
            "response": response,
            "biases_mitigated": []
        }

        # Build evaluation prompt
        eval_prompt = self._build_prompt(prompt, response, reference)

        # Get panel evaluation (mitigates self-preference)
        result = self.panel.evaluate(eval_prompt, response, target_model)
        evaluation_context["biases_mitigated"].append("self_preference")

        # Apply verbosity adjustment
        if self.anti_verbosity and reference:
            ref_len = len(reference.split())
            result["aggregate_score"] = verbosity_adjusted_score(
                response, result["aggregate_score"], ref_len
            )
            evaluation_context["biases_mitigated"].append("verbosity")

        return {
            **result,
            **evaluation_context
        }

    def pairwise_evaluate(self, prompt: str, response_a: str, response_b: str,
                         target_model_a: str = None,
                         target_model_b: str = None) -> dict:
        """
        Pairwise with position bias mitigation.
        """
        # Forward pass
        forward_result = self._single_pairwise(prompt, response_a, response_b)

        # Reverse pass
        reverse_result = self._single_pairwise(prompt, response_b, response_a)

        # Pool (mitigates position bias)
        return self._pool_pairwise(forward_result, reverse_result)

    def _build_prompt(self, prompt: str, response: str, reference: str) -> str:
        parts = [prompt]

        if reference:
            parts.append(f"\n## Reference Answer\n{reference}")

        if self.anti_verbosity:
            parts.append(ANTI_VERBOSITY_PROMPT)

        parts.append(DEVILS_ADVOCATE_PROMPT)

        return "\n\n".join(parts)
```

---

## Bias Mitigation Checklist

Before running evaluations, verify:

- [ ] **Position Bias**: Swap-and-Pool enabled for pairwise comparisons
- [ ] **Verbosity Bias**: Reference provided OR anti-verbosity prompting enabled
- [ ] **Self-Preference**: Using panel of judges from diverse model families
- [ ] **Sycophancy**: Devil's Advocate prompting OR fact-checking enabled
- [ ] **Anchoring**: Structured evaluation with explicit criteria order

## Recommended Default Configuration

```python
DEFAULT_CONFIG = {
    "judges": [
        {"name": "claude-3-5-sonnet", "weight": 1.0, "family": "claude"},
        {"name": "gpt-4o-mini", "weight": 0.8, "family": "gpt"},
    ],
    "use_reference": True,
    "anti_verbosity": True,
    "fact_check": False,  # Enable for factual evaluation tasks
    "position_debiasing": "swap_and_pool",
    "strict_consistency": True
}
```
