# Integration Patterns for LLM Judge

This reference provides patterns for integrating LLM-as-a-Judge into various workflows.

## Pattern 1: CI/CD Quality Gate

Integrate evaluation into your CI/CD pipeline to catch quality regressions.

```python
# ci_quality_gate.py
import json
import sys
from pathlib import Path

# Add skill scripts to path
sys.path.insert(0, str(Path.home() / ".claude/skills/llm-judge/scripts"))
from evaluate import LLMJudge

def run_quality_gate(
    test_cases_path: str,
    rubric_path: str,
    threshold: float = 3.5,
    fail_on_below: bool = True
) -> dict:
    """
    Run quality gate on a set of test cases.

    Args:
        test_cases_path: Path to JSON file with test cases
        rubric_path: Path to evaluation rubric
        threshold: Minimum acceptable score
        fail_on_below: If True, exit with error code on failure

    Returns:
        Summary of evaluation results
    """
    judge = LLMJudge()
    rubric = judge.load_rubric(rubric_path)

    with open(test_cases_path) as f:
        test_cases = json.load(f)

    results = []
    failures = []

    for i, case in enumerate(test_cases):
        result = judge.pointwise_evaluate(
            prompt=case["prompt"],
            response=case["response"],
            rubric=rubric,
            reference=case.get("reference")
        )

        results.append({
            "case_id": case.get("id", i),
            "score": result.score,
            "passed": result.score >= threshold,
            "dimensions": result.scores_by_dimension
        })

        if result.score < threshold:
            failures.append({
                "case_id": case.get("id", i),
                "score": result.score,
                "reasoning": result.reasoning
            })

    summary = {
        "total_cases": len(test_cases),
        "passed": sum(1 for r in results if r["passed"]),
        "failed": len(failures),
        "average_score": sum(r["score"] for r in results) / len(results),
        "threshold": threshold,
        "failures": failures
    }

    # Print summary
    print(f"\n{'='*50}")
    print(f"Quality Gate Results")
    print(f"{'='*50}")
    print(f"Total: {summary['total_cases']}")
    print(f"Passed: {summary['passed']}")
    print(f"Failed: {summary['failed']}")
    print(f"Average Score: {summary['average_score']:.2f}")
    print(f"Threshold: {threshold}")

    if failures and fail_on_below:
        print(f"\n❌ Quality gate FAILED")
        for f in failures:
            print(f"  - Case {f['case_id']}: {f['score']:.2f} (below {threshold})")
        sys.exit(1)
    else:
        print(f"\n✅ Quality gate PASSED")

    return summary


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--test-cases", required=True)
    parser.add_argument("--rubric", required=True)
    parser.add_argument("--threshold", type=float, default=3.5)
    args = parser.parse_args()

    run_quality_gate(args.test_cases, args.rubric, args.threshold)
```

### GitHub Actions Integration

```yaml
# .github/workflows/quality-gate.yml
name: LLM Quality Gate

on:
  pull_request:
    paths:
      - 'prompts/**'
      - 'pipelines/**'

jobs:
  evaluate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          pip install anthropic pyyaml

      - name: Run quality gate
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
        run: |
          python ci_quality_gate.py \
            --test-cases tests/evaluation_cases.json \
            --rubric rubrics/general_quality.yaml \
            --threshold 3.5
```

---

## Pattern 2: A/B Testing Pipeline

Compare two model versions to determine which performs better.

```python
# ab_test_models.py
import json
from dataclasses import dataclass
from typing import List, Tuple

from evaluate import LLMJudge, EvaluationResult


@dataclass
class ABTestResult:
    model_a_name: str
    model_b_name: str
    model_a_wins: int
    model_b_wins: int
    ties: int
    total_comparisons: int
    position_bias_cases: int
    winner: str
    confidence: str

    @property
    def win_rate_a(self) -> float:
        return self.model_a_wins / self.total_comparisons

    @property
    def win_rate_b(self) -> float:
        return self.model_b_wins / self.total_comparisons


def run_ab_test(
    model_a_outputs: List[dict],
    model_b_outputs: List[dict],
    model_a_name: str = "Model A",
    model_b_name: str = "Model B",
    criteria: List[str] = None
) -> ABTestResult:
    """
    Run A/B test between two model versions.

    Each output dict should have: {"prompt": str, "response": str}
    """
    if len(model_a_outputs) != len(model_b_outputs):
        raise ValueError("Must have same number of outputs from each model")

    judge = LLMJudge()
    criteria = criteria or ["accuracy", "completeness", "clarity", "helpfulness"]

    a_wins = 0
    b_wins = 0
    ties = 0
    bias_cases = 0

    for a_out, b_out in zip(model_a_outputs, model_b_outputs):
        if a_out["prompt"] != b_out["prompt"]:
            raise ValueError("Prompts must match between model outputs")

        result = judge.pairwise_evaluate(
            prompt=a_out["prompt"],
            response_a=a_out["response"],
            response_b=b_out["response"],
            criteria=criteria,
            use_swap_and_pool=True
        )

        if result.winner == "A_BETTER":
            a_wins += 1
        elif result.winner == "B_BETTER":
            b_wins += 1
        else:
            ties += 1

        if result.metadata and result.metadata.get("position_bias_detected"):
            bias_cases += 1

    # Determine overall winner
    total = len(model_a_outputs)
    if a_wins > b_wins + total * 0.1:  # >10% margin
        winner = model_a_name
        confidence = "HIGH" if a_wins > b_wins + total * 0.2 else "MEDIUM"
    elif b_wins > a_wins + total * 0.1:
        winner = model_b_name
        confidence = "HIGH" if b_wins > a_wins + total * 0.2 else "MEDIUM"
    else:
        winner = "TIE"
        confidence = "LOW"

    return ABTestResult(
        model_a_name=model_a_name,
        model_b_name=model_b_name,
        model_a_wins=a_wins,
        model_b_wins=b_wins,
        ties=ties,
        total_comparisons=total,
        position_bias_cases=bias_cases,
        winner=winner,
        confidence=confidence
    )


def print_ab_results(result: ABTestResult):
    """Pretty print A/B test results."""
    print(f"\n{'='*60}")
    print(f"A/B Test Results: {result.model_a_name} vs {result.model_b_name}")
    print(f"{'='*60}")
    print(f"Total Comparisons: {result.total_comparisons}")
    print(f"\n{result.model_a_name}: {result.model_a_wins} wins ({result.win_rate_a:.1%})")
    print(f"{result.model_b_name}: {result.model_b_wins} wins ({result.win_rate_b:.1%})")
    print(f"Ties: {result.ties}")
    print(f"\nPosition bias detected in {result.position_bias_cases} comparisons")
    print(f"\n🏆 Winner: {result.winner} (Confidence: {result.confidence})")
```

---

## Pattern 3: Continuous Monitoring Dashboard

Log evaluations for trend analysis and anomaly detection.

```python
# monitoring.py
import json
import hashlib
from datetime import datetime
from pathlib import Path
from typing import Optional


class EvaluationLogger:
    """Log evaluations for monitoring and analysis."""

    def __init__(self, log_dir: str = "evaluation_logs"):
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)

    def log_evaluation(
        self,
        prompt: str,
        response: str,
        result: dict,
        model_version: str,
        pipeline_name: str,
        metadata: Optional[dict] = None
    ):
        """Log a single evaluation result."""
        timestamp = datetime.utcnow().isoformat()
        prompt_hash = hashlib.md5(prompt.encode()).hexdigest()[:8]
        response_hash = hashlib.md5(response.encode()).hexdigest()[:8]

        log_entry = {
            "timestamp": timestamp,
            "pipeline": pipeline_name,
            "model_version": model_version,
            "prompt_hash": prompt_hash,
            "response_hash": response_hash,
            "score": result.get("score"),
            "scores_by_dimension": result.get("scores_by_dimension"),
            "confidence": result.get("confidence"),
            "metadata": metadata or {}
        }

        # Append to daily log file
        date_str = datetime.utcnow().strftime("%Y-%m-%d")
        log_file = self.log_dir / f"{pipeline_name}_{date_str}.jsonl"

        with open(log_file, "a") as f:
            f.write(json.dumps(log_entry) + "\n")

        return log_entry

    def get_daily_summary(self, pipeline_name: str, date: str) -> dict:
        """Get summary statistics for a day."""
        log_file = self.log_dir / f"{pipeline_name}_{date}.jsonl"
        if not log_file.exists():
            return {"error": "No logs found for this date"}

        scores = []
        dimension_scores = {}

        with open(log_file) as f:
            for line in f:
                entry = json.loads(line)
                if entry.get("score"):
                    scores.append(entry["score"])
                for dim, score in (entry.get("scores_by_dimension") or {}).items():
                    dimension_scores.setdefault(dim, []).append(score)

        return {
            "date": date,
            "pipeline": pipeline_name,
            "total_evaluations": len(scores),
            "average_score": sum(scores) / len(scores) if scores else 0,
            "min_score": min(scores) if scores else 0,
            "max_score": max(scores) if scores else 0,
            "dimension_averages": {
                dim: sum(s) / len(s) for dim, s in dimension_scores.items()
            }
        }

    def detect_anomalies(
        self,
        pipeline_name: str,
        lookback_days: int = 7,
        threshold_std: float = 2.0
    ) -> list:
        """Detect anomalous scores based on historical data."""
        from datetime import timedelta
        import statistics

        today = datetime.utcnow().date()
        historical_scores = []

        # Collect historical data
        for i in range(1, lookback_days + 1):
            date = (today - timedelta(days=i)).strftime("%Y-%m-%d")
            summary = self.get_daily_summary(pipeline_name, date)
            if "average_score" in summary:
                historical_scores.append(summary["average_score"])

        if len(historical_scores) < 3:
            return []  # Not enough data

        mean = statistics.mean(historical_scores)
        std = statistics.stdev(historical_scores)

        # Check today's scores
        today_summary = self.get_daily_summary(
            pipeline_name, today.strftime("%Y-%m-%d")
        )
        today_avg = today_summary.get("average_score", mean)

        anomalies = []
        if abs(today_avg - mean) > threshold_std * std:
            direction = "drop" if today_avg < mean else "spike"
            anomalies.append({
                "type": f"score_{direction}",
                "today_average": today_avg,
                "historical_mean": mean,
                "deviation_std": (today_avg - mean) / std,
                "message": f"Score {direction} detected: {today_avg:.2f} vs historical mean {mean:.2f}"
            })

        return anomalies
```

### Usage Example

```python
from evaluate import LLMJudge
from monitoring import EvaluationLogger

judge = LLMJudge()
logger = EvaluationLogger()

# After each pipeline run
result = judge.pointwise_evaluate(prompt, response, rubric)

logger.log_evaluation(
    prompt=prompt,
    response=response,
    result=result.to_dict(),
    model_version="v1.2.3",
    pipeline_name="customer_support_bot"
)

# Daily check
anomalies = logger.detect_anomalies("customer_support_bot")
if anomalies:
    send_alert(anomalies)
```

---

## Pattern 4: RAG Pipeline Evaluation

Specialized evaluation for Retrieval-Augmented Generation.

```python
# rag_evaluation.py
from evaluate import LLMJudge


class RAGEvaluator:
    """Specialized evaluator for RAG pipelines."""

    def __init__(self):
        self.judge = LLMJudge()

    def evaluate_faithfulness(
        self,
        question: str,
        answer: str,
        context_chunks: list[str]
    ) -> dict:
        """
        Evaluate if answer is faithful to retrieved context.
        Based on Ragas methodology.
        """
        context = "\n\n---\n\n".join(context_chunks)

        eval_prompt = f"""Evaluate the faithfulness of this answer to the provided context.

## Retrieved Context
{context}

## Question
{question}

## Generated Answer
{answer}

## Instructions
1. Extract all factual claims from the answer
2. For each claim, determine if it can be inferred from the context
3. Calculate the faithfulness score

Output format:
CLAIMS:
- [Claim 1]: [SUPPORTED | NOT_SUPPORTED]
- [Claim 2]: [SUPPORTED | NOT_SUPPORTED]
...

SUPPORTED_COUNT: [number]
TOTAL_CLAIMS: [number]
FAITHFULNESS_SCORE: [supported / total, as decimal]
REASONING: [Brief explanation]
"""

        result = self.judge._call_model(eval_prompt)
        return self._parse_faithfulness(result)

    def evaluate_answer_relevancy(
        self,
        question: str,
        answer: str
    ) -> dict:
        """
        Evaluate if answer is relevant to the question.
        Uses reverse question generation approach.
        """
        eval_prompt = f"""Evaluate the relevancy of this answer to the question.

## Question
{question}

## Answer
{answer}

## Instructions
1. Generate 3 questions that this answer would be a good response to
2. Compare those questions to the original question
3. Rate the semantic similarity

Output format:
GENERATED_QUESTIONS:
1. [Question that this answer addresses]
2. [Question that this answer addresses]
3. [Question that this answer addresses]

SIMILARITY_ASSESSMENT:
- Q1 similarity to original: [HIGH | MEDIUM | LOW]
- Q2 similarity to original: [HIGH | MEDIUM | LOW]
- Q3 similarity to original: [HIGH | MEDIUM | LOW]

RELEVANCY_SCORE: [1-5]
REASONING: [Brief explanation]
"""

        result = self.judge._call_model(eval_prompt)
        return self._parse_relevancy(result)

    def evaluate_context_relevancy(
        self,
        question: str,
        context_chunks: list[str]
    ) -> dict:
        """
        Evaluate if retrieved context is relevant to the question.
        """
        results = []
        for i, chunk in enumerate(context_chunks):
            eval_prompt = f"""Rate the relevancy of this context chunk to the question.

## Question
{question}

## Context Chunk {i+1}
{chunk}

## Instructions
Rate how useful this chunk is for answering the question.

Output format:
RELEVANCY: [1-5]
USEFUL_CONTENT: [Brief description of what's useful, or "Nothing relevant"]
"""
            result = self.judge._call_model(eval_prompt)
            results.append(self._parse_chunk_relevancy(result, i))

        avg_relevancy = sum(r["relevancy"] for r in results) / len(results)
        return {
            "chunk_results": results,
            "average_relevancy": avg_relevancy,
            "relevant_chunks": sum(1 for r in results if r["relevancy"] >= 3),
            "total_chunks": len(context_chunks)
        }

    def full_rag_evaluation(
        self,
        question: str,
        answer: str,
        context_chunks: list[str]
    ) -> dict:
        """Run complete RAG evaluation."""
        faithfulness = self.evaluate_faithfulness(question, answer, context_chunks)
        relevancy = self.evaluate_answer_relevancy(question, answer)
        context_rel = self.evaluate_context_relevancy(question, context_chunks)

        # Composite score
        composite = (
            faithfulness.get("score", 0) * 0.4 +
            relevancy.get("score", 0) / 5 * 0.35 +
            context_rel.get("average_relevancy", 0) / 5 * 0.25
        )

        return {
            "faithfulness": faithfulness,
            "answer_relevancy": relevancy,
            "context_relevancy": context_rel,
            "composite_score": composite,
            "pass": composite >= 0.7
        }

    def _parse_faithfulness(self, raw: str) -> dict:
        # Parse faithfulness response
        score = 0.5  # default
        for line in raw.split("\n"):
            if line.strip().startswith("FAITHFULNESS_SCORE:"):
                try:
                    score = float(line.split(":")[-1].strip())
                except:
                    pass
        return {"score": score, "raw": raw}

    def _parse_relevancy(self, raw: str) -> dict:
        score = 3  # default
        for line in raw.split("\n"):
            if line.strip().startswith("RELEVANCY_SCORE:"):
                try:
                    score = int(line.split(":")[-1].strip())
                except:
                    pass
        return {"score": score, "raw": raw}

    def _parse_chunk_relevancy(self, raw: str, chunk_idx: int) -> dict:
        relevancy = 3
        for line in raw.split("\n"):
            if line.strip().startswith("RELEVANCY:"):
                try:
                    relevancy = int(line.split(":")[-1].strip())
                except:
                    pass
        return {"chunk_index": chunk_idx, "relevancy": relevancy}
```

---

## Pattern 5: Advisor Mode - Implementation Guidance

When using the skill in advisor mode to help implement evaluation in a project.

### Step 1: Analyze the Pipeline

```python
# advisor_analyze.py
"""
Analysis workflow for advising on evaluation implementation.
"""

def analyze_pipeline_for_evaluation(project_path: str) -> dict:
    """
    Analyze a project to recommend evaluation strategy.

    Returns recommendations for:
    - Evaluation framework (pointwise/pairwise/g-eval)
    - Rubric dimensions
    - Integration points
    """
    # This would be called by Claude when analyzing a project
    recommendations = {
        "analysis": {},
        "recommended_framework": "",
        "recommended_rubric": {},
        "integration_points": []
    }

    # Analyze output types
    # - Text generation -> general_quality rubric
    # - Code generation -> code_generation rubric
    # - RAG pipeline -> rag_pipeline rubric
    # - Chat/conversation -> conversation rubric

    # Analyze volume
    # - High volume (>1000/day) -> Cascade architecture
    # - Medium volume -> Direct evaluation
    # - Low volume -> Full G-Eval

    # Analyze comparison needs
    # - Model selection -> Pairwise
    # - Quality gate -> Pointwise
    # - Fine-grained analysis -> G-Eval

    return recommendations
```

### Advisor Prompt Template

When advising on implementation, use this structure:

```markdown
## Analysis of Your Pipeline

Based on my analysis of [project name]:

### Output Type
- [Text/Code/RAG/Chat] generation
- Typical output length: [short/medium/long]
- Quality dimensions that matter: [list]

### Recommended Evaluation Strategy

**Framework**: [Pointwise/Pairwise/G-Eval/Hybrid]
**Reasoning**: [Why this framework fits]

### Rubric Recommendations

For your use case, I recommend evaluating these dimensions:
1. **[Dimension]** (weight: X) - [Why important]
2. **[Dimension]** (weight: X) - [Why important]

### Integration Points

1. **[Where in workflow]**: [What to evaluate and why]
2. **[CI/CD step]**: [Quality gate configuration]

### Implementation Steps

1. [ ] Create rubric file at `rubrics/[name].yaml`
2. [ ] Add evaluation hook at [location]
3. [ ] Set up logging with [monitoring pattern]
4. [ ] Configure alerts for [anomaly types]

### Example Evaluation Call

```python
from llm_judge import LLMJudge

judge = LLMJudge()
result = judge.[method](
    prompt=...,
    response=...,
    rubric=...
)
```
```

---

## Quick Reference: Which Pattern to Use

| Scenario | Pattern |
|----------|---------|
| PR/deployment quality gate | Pattern 1: CI/CD |
| Comparing model versions | Pattern 2: A/B Testing |
| Production monitoring | Pattern 3: Continuous Monitoring |
| RAG pipeline quality | Pattern 4: RAG Evaluation |
| "How should I implement evaluation?" | Pattern 5: Advisor Mode |
