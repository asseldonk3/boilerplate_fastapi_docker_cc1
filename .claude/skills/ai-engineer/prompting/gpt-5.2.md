# GPT-5.2 Prompting Guide

Based on [OpenAI's official GPT-5.2 prompting guide](https://cookbook.openai.com/examples/gpt-5/gpt-5-2_prompting_guide).

## Key Characteristics

GPT-5.2 has distinct behavioral traits that require specific prompting approaches:

1. **More deliberate scaffolding** - Structured, planned responses
2. **Lower verbosity** - Concise by default
3. **Stronger instruction adherence** - Follows instructions precisely
4. **Token efficient** - Cleaner output
5. **Prompt-sensitive** - Responds well to tone/style guidance

## Reasoning Effort Control

GPT-5.2 supports adjustable reasoning depth:

```python
response = client.responses.create(
    model="gpt-5.2",
    reasoning={"effort": "medium"},  # none, low, medium, high, xhigh
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
| GPT-5 / GPT-5.1 | Keep existing (`minimal` → `none`) |

## Critical Prompting Patterns

### 1. Verbosity Control

GPT-5.2 is concise by default. For detailed responses, be explicit:

```
Provide your analysis in this format:
1. One short overview paragraph
2. Up to 5 bullets tagged as:
   - What changed
   - Where
   - Risks
   - Next steps
```

### 2. Scope Discipline

Prevent feature creep with explicit boundaries:

```
Implement EXACTLY and ONLY what the user requests.
Do not add:
- Extra components not specified
- Styling unless explicitly requested
- "Nice to have" features
- Explanatory comments beyond what's needed
```

### 3. Long Context Handling (>10K tokens)

Force re-grounding for long inputs:

```
<document>
[Very long document here...]
</document>

IMPORTANT: Before answering:
1. First summarize the key points relevant to my question
2. Re-state my constraints
3. Finally, provide your answer

Question: [Your question]
Constraints: [Your constraints]
```

### 4. Ambiguity Mitigation

Handle unclear instructions gracefully:

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

## Web Search & Research

```
<research_configuration>
- Do not ask clarifying questions; cover all plausible intents instead
- Require breadth/depth when uncertainty exists
- Include citations for all web-derived information
- Write in Markdown with headers, bullets, tables for comparisons
</research_configuration>
```

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

For agentic coding tasks:

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

## Context Compaction

For multi-step workflows exceeding context limits:

```python
compacted_response = client.responses.compact(
   model="gpt-5.2",
   input=[user_message, assistant_output]
)
```

Use after major milestones, not every turn.

## Common Anti-Patterns

### Don't Over-explain

```
# Bad
I want you to understand that this is a very important task and I need you
to carefully analyze this code before making any changes...

# Good
Analyze this code for security vulnerabilities. List each issue with severity.
```

### Don't Repeat Instructions

```
# Bad
Be concise. Remember to be concise. Your response should be concise.

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

## Prompt Block Templates

### Uncertainty Handling
```
<uncertainty_and_ambiguity>
- If ambiguous, call it out and ask 1-3 precise questions OR present 2-3 labeled interpretations
- For time-sensitive facts without tools, answer generally and state details may have changed
- Never fabricate exact figures or external references when uncertain
</uncertainty_and_ambiguity>
```

### High-Risk Self-Check
```
<high_risk_self_check>
Before finalizing in legal/financial/compliance contexts:
- Re-scan for unstated assumptions
- Check specific numbers grounded in context
- Soften overly strong language ("always," "guaranteed")
</high_risk_self_check>
```

## Temperature Guidelines

| Task | Temperature | Reasoning Effort |
|------|-------------|------------------|
| Code generation | 0 - 0.3 | none or low |
| Data extraction | 0 | none |
| Analysis | 0.3 - 0.5 | medium |
| Creative | 0.7 - 1.0 | low |
| Brainstorming | 1.0+ | low |

## Sources

- [GPT-5.2 Prompting Guide](https://cookbook.openai.com/examples/gpt-5/gpt-5-2_prompting_guide)
- [GPT-5.2-Codex Guide](https://cookbook.openai.com/examples/gpt-5-codex_prompting_guide)
- [Prompt Optimizer Tool](https://platform.openai.com/playground)
