# GPT-5.2 Prompting Guide

GPT-5.2 (released December 2025) is designed for enterprise and agentic workloads, delivering higher accuracy, stronger instruction following, and more disciplined execution compared to GPT-5.1.

## Key Characteristics

1. **More deliberate scaffolding** - Better structured responses
2. **Lower verbosity** - Concise by default
3. **Stronger instruction adherence** - Improved formatting compliance
4. **Token efficient** - Cleaner output, less waste
5. **Prompt-sensitive** - Responds well to tone/style guidance

## Reasoning Effort Levels

GPT-5.2 supports different reasoning modes:

```python
response = client.responses.create(
    model="gpt-5.2",
    reasoning={"effort": "medium"},  # none, low, medium, high, xhigh (Pro only)
    input="Your prompt here"
)
```

| Effort | Use Case | Cost Impact |
|--------|----------|-------------|
| `none` | Simple tasks, low latency | Lowest |
| `low` | Standard queries | Low |
| `medium` | Default, balanced | Medium |
| `high` | Complex reasoning | Higher |
| `xhigh` | Pro only, maximum quality | Highest |

### Migration from Previous Models

| From Model | Recommended Effort |
|------------|-------------------|
| GPT-4o / GPT-4.1 | `none` |
| GPT-5 / GPT-5.1 | Keep existing, but change `minimal` → `none` |

## Critical Prompting Patterns

### 1. Verbosity Control

GPT-5.2 is concise by default. For detailed responses, be explicit:

```
# For complex tasks with structure:
Provide your analysis in this format:
1. One short overview paragraph
2. Up to 5 bullets tagged as:
   - What changed
   - Where
   - Risks
   - Next steps
```

### 2. Scope Discipline

Prevent feature creep by being explicit:

```
Implement EXACTLY and ONLY what the user requests.
Do not add:
- Extra components not specified
- Styling unless explicitly requested
- "Nice to have" features
- Explanatory comments beyond what's needed
```

### 3. Long Context Handling (>10K tokens)

For long inputs, force summarization first:

```
<document>
[Very long document here...]
</document>

IMPORTANT: Before answering:
1. First summarize the key points relevant to my question
2. Then re-state my constraints
3. Finally, provide your answer

Question: [Your question]
Constraints: [Your constraints]
```

### 4. Ambiguity Mitigation

When instructions are unclear:

```
If any aspect of this request is ambiguous:
1. Explicitly call out the ambiguity
2. Present 2-3 plausible interpretations
3. Label your assumptions clearly
4. Ask clarifying questions before proceeding
```

## Agentic Prompting

### Brief Status Updates

```
When providing status updates:
- Keep updates to 1-2 sentences only
- Update when starting new phases or discovering plan changes
- Do NOT narrate routine tool calls
- Each update must include concrete outcomes
```

### Tool Use Guidance

```
You have access to these tools: [list]

When using tools:
1. Plan your approach first
2. Execute tools in logical order
3. Verify results before proceeding
4. If a tool fails, try alternative approaches
5. Report concrete outcomes, not process
```

### Error Recovery

```
If you encounter an error:
1. Analyze the root cause
2. Attempt a fix
3. If still failing after 3 attempts, explain:
   - What you tried
   - Why it failed
   - Suggested next steps
```

## Structured Extraction

Always provide explicit schemas:

```
Extract information as JSON with this schema:
{
  "required_fields": {
    "name": "string",
    "date": "ISO 8601 string",
    "amount": "number"
  },
  "optional_fields": {
    "notes": "string or null",
    "category": "string or null"
  }
}

Rules:
- Set missing required fields to empty string/0
- Set missing optional fields to null
- Do NOT guess or infer values not in source
```

## Code Generation

### Clean Output

```
Output ONLY the code.
No explanations before or after.
No markdown code fences unless specifically requested.
No comments unless they clarify non-obvious logic.
```

### Targeted Changes

```
When modifying code:
1. Show only the changed sections
2. Include 3-5 lines of context before/after
3. Use clear markers: // CHANGED or # MODIFIED
4. Do not regenerate unchanged code
```

## Temperature Guidelines

| Task | Temperature | Reasoning Effort |
|------|-------------|------------------|
| Code generation | 0 - 0.3 | none or low |
| Data extraction | 0 | none |
| Analysis | 0.3 - 0.5 | medium |
| Creative | 0.7 - 1.0 | low |
| Brainstorming | 1.0+ | low |

## Differences from GPT-5.1

| Aspect | GPT-5.1 | GPT-5.2 |
|--------|---------|---------|
| Verbosity | Moderate | Lower (more concise) |
| Instruction following | Good | Stronger |
| Token efficiency | Good | Better |
| Price | $1.25/$10 | $1.75/$14 |
| Reasoning calibration | Fixed | Adaptive to difficulty |
| Formatting | Good | Cleaner |

## Cached Input Optimization

GPT-5.2 offers 90% discount on cached inputs:

```python
# Structure prompts with stable prefix
system_prompt = """[Your system instructions - these get cached]"""

# Variable content at the end
user_content = f"""
{system_prompt}

Current task: {task}
"""
```

**Tips for maximizing cache hits:**
- Put static instructions at the beginning
- Put variable content at the end
- Reuse identical prefixes across requests

## GPT-5.2-Codex for Coding

For agentic coding tasks, use GPT-5.2-Codex:

```python
response = client.responses.create(
    model="gpt-5.2-codex",
    input=[
        {"role": "developer", "content": "You are a senior software engineer."},
        {"role": "user", "content": "Refactor this module to use async/await"}
    ]
)
```

**Codex-specific best practices:**
- "Less is more" - start minimal, add guidance as needed
- Many coding best practices are built-in
- Over-prompting can reduce quality
- Good for long-horizon agentic work
- Excellent at large refactors and migrations

## Common Anti-Patterns

### Don't Over-explain

```
# Bad
I want you to understand that this is a very important task and I need you
to carefully analyze this code before making any changes. Please think step
by step about what you're doing...

# Good
Analyze this code for security vulnerabilities. List each issue with severity.
```

### Don't Repeat Instructions

```
# Bad
Be concise. Remember to be concise. Your response should be concise.
Keep it short. Brevity is important.

# Good
Maximum 100 words.
```

### Don't Mix Conflicting Constraints

```
# Bad
Be thorough and comprehensive, but also keep it brief and to the point.

# Good
Provide a thorough analysis in bullet points (max 10 bullets, 1 sentence each).
```

## Model Selection: When to Use GPT-5.2

| Scenario | Use GPT-5.2 | Alternative |
|----------|-------------|-------------|
| Enterprise knowledge work | ✅ | - |
| Complex multi-step projects | ✅ | - |
| Agentic coding | ✅ (Codex) | - |
| Simple Q&A | ❌ | GPT-4.1 mini |
| Budget-constrained | ❌ | GPT-4.1 |
| Audio I/O needed | ❌ | GPT-4o |
| Extended reasoning | ❌ | o3 |

## Official Resources

- [GPT-5.2 Prompting Guide](https://cookbook.openai.com/examples/gpt-5/gpt-5-2_prompting_guide)
- [GPT-5.2-Codex Guide](https://cookbook.openai.com/examples/gpt-5-codex_prompting_guide)
- [Prompt Optimizer Tool](https://platform.openai.com/playground) - Use to migrate prompts
- [GPT-5.2 Model Docs](https://platform.openai.com/docs/models/gpt-5.2)
