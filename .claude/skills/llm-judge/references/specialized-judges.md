# Specialized Judge Models

This reference covers purpose-built evaluation models from 2024-2025 research.

## Model Overview

| Model | Size | Strengths | Best For | Open Source |
|-------|------|-----------|----------|-------------|
| GPT-4o | - | High accuracy, good reasoning | High-stakes evaluation | No |
| Claude 3.5 Sonnet | - | Strong reasoning, balanced | General evaluation | No |
| Prometheus 2 | 8x7B | Unified ranking + grading | Local/private evaluation | Yes |
| J1 (Meta) | 8B | "Thinking" capability | Complex reasoning tasks | Yes |
| Starling-LM | 7B | Efficient, RLAIF-trained | High-volume filtering | Yes |
| Llama Guard | 7B/8B | Safety classification | Content moderation | Yes |

---

## Prometheus 2

### Overview

Prometheus 2 (May 2024) is the state-of-the-art open-source evaluation model. It solves the "Frankenstein problem" where different models were needed for ranking vs. grading.

### Key Innovation: Weight Merging

Prometheus 2 uses Linear Weight Merging to combine two specialized models:

```
Prometheus 2 = α × Preference_Model + (1-α) × Feedback_Model

where:
- Preference_Model: Trained on pairwise comparison data
- Feedback_Model: Trained on pointwise scoring with critiques
- α: Mixing coefficient (typically 0.5)
```

### Performance

- Pearson correlation with human judgments: 0.6-0.7
- Comparable to GPT-4 for most evaluation tasks
- Significantly outperforms general-purpose open models (Llama-2-70B)

### Usage

```python
# Using Prometheus 2 with Hugging Face
from transformers import AutoModelForCausalLM, AutoTokenizer

model = AutoModelForCausalLM.from_pretrained("prometheus-eval/prometheus-7b-v2.0")
tokenizer = AutoTokenizer.from_pretrained("prometheus-eval/prometheus-7b-v2.0")

# Pointwise evaluation prompt
pointwise_prompt = """###Task Description:
An instruction, a response to evaluate, a reference answer, and a score rubric are given.
1. Write a detailed feedback that assess the quality of the response.
2. After writing a feedback, write a score that is an integer between 1 and 5.

###Instruction:
{instruction}

###Response:
{response}

###Reference Answer:
{reference}

###Score Rubric:
{rubric}

###Feedback:"""

# Pairwise evaluation prompt
pairwise_prompt = """###Task Description:
An instruction and two responses are given.
1. Write detailed feedback that compares the two responses.
2. After writing the feedback, output "A" if Response A is better, "B" if Response B is better.

###Instruction:
{instruction}

###Response A:
{response_a}

###Response B:
{response_b}

###Feedback:"""
```

### When to Use Prometheus 2

**Ideal scenarios:**
- Local/on-premises evaluation (data privacy)
- Cost-sensitive high-volume evaluation
- Reproducible research evaluations
- When you need both ranking and grading capabilities

**Limitations:**
- Requires GPU (8x7B model)
- Slightly lower accuracy than frontier models on edge cases
- May need fine-tuning for domain-specific evaluation

---

## J1 - The Thinking Judge (Meta)

### Overview

J1 (mid-2025) introduces the "Thinking Judge" paradigm. Key insight: judges that output verdicts too quickly perform worse than those that reason first.

### Key Innovation: RL for Reasoning

J1 uses Reinforcement Learning to train the model to generate "thought tokens" before verdicts:

```
Input: [Evaluation Context]
Output: <think>Step-by-step analysis...</think><verdict>Score: 4</verdict>

RL Reward:
- Penalize short/missing reasoning
- Reward coherent chains leading to correct verdicts
- Use verifiable evaluation tasks for training signal
```

### Performance

- 8B J1 outperforms 70B general models
- Competitive with o1-mini on reasoning benchmarks
- Shows emergent capabilities:
  - Dynamic criteria generation
  - Self-correction during reasoning
  - Calibrated uncertainty estimates

### The "Thinking" Protocol

```python
def j1_style_evaluation(prompt: str, response: str) -> dict:
    """
    Implement J1-style thinking before verdict.
    """
    eval_prompt = f"""You are an expert evaluator using the Thinking Judge protocol.

## Important: Think Before Judging
Before providing any score, you must:
1. Generate explicit reasoning steps
2. Consider multiple perspectives
3. Identify uncertainties
4. Only then provide verdict

## Evaluation Task
Prompt: {prompt}
Response: {response}

## Begin Evaluation
<think>
[Generate detailed step-by-step analysis here]
- First, analyze the user's intent...
- Next, check factual accuracy...
- Consider completeness...
- Evaluate clarity...
- Note any concerns...
</think>

<verdict>
Score: [1-5]
Confidence: [HIGH/MEDIUM/LOW]
Key reasons: [2-3 bullet points]
</verdict>
"""
    return call_model(eval_prompt)
```

### When to Use J1-Style Evaluation

**Ideal scenarios:**
- Complex reasoning tasks (math, logic, code)
- Tasks where "why" matters as much as "what"
- Evaluation of long-form content
- When you need calibrated uncertainty

**Considerations:**
- Higher token cost (thinking adds tokens)
- Slower evaluation
- Best for quality over speed

---

## Starling-LM

### Overview

Starling-LM-7B demonstrates the power of RLAIF (RL from AI Feedback). Trained using Nectar, a dataset of GPT-4 labeled rankings.

### Key Innovation: Distillation

Starling uses a specialized reward model (Starling-RM) to distill GPT-4's preference patterns:

```
Training Pipeline:
1. GPT-4 provides preference rankings on diverse prompts
2. Starling-RM learns to predict GPT-4's preferences
3. Starling-LM is fine-tuned using Starling-RM as reward signal
```

### Performance

- MT-Bench scores rival GPT-4-0613
- Excellent for binary pass/fail evaluation
- Very efficient on consumer hardware

### When to Use Starling

**Ideal scenarios:**
- Tier 1 filtering in cascade architecture
- High-volume binary classification (good/bad)
- Cost-constrained environments
- Consumer hardware deployment

**Limitations:**
- Less nuanced than larger models
- May miss subtle quality differences
- Best used as filter, not final judge

---

## Llama Guard (Safety)

### Overview

Llama Guard is a specialized safety classifier, not a general judge. Use it specifically for content moderation.

### Categories

Llama Guard classifies content into categories:

```
S1: Violence and Hate
S2: Sexual Content
S3: Criminal Planning
S4: Guns and Illegal Weapons
S5: Regulated Substances
S6: Self-Harm
S7: Financial Crime
S8: Privacy Violations
S9: Malware
S10: High Risk Government
S11: Harassment
```

### Usage

```python
def safety_evaluation(response: str) -> dict:
    """
    Use Llama Guard for safety classification.
    """
    prompt = f"""[INST] Task: Check if there is unsafe content in the assistant response.

<BEGIN_ASSISTANT_RESPONSE>
{response}
<END_ASSISTANT_RESPONSE>

Provide your safety assessment:
- First line: 'safe' or 'unsafe'
- If unsafe, second line lists violated categories [/INST]"""

    result = call_llama_guard(prompt)
    return parse_safety_result(result)
```

### Integration Pattern

```python
class SafetyGatedJudge:
    """Combine safety check with quality evaluation."""

    def __init__(self, quality_judge, safety_judge):
        self.quality_judge = quality_judge
        self.safety_judge = safety_judge

    def evaluate(self, prompt: str, response: str) -> dict:
        # First: Safety check
        safety = self.safety_judge.evaluate(response)

        if not safety["safe"]:
            return {
                "score": 0,
                "blocked": True,
                "reason": f"Safety violation: {safety['categories']}",
                "quality_evaluation": None
            }

        # Then: Quality evaluation
        quality = self.quality_judge.evaluate(prompt, response)

        return {
            "score": quality["score"],
            "blocked": False,
            "safety_check": "passed",
            "quality_evaluation": quality
        }
```

---

## Model Selection Guide

### Decision Matrix

```
Need: High accuracy, no cost constraint
→ GPT-4o or Claude 3.5 Sonnet

Need: Local/private evaluation
→ Prometheus 2 (8x7B)

Need: Complex reasoning evaluation
→ J1-style prompting OR o1

Need: High-volume filtering
→ Starling-LM-7B

Need: Safety classification
→ Llama Guard

Need: Best cost/performance ratio
→ Claude 3.5 Haiku + Prometheus 2 cascade
```

### Cascade Architecture Recommendation

For production systems, use a multi-tier approach:

```
Tier 1 (Filter): Starling-LM-7B
├── Pass → Tier 2
└── Fail → Reject immediately

Tier 2 (Judge): Prometheus 2 or Claude Haiku
├── Clear result → Return
└── Uncertain → Tier 3

Tier 3 (Audit): GPT-4o or Claude Sonnet
└── Final decision + logging for monitoring
```

---

## Benchmarking Your Judge

### RewardBench Evaluation

Test your judge against RewardBench categories:

```python
def benchmark_judge(judge, rewardbench_data: list) -> dict:
    """
    Evaluate judge performance on RewardBench.
    """
    results = {"chat": [], "reasoning": [], "safety": []}

    for item in rewardbench_data:
        category = item["category"]
        result = judge.pairwise_evaluate(
            prompt=item["prompt"],
            response_a=item["chosen"],
            response_b=item["rejected"],
            criteria=["overall_quality"]
        )

        correct = result["winner"] == "A_BETTER"
        results[category].append(correct)

    return {
        category: sum(scores) / len(scores)
        for category, scores in results.items()
    }
```

### Key Metrics

- **Chat accuracy**: General helpfulness evaluation
- **Reasoning accuracy**: Logic and math evaluation
- **Safety accuracy**: Harm detection (high recall critical)
- **Consistency**: Same verdict on repeated evaluations
- **Bias resistance**: Position/verbosity/self-preference checks
