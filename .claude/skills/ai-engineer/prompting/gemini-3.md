# Gemini 3 Prompting Guide

Based on [Google's official prompting strategies](https://ai.google.dev/gemini-api/docs/prompting-strategies).

## Key Characteristics

Gemini 3 models (Flash and Pro) have specific behaviors:

1. **Strong instruction following** - Precise execution of instructions
2. **Excellent multimodal** - 81.2% MMMU-Pro score
3. **Superior coding** - 78% SWE-bench (Flash)
4. **1M token context** - Handle very long documents
5. **Thinking level control** - Adjustable reasoning depth

## Thinking Level Control

Gemini 3 supports adjustable reasoning:

```python
response = client.models.generate_content(
    model="gemini-3-flash-preview",
    config={
        "thinking_level": "medium"  # minimal, low, medium, high
    },
    contents="Your prompt here"
)
```

| Level | Use Case | Token Usage |
|-------|----------|-------------|
| `minimal` | Simple tasks | Lowest |
| `low` | Standard queries | Low |
| `medium` | Default, balanced | Medium |
| `high` | Complex reasoning | Higher |

## Critical: Temperature Setting

**For Gemini 3 models, keep temperature at default 1.0.**

Setting temperature below 1.0 can cause:
- Unexpected looping behavior
- Degraded performance on math/reasoning
- Inconsistent outputs

```python
# Good - use default
config = {}

# Bad - can cause issues
config = {"temperature": 0.7}  # Don't do this for Gemini 3
```

## Core Prompting Techniques

### 1. Few-Shot Prompting (Recommended)

Always include examples when possible:

```python
prompt = """
English: Hello
French: Bonjour

English: Goodbye
French: Au revoir

English: Good morning
French:
"""
```

**Key principle:** Show positive examples, not anti-patterns.

### 2. Input/Output Prefixes

Use prefixes to signal structure:

```python
prompt = """
Input: What is machine learning?
Output: Machine learning is a subset of AI that enables systems to learn from data.

Input: Explain quantum computing.
Output:
"""
```

### 3. Constraint Definition

Specify limitations clearly:

```python
prompt = """
Summarize this article in exactly one sentence.
Do not exceed 20 words.
Focus only on the main conclusion.

Article: [content]
"""
```

### 4. Context Addition

Provide necessary background:

```python
prompt = """
Context: You are helping a customer troubleshoot their home router.
The router model is TP-Link Archer AX6000.
Common issues include: WiFi dropping, slow speeds, firmware updates.

Customer question: My internet keeps disconnecting every few hours.

Provide a step-by-step troubleshooting guide.
"""
```

## Gemini 3 Structural Principles

### Be Direct and Concise

```
# Good
Extract the company name and revenue from this text.

# Avoid
I would like you to please carefully read through the following text
and then extract the relevant information...
```

### Use Consistent Delimiters

```xml
<document>
[Your document content]
</document>

<instructions>
1. Extract key facts
2. Summarize in 3 bullets
3. Identify any dates mentioned
</instructions>

<output_format>
JSON with keys: facts, summary, dates
</output_format>
```

### Explicit Verbosity Control

```
<verbosity>
- Use 1-2 sentences per point
- Maximum 5 bullet points
- No introductory phrases like "Here's what I found..."
</verbosity>
```

### Instruction Priority

Place critical instructions at the start:

```
IMPORTANT: Output must be valid JSON only. No markdown.

[Rest of your prompt...]
```

### Context Placement

Put large context blocks first, queries last:

```
<context>
[10,000 words of documentation...]
</context>

<query>
Based on the documentation above, how do I configure OAuth?
</query>
```

## Knowledge Management

Add these to system instructions when needed:

```
# Current date awareness
Remember that today is January 2026.

# Knowledge cutoff
Your knowledge cutoff date is January 2025. For events after this,
rely on provided context or indicate uncertainty.

# Grounding instruction
Base your response ONLY on the provided context. If the answer is not
in the context, say "I don't have information about this in the provided documents."
```

## Reasoning Enhancement

### Explicit Planning

```
Before answering:
1. Parse the question into sub-tasks
2. Check if you have all required information
3. Create a structured outline
4. Self-critique your plan before executing
```

### Self-Critique

```
<self_critique>
After generating your response:
1. Check for logical inconsistencies
2. Verify all claims are supported by context
3. Ensure you answered all parts of the question
4. Refine if needed before finalizing
</self_critique>
```

## Agentic Workflow Configuration

Steer behavior across three dimensions:

```xml
<agent_behavior>
  <reasoning>
    - Break complex problems into sub-tasks
    - Diagnose issues before proposing solutions
    - Be exhaustive in gathering information
  </reasoning>

  <execution>
    - Adapt when new data contradicts assumptions
    - Persist through errors (try 3 approaches before asking for help)
    - Assess risk before destructive operations
  </execution>

  <interaction>
    - Ask for clarification only when truly ambiguous
    - Keep updates brief and outcome-focused
    - Be precise in technical contexts
  </interaction>
</agent_behavior>
```

## Response Format Control

### JSON Output

```python
prompt = """
Extract information as JSON:
{
  "name": "string",
  "email": "string or null",
  "company": "string or null"
}

Text: John Smith works at Acme Corp. His email is john@acme.com.
"""
```

### Table Format

```python
prompt = """
Compare these products in a markdown table with columns:
| Product | Price | Rating | Key Feature |

Products: [list]
"""
```

### Structured Lists

```python
prompt = """
Provide your analysis as:

## Summary
[2-3 sentences]

## Key Points
- Point 1
- Point 2
- Point 3

## Recommendation
[1 sentence]
"""
```

## Iteration Strategies

When initial results aren't satisfactory:

1. **Rephrase**: Try different wording for same concept
2. **Switch tasks**: Reframe as analogous problem (e.g., categorization → multiple choice)
3. **Reorder content**: Experiment with `[examples] → [context] → [input]` order

## Complex Prompt Architecture

For intricate tasks:

```python
# Break into chained prompts
step1_result = gemini("Extract all entities from: {document}")
step2_result = gemini(f"Classify these entities: {step1_result}")
step3_result = gemini(f"Generate summary based on: {step2_result}")
```

Or use parallel operations:

```python
# Process segments in parallel
results = [gemini(f"Analyze: {segment}") for segment in segments]
final = gemini(f"Synthesize these analyses: {results}")
```

## Media Resolution Control (Gemini 3 Only)

For multimodal inputs:

```python
config = {
    "media_resolution": "high"  # low, medium, high, ultra high
}
```

Use higher resolution for:
- Detailed image analysis
- Document OCR
- Small text recognition

Use lower resolution for:
- General image understanding
- Faster processing
- Cost optimization

## Things to Avoid

1. **Don't rely solely on models for factual generation** - Use grounding
2. **Use caution with math/logic** - Verify critical calculations
3. **Don't assume model knowledge** - Provide necessary context
4. **Don't set temperature <1.0 for Gemini 3** - Can cause issues

## Sources

- [Gemini Prompting Strategies](https://ai.google.dev/gemini-api/docs/prompting-strategies)
- [Gemini Enterprise Prompt Guide](https://cloud.google.com/gemini-enterprise/resources/prompt-guide)
- [Getting Started with Gemini](https://www.promptingguide.ai/models/gemini)
