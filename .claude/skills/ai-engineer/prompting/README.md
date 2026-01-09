# Prompting Guide

This chapter covers prompting techniques for getting the best results from LLMs. It focuses on **techniques** rather than model selection.

## Contents

### Model-Specific Guides
- [GPT-5.2 Prompting](./gpt-5.2.md) - OpenAI's latest flagship
- [Gemini 3 Prompting](./gemini-3.md) - Google's latest models
- [Claude 4.5 Prompting](./claude-4.5.md) - Anthropic's Claude family

### Advanced Techniques
- [Reasoning Techniques](./techniques/reasoning.md) - CoT, ToT, Self-Consistency
- [Hallucination Reduction](./techniques/hallucination-reduction.md) - CoVe and verification methods
- [Agentic Prompting](./techniques/agentic.md) - Tool use, multi-step, long-horizon tasks

## Quick Reference: Universal Best Practices

These apply across all models:

### 1. Be Explicit and Specific
```
❌ "Create a dashboard"
✅ "Create an analytics dashboard with user engagement metrics, retention charts, and export functionality"
```

### 2. Provide Context
```
❌ "NEVER use ellipses"
✅ "Your response will be read by a text-to-speech engine, so never use ellipses since they cannot be pronounced"
```

### 3. Show Don't Tell (Few-Shot)
Include examples of desired output format rather than just describing it.

### 4. Control Output Format
- Specify length constraints ("max 3 sentences", "≤5 bullets")
- Define structure ("respond in JSON with schema: {...}")
- Use delimiters (XML tags, markdown headers)

### 5. Iterate and Refine
Prompt engineering is iterative. Start simple, identify issues, refine.

## Model-Specific Quick Tips

| Aspect | GPT-5.2 | Gemini 3 | Claude 4.5 |
|--------|---------|----------|------------|
| Default verbosity | Low (concise) | Medium | Low (direct) |
| Instruction following | Very strong | Strong | Very strong |
| Reasoning parameter | `reasoning.effort` | `thinking_level` | Extended thinking |
| Format control | Explicit constraints | XML tags + prefixes | Explicit + XML |
| Temperature tip | Keep default for reasoning | Keep 1.0 for Gemini 3 | Default usually best |

## Technique Selection Guide

| Goal | Technique | When to Use |
|------|-----------|-------------|
| Step-by-step reasoning | Chain of Thought | Math, logic, planning |
| Reduce hallucinations | Chain of Verification | Factual queries, research |
| Complex decisions | Tree of Thoughts | Multi-path problems |
| Improve accuracy | Self-Consistency | When one answer exists |
| Tool orchestration | ReAct | Agentic workflows |
| Long tasks | State management | Multi-turn, multi-window |
