# Meta-Evaluation: Judging the Judge

This document covers how to validate, calibrate, and continuously improve your LLM-as-a-Judge system.

## The Problem: Trusting the Judge

Before deploying an automated evaluation system, you need to answer:
- Does this judge agree with human experts?
- Is it calibrated correctly (not systematically over/under-scoring)?
- Will it remain reliable over time?
- Can we detect when it's failing?

## Golden Set Validation

### What is a Golden Set?

A **Golden Set** is a curated collection of examples with expert-labeled evaluations:
- 50-100 examples (minimum)
- Labeled by domain experts (not crowdworkers)
- Diverse coverage of quality levels (good, medium, bad)
- Representative of your actual production data

### Creating a Golden Set

```yaml
golden_set_example:
  - id: "gs_001"
    prompt: "Write a product description for wireless earbuds"
    output: "Experience crystal-clear audio with our EarPod Pro..."
    expert_scores:
      accuracy: 4
      clarity: 5
      completeness: 4
      overall: 4.3
    expert_reasoning: "Clear, accurate, missing battery life info"
    annotator: "senior_content_editor"
    timestamp: "2025-01-05"

  - id: "gs_002"
    prompt: "Summarize the quarterly earnings report"
    output: "Q3 revenue increased by 15%..."
    expert_scores:
      accuracy: 2
      clarity: 4
      completeness: 3
      overall: 3.0
    expert_reasoning: "Revenue figure incorrect (actual: 12%)"
    annotator: "finance_analyst"
    timestamp: "2025-01-05"
```

### Best Practices for Golden Sets

1. **Multiple annotators:** Have 2-3 experts label each example
2. **Include edge cases:** Deliberately include difficult examples
3. **Score distribution:** Ensure you have examples at all quality levels
4. **Regular updates:** Add new examples as you find interesting cases
5. **Version control:** Track changes to the golden set over time

## Correlation Metrics

### Pearson Correlation

Measures linear relationship between judge scores and human scores:

```
Pearson r = cov(judge, human) / (std(judge) × std(human))
```

- **r > 0.8:** Excellent agreement
- **r > 0.7:** Good agreement (deployment threshold)
- **r > 0.5:** Moderate agreement
- **r < 0.5:** Poor agreement (do not deploy)

### Spearman Correlation

Measures monotonic relationship (better for ordinal data):

```
Spearman ρ = 1 - (6 × Σd²) / (n × (n² - 1))
```

Where d = difference in ranks between judge and human.

**Use Spearman when:**
- Scores are ordinal (1-5 scale)
- You care more about ranking than exact values

### Agreement Rate

Simple percentage of exact matches:

```
Agreement = (matches) / (total) × 100%
```

Consider "close agreement" (within 0.5 points) for continuous scores.

## Calibration Analysis

### What is Calibration?

A judge is **well-calibrated** if its scores match the distribution of human scores. Common calibration issues:

| Issue | Description | Detection |
|-------|-------------|-----------|
| **Grade inflation** | Scores systematically too high | Mean(judge) >> Mean(human) |
| **Central tendency** | Avoiding extreme scores (1 or 5) | Low std(judge) |
| **Score clustering** | All scores in narrow range | Histogram analysis |
| **Threshold bias** | Different behavior at score boundaries | Confusion matrix |

### Calibration Correction

If you detect systematic bias, apply post-hoc correction:

```python
def calibrate_scores(judge_scores, human_mean, human_std):
    """
    Z-score normalization to match human distribution.
    """
    judge_mean = np.mean(judge_scores)
    judge_std = np.std(judge_scores)

    # Normalize to human distribution
    calibrated = (judge_scores - judge_mean) / judge_std
    calibrated = calibrated * human_std + human_mean

    return np.clip(calibrated, 1, 5)  # Keep in valid range
```

## Running a Meta-Evaluation

### Step-by-Step Process

```
┌─────────────────────────────────────────────────────────────────┐
│ META-EVALUATION WORKFLOW                                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│ 1. PREPARE GOLDEN SET                                          │
│    └─ 50-100 expert-labeled examples                           │
│                                                                 │
│ 2. RUN AUTOMATED JUDGE                                         │
│    └─ Evaluate all golden set examples                         │
│    └─ Record scores and reasoning                              │
│                                                                 │
│ 3. CALCULATE CORRELATION                                       │
│    └─ Pearson/Spearman with human scores                       │
│    └─ Per-dimension and overall                                │
│                                                                 │
│ 4. ANALYZE CALIBRATION                                         │
│    └─ Compare score distributions                              │
│    └─ Check for systematic bias                                │
│                                                                 │
│ 5. ERROR ANALYSIS                                              │
│    └─ Examine cases with large disagreement                    │
│    └─ Identify patterns in failures                            │
│                                                                 │
│ 6. DECISION                                                    │
│    └─ Correlation > 0.7? → Deploy                              │
│    └─ Correlation < 0.7? → Improve judge or rubrics            │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Meta-Evaluation Report Template

```yaml
meta_evaluation_report:
  date: "2025-01-08"
  golden_set_version: "v2.3"
  golden_set_size: 75

  judge_configuration:
    model: "claude-opus-4"
    rubric: "general_quality.yaml"
    bias_mitigation: ["swap_and_pool", "verbosity_penalty"]

  correlation_metrics:
    pearson_overall: 0.78
    spearman_overall: 0.81
    pearson_by_dimension:
      accuracy: 0.82
      clarity: 0.75
      completeness: 0.79

  agreement_metrics:
    exact_match: 0.45
    within_0.5: 0.72
    within_1.0: 0.89

  calibration_analysis:
    judge_mean: 3.8
    human_mean: 3.5
    judge_std: 0.9
    human_std: 1.1
    bias_detected: "slight_inflation"
    correction_applied: false

  error_analysis:
    total_large_disagreements: 8  # |judge - human| > 1.5
    patterns_identified:
      - "Judge overrates verbose responses (3 cases)"
      - "Judge misses subtle factual errors (2 cases)"

  recommendation: "DEPLOY with verbosity penalty increase"
```

## Continuous Monitoring

### Drift Detection

Once deployed, monitor for **evaluation drift**:

```python
def detect_drift(recent_scores, baseline_scores, threshold=0.1):
    """
    Detect if recent evaluations have drifted from baseline.
    """
    recent_mean = np.mean(recent_scores)
    baseline_mean = np.mean(baseline_scores)

    drift = abs(recent_mean - baseline_mean)

    if drift > threshold:
        return {
            "drift_detected": True,
            "drift_magnitude": drift,
            "direction": "inflation" if recent_mean > baseline_mean else "deflation"
        }
    return {"drift_detected": False}
```

### Tracking Over Time

```yaml
evaluation_history:
  - week: "2025-W01"
    evaluations: 1247
    mean_score: 3.72
    std_score: 0.95
    human_feedback_received: 23
    feedback_agreement: 0.87

  - week: "2025-W02"
    evaluations: 1389
    mean_score: 3.81  # ← Slight drift?
    std_score: 0.88
    human_feedback_received: 31
    feedback_agreement: 0.84
```

## Human-in-the-Loop Integration

### When to Escalate to Humans

```
┌─────────────────────────────────────────────────────────────────┐
│ ESCALATION TRIGGERS                                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│ 1. LOW CONFIDENCE                                              │
│    └─ Judge confidence < threshold                              │
│    └─ Multi-judge disagreement                                  │
│    └─ Self-consistency voting split                             │
│                                                                 │
│ 2. EDGE CASES                                                  │
│    └─ Score near pass/fail boundary                             │
│    └─ Novel content type                                        │
│    └─ Unusual prompt structure                                  │
│                                                                 │
│ 3. RANDOM SAMPLING                                             │
│    └─ 5-10% of evaluations for ongoing calibration              │
│                                                                 │
│ 4. USER DISPUTE                                                │
│    └─ User disagrees with automated evaluation                  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Feedback Loop

```
User feedback → Update golden set → Re-run meta-evaluation → Adjust judge
```

Store all human feedback for future golden set expansion:

```yaml
human_feedback_record:
  evaluation_id: "eval_12345"
  automated_score: 4.2
  human_score: 3.5
  human_reasoning: "Judge missed that the date was incorrect"
  action_taken: "Added to golden set as edge case"
  rubric_updated: false
```

## Judge Improvement Strategies

When correlation is below threshold, consider:

### 1. Rubric Refinement
- Add more specific examples in the rubric
- Clarify ambiguous criteria
- Add behavioral anchors for each score level

### 2. Few-Shot Calibration
- Include golden set examples in judge prompt
- Show explicit examples of "this gets a 5", "this gets a 3", etc.

### 3. Model Upgrade
- Try a more capable judge model
- Use multi-judge panel for controversial cases

### 4. Dimension Decomposition
- Break overall score into specific dimensions
- Some dimensions may have better agreement

### 5. Hybrid Approach
- Use automated judge for clear cases
- Escalate ambiguous cases to humans

## Summary Checklist

Before deploying an LLM judge:

- [ ] Create golden set (50+ examples, expert-labeled)
- [ ] Run meta-evaluation
- [ ] Achieve correlation > 0.7
- [ ] Check calibration (no systematic bias)
- [ ] Analyze error patterns
- [ ] Set up drift monitoring
- [ ] Define escalation triggers
- [ ] Establish feedback collection process
