# Reasoning Techniques

Advanced prompting techniques for improving LLM reasoning capabilities.

## Chain-of-Thought (CoT) Prompting

**Source:** [Google Research, 2022](https://arxiv.org/abs/2201.11903)

Chain-of-Thought prompting guides models through step-by-step reasoning, significantly improving performance on math, logic, and multi-step problems.

### Zero-Shot CoT

Simply add "Let's think step by step":

```
Q: A store has 50 apples. They sell 23 and receive 15 more. How many apples?

Let's think step by step.
```

This outperforms other zero-shot methods for reasoning tasks.

### Few-Shot CoT

Provide examples with reasoning chains:

```
Q: Roger has 5 tennis balls. He buys 2 cans of 3 balls each. How many balls?
A: Roger started with 5 balls. 2 cans of 3 balls = 6 balls. 5 + 6 = 11 balls.

Q: A cafeteria had 23 apples. They used 20 for lunch and bought 6 more. How many?
A: Started with 23. Used 20, so 23 - 20 = 3. Bought 6, so 3 + 6 = 9 apples.

Q: [Your question]
A:
```

### When to Use CoT

| Good For | Not Ideal For |
|----------|---------------|
| Math problems | Simple factual recall |
| Logic puzzles | Creative writing |
| Multi-step planning | Subjective opinions |
| Code debugging | Classification tasks |

### Implementation

```python
# Zero-shot CoT
prompt = f"{question}\n\nLet's think step by step."

# Few-shot CoT
prompt = f"""
{example_1_with_reasoning}

{example_2_with_reasoning}

Q: {question}
A: Let me work through this step by step.
"""
```

---

## Self-Consistency

**Source:** [Wang et al., 2022](https://arxiv.org/abs/2203.11171)

Self-Consistency improves CoT by generating multiple reasoning paths and selecting the most common answer.

### How It Works

1. Generate N different reasoning chains (with temperature > 0)
2. Extract the final answer from each chain
3. Take the majority vote

### Performance Improvements

| Benchmark | Improvement |
|-----------|-------------|
| GSM8K | +17.9% |
| SVAMP | +11.0% |
| AQuA | +12.2% |
| LaMDA 137B | +23% |

### Implementation

```python
def self_consistency(question, n_samples=5):
    answers = []

    for _ in range(n_samples):
        response = llm(
            prompt=f"{question}\nLet's think step by step.",
            temperature=0.7  # Higher temp for diversity
        )
        answer = extract_final_answer(response)
        answers.append(answer)

    # Return most common answer
    return max(set(answers), key=answers.count)
```

### When to Use

- Problems with a single correct answer
- Math and logic problems
- When you need higher confidence
- When cost/latency is acceptable (requires multiple calls)

---

## Tree of Thoughts (ToT)

**Source:** [Yao et al., 2023](https://arxiv.org/abs/2305.10601)

Tree of Thoughts extends CoT by exploring multiple reasoning branches, with the ability to evaluate and backtrack.

### How It Works

1. Break problem into intermediate "thoughts"
2. Generate multiple candidate thoughts at each step
3. Evaluate which thoughts are promising
4. Search (BFS or DFS) through the thought tree
5. Backtrack from unpromising branches

### Conceptual Structure

```
Problem
├── Thought A (promising)
│   ├── Thought A1 (dead end)
│   └── Thought A2 (solution!)
├── Thought B (unpromising, abandoned)
└── Thought C (promising)
    └── Thought C1 (exploring...)
```

### Implementation Pattern

```python
def tree_of_thoughts(problem, breadth=3, depth=3):
    thoughts = [{"state": problem, "path": []}]

    for _ in range(depth):
        candidates = []

        for thought in thoughts:
            # Generate candidate next steps
            next_steps = llm(
                f"Given: {thought['state']}\n"
                f"Generate {breadth} possible next steps:"
            )

            for step in parse_steps(next_steps):
                # Evaluate each step
                score = llm(
                    f"Rate this reasoning step 1-10:\n{step}"
                )
                candidates.append({
                    "state": step,
                    "path": thought["path"] + [step],
                    "score": score
                })

        # Keep top candidates
        thoughts = sorted(candidates, key=lambda x: x["score"])[:breadth]

    return thoughts[0]["path"]  # Best solution path
```

### When to Use

| Ideal For | Not Ideal For |
|-----------|---------------|
| Complex planning | Simple questions |
| Creative problem solving | Time-sensitive tasks |
| Game playing (e.g., 24 game) | Straightforward reasoning |
| Multi-step puzzles | Cost-sensitive applications |

### Simplified Prompt-Only Version

```
Problem: [Your problem]

Generate 3 different approaches to solve this.
For each approach, rate its promise on a scale of 1-10.
Then develop the most promising approach further.
If you reach a dead end, backtrack and try another approach.
```

---

## Comparison Table

| Technique | Complexity | Cost | Best For |
|-----------|------------|------|----------|
| Zero-shot CoT | Low | 1x | Quick reasoning boost |
| Few-shot CoT | Medium | 1x | Consistent format |
| Self-Consistency | Medium | Nx | High-stakes accuracy |
| Tree of Thoughts | High | Many x | Complex exploration |

## Combining Techniques

You can combine these techniques:

```python
def robust_reasoning(problem):
    # Use ToT for exploration
    candidate_solutions = tree_of_thoughts(problem, breadth=3, depth=2)

    # Use self-consistency to verify
    final_answers = []
    for solution in candidate_solutions:
        # CoT for each solution
        answer = chain_of_thought(solution)
        final_answers.append(answer)

    # Majority vote
    return most_common(final_answers)
```

## Model-Specific Notes

### GPT-5.2
- Has built-in `reasoning.effort` parameter
- Use `effort: high` instead of explicit CoT for complex tasks

### Gemini 3
- Has `thinking_level` parameter
- Keep temperature at 1.0 even for reasoning

### Claude 4.5
- Extended thinking provides native reasoning
- Use "consider" instead of "think" when thinking is disabled

## Sources

- [Chain-of-Thought Prompting](https://www.promptingguide.ai/techniques/cot)
- [Self-Consistency](https://www.promptingguide.ai/techniques/consistency)
- [Tree of Thoughts](https://www.promptingguide.ai/techniques/tot)
- [IBM: Chain of Thought](https://www.ibm.com/think/topics/chain-of-thoughts)
