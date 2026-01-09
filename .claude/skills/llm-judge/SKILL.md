---
name: llm-judge
description: This skill should be used when the user asks to "evaluate AI output", "judge model response", "assess pipeline results", "compare model outputs", "check output quality", or needs to verify if LLM-generated work is correct.
---

# LLM Judge - AI Output Evaluation Skill

A context-aware evaluation skill that checks the quality of AI-generated outputs. It reads your chat session, understands what was built, proposes an evaluation approach, and delivers a clear verdict with reasoning.

## How It Works

```
┌─────────────────────────────────────────────────────────────────┐
│  1. READ CONTEXT (silent)                                       │
│     └─ What output was created? What was the task?              │
│     └─ What criteria matter? (stated or inferred)               │
├─────────────────────────────────────────────────────────────────┤
│  2. PROPOSE & CONFIRM (single question)                         │
│     └─ "I'll evaluate [X] for [criteria]."                      │
│     └─ "Do you have a golden set or reference examples?"        │
│     └─ Wait for confirmation                                    │
├─────────────────────────────────────────────────────────────────┤
│  3. EVALUATE                                                    │
│     └─ G-Eval with Chain-of-Thought reasoning                   │
│     └─ If factual claims → verify with web search               │
│     └─ If comparing two outputs → pairwise comparison           │
├─────────────────────────────────────────────────────────────────┤
│  4. REPORT                                                      │
│     └─ Clear verdict with score                                 │
│     └─ Reasoning (strengths and weaknesses)                     │
│     └─ Specific improvement suggestions                         │
└─────────────────────────────────────────────────────────────────┘
```

## The Proposal Step

After reading chat context, present ONE confirmation message:

```
Based on our session, I'll evaluate the [describe output] you created.

**What I'll check:**
- [Criterion 1 - e.g., correctness]
- [Criterion 2 - e.g., completeness]
- [Criterion 3 - e.g., code quality]

**Do you have a golden set or reference examples to calibrate against?**
(This could be expert-labeled examples, high-performing outputs, or reference answers)

Should I proceed, or would you like to adjust what I evaluate?
```

Then wait for user response before evaluating.

## Evaluation Method: G-Eval with Chain-of-Thought

The core evaluation uses structured reasoning before scoring:

```
STEP 1: Analyze Intent
└─ What was the user actually asking for?
└─ What are the implicit requirements?

STEP 2: Check Against Criteria
└─ For each criterion, assess the output
└─ Note specific strengths
└─ Note specific weaknesses

STEP 3: Verify Facts (if applicable)
└─ If output contains factual claims, verify key ones
└─ Use web search for external verification

STEP 4: Score & Verdict
└─ Assign score based on the analysis
└─ Provide clear reasoning
```

This Chain-of-Thought approach forces thorough analysis before judgment, achieving higher correlation with human evaluation than simple "rate 1-5" prompts.

## When to Use Different Approaches

| Situation | Approach |
|-----------|----------|
| **Standard evaluation** | G-Eval with CoT (default) |
| **Output contains facts/data** | G-Eval + verify key facts with web search |
| **Comparing two versions** | Pairwise comparison with swap-and-pool |
| **User wants high confidence** | Multi-judge panel (Claude + GPT + Gemini) |
| **User provides golden set** | Use examples for calibration in prompts |

The default is single-judge G-Eval. Multi-judge and other advanced methods are available on request.

## Using a Golden Set

If the user provides reference examples:

**Expert-labeled examples:** Include in the evaluation prompt as calibration anchors
```
"Here's an example that scored 5/5: [example]
Here's an example that scored 3/5: [example]
Now evaluate the candidate output..."
```

**High-performing outputs:** Use as quality benchmarks
```
"Compare the candidate to these proven high-performers..."
```

**Reference answers:** Use for accuracy comparison
```
"The reference answer covers: [X, Y, Z].
Does the candidate cover the same information?"
```

## Output Format

After evaluation, provide:

```
## Evaluation Result

**Score: [X/5]** — [One-line verdict]

### Strengths
- [Specific strength 1]
- [Specific strength 2]

### Weaknesses
- [Specific weakness 1]
- [Specific weakness 2]

### Suggestions for Improvement
1. [Actionable suggestion]
2. [Actionable suggestion]

### Reasoning
[2-3 sentences explaining the overall assessment]
```

## Bias Mitigation (Built-in)

These are applied automatically:

- **Verbosity penalty:** Longer ≠ better. Evaluate information coverage, not length.
- **Position bias (pairwise):** When comparing, run both orderings and check consistency.
- **Reference anchoring:** When golden set provided, use it to calibrate scoring.

## Advanced Options (On Request)

These are available if the user asks:

| Option | Trigger phrases |
|--------|-----------------|
| **Multi-judge panel** | "use multiple judges", "get different perspectives", "high confidence evaluation" |
| **Self-consistency voting** | "make sure you're confident", "verify your assessment" |
| **SAFE fact-checking** | "verify all the facts", "full fact-check" |
| **Pairwise comparison** | "compare these two", "which is better" |

## Example Interaction

```
User: [After building a Python function]
      /llm-judge

Skill: Based on our session, I'll evaluate the `parse_config()`
       function you created.

       **What I'll check:**
       - Correctness (handles the YAML format correctly)
       - Edge cases (empty files, malformed input)
       - Code quality (readability, error handling)

       **Do you have a golden set or reference examples to
       calibrate against?**

       Should I proceed?

User: Yes, no golden set

Skill: [Runs G-Eval with CoT]

       ## Evaluation Result

       **Score: 4.2/5** — Solid implementation with minor gaps

       ### Strengths
       - Correctly parses standard YAML structures
       - Good use of type hints
       - Clear variable naming

       ### Weaknesses
       - No handling for FileNotFoundError
       - Missing docstring

       ### Suggestions for Improvement
       1. Add try/except for file operations
       2. Add docstring explaining parameters and return value

       ### Reasoning
       The function correctly implements the core requirement and
       follows Python conventions. The missing error handling is
       the main gap - in production, file operations should always
       handle potential exceptions.
```

## Reference Documentation

For deeper understanding of the methodologies:

- `references/frameworks.md` — G-Eval, Pointwise, Pairwise explained
- `references/bias-mitigation.md` — How biases are handled
- `references/safe-framework.md` — Search-augmented fact-checking
- `references/meta-evaluation.md` — Validating judge accuracy

## Scripts

- `scripts/evaluate.py` — Core evaluation logic
- `scripts/safe_factcheck.py` — SAFE framework for fact verification
