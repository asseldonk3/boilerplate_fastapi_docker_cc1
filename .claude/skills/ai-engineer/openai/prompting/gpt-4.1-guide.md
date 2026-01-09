# GPT-4.1 Prompting Guide

GPT-4.1 represents a significant improvement over GPT-4o in coding, instruction following, and long context handling. This guide covers best practices derived from OpenAI's internal testing.

## Key Characteristics of GPT-4.1

1. **More literal instruction following** - Follows instructions exactly as written
2. **1M token context** - Can process much longer documents
3. **Better at coding** - State-of-the-art on SWE-bench (55%)
4. **Agentic capabilities** - Excellent for multi-step autonomous tasks

## Core Principles

### 1. Be Specific and Literal

GPT-4.1 follows instructions more literally than predecessors. Be explicit about what you want.

```
# Bad - Too vague
Summarize this document.

# Good - Specific
Summarize this document in exactly 3 bullet points.
Each bullet should be one sentence.
Focus on financial metrics only.
```

### 2. Use the Sandwich Method for Long Context

When working with long documents (>50K tokens), place instructions at BOTH the beginning AND end.

```
# Structure for long context
[System prompt with instructions]
[Long document content...]
[Repeat key instructions at the end]

# Example
System: You are analyzing a legal contract. Focus on liability clauses.

[200 pages of contract text...]

User: Based on the contract above, list all liability clauses.
Remember to focus ONLY on liability-related sections.
Format as a numbered list.
```

### 3. Provide Context Examples

Show the model what you want through examples.

```
System: You are a code reviewer. Provide feedback in this format:

Example input:
```python
def add(a, b):
    return a + b
```

Example output:
- **Severity**: Low
- **Issue**: Missing type hints
- **Suggestion**: Add type hints for better code clarity
- **Fixed code**:
```python
def add(a: int, b: int) -> int:
    return a + b
```

Now review the following code:
[user's code here]
```

### 4. Induce Planning for Complex Tasks

For multi-step problems, ask the model to plan first.

```
Before solving, first:
1. Identify the key components of this problem
2. List the steps needed to solve it
3. Note any potential edge cases
4. Then execute your plan step by step

Problem: [complex problem here]
```

## Agentic Workflows

GPT-4.1 excels at autonomous, multi-step tasks. Use these patterns:

### Persistence Reminder
```
You are an agent. Keep working until the user's query is completely
resolved before ending your turn and yielding back to the user.
Do not stop prematurely.
```

### Tool Use Guidance
```
You have access to these tools:
- search: Search the codebase
- edit: Edit files
- run: Run commands

When solving a task:
1. First, search to understand the codebase
2. Plan your changes
3. Make edits one file at a time
4. Run tests after each change
5. Continue until all tests pass
```

### Error Recovery
```
If you encounter an error:
1. Analyze the error message
2. Identify the root cause
3. Attempt a fix
4. Verify the fix worked
5. If still failing after 3 attempts, explain what you tried

Do NOT give up after the first error.
```

## Temperature Settings

| Use Case | Temperature | Rationale |
|----------|-------------|-----------|
| Code generation | 0 - 0.2 | Deterministic, consistent |
| Code review | 0 - 0.3 | Factual analysis |
| Technical writing | 0.3 - 0.5 | Some variation, mostly factual |
| Creative writing | 0.7 - 1.0 | More creative variety |
| Brainstorming | 1.0 - 1.5 | Maximum diversity |

## Structured Output

### JSON Mode
```python
response = client.chat.completions.create(
    model="gpt-4.1",
    messages=[
        {"role": "system", "content": "Output valid JSON. Always include a 'result' field."},
        {"role": "user", "content": "List 3 programming languages with their paradigms"}
    ],
    response_format={"type": "json_object"}
)
```

**Important:** Always mention "JSON" in your prompt when using JSON mode.

### Schema Enforcement with Functions
```python
tools = [{
    "type": "function",
    "function": {
        "name": "structured_response",
        "strict": True,
        "parameters": {
            "type": "object",
            "properties": {
                "languages": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "name": {"type": "string"},
                            "paradigm": {"type": "string"}
                        },
                        "required": ["name", "paradigm"]
                    }
                }
            },
            "required": ["languages"]
        }
    }
}]
```

## Common Patterns

### Code Generation
```
Write a Python function that [description].

Requirements:
- Use type hints
- Include docstring with examples
- Handle edge cases: [list them]
- Follow PEP 8 style

Do not include any explanation, only the code.
```

### Code Review
```
Review this code for:
1. Bugs and logic errors
2. Security vulnerabilities
3. Performance issues
4. Code style and readability

For each issue found:
- Quote the problematic code
- Explain the issue
- Provide the corrected code

Code to review:
```[code]```
```

### Document Analysis
```
Analyze the following document and extract:
1. Main topics (max 5)
2. Key entities mentioned
3. Dates and deadlines
4. Action items

Format your response as:
## Topics
- topic 1
- topic 2

## Entities
- entity: description

## Dates
- date: associated event

## Action Items
- [ ] action item

Document:
[long document here]

Remember: Extract ONLY what's explicitly stated. Do not infer or assume.
```

### Multi-turn Conversation Memory
```
# System prompt for consistent persona
You are Alex, a senior software engineer at TechCorp.
- You have 10 years of experience
- You specialize in distributed systems
- You're friendly but direct
- You always ask clarifying questions before giving advice

Maintain this persona throughout the conversation.
Remember details the user shares about their project.
```

## What NOT to Do

### Don't Be Vague
```
# Bad
Help me with my code.

# Good
Debug this Python function that should return the factorial of n,
but returns incorrect results for n > 10.
```

### Don't Assume
```
# Bad (assumes model knows context)
Update the function we discussed.

# Good (provides context)
Update the calculate_tax function in utils.py to handle
negative income values by returning 0.
```

### Don't Over-constrain
```
# Bad (too many competing constraints)
Write a function that is:
- Under 10 lines
- Has full error handling
- Is fully documented
- Handles all edge cases
- Uses no external libraries
- Is highly performant

# Good (prioritized constraints)
Write a function that handles the main use case efficiently.
Prioritize: correctness > readability > performance.
Error handling for invalid input types only.
```

## Differences from GPT-4o

| Aspect | GPT-4o | GPT-4.1 |
|--------|--------|---------|
| Instruction following | Infers intent | More literal |
| Context window | 128K | 1M |
| Coding ability | Good | State-of-the-art |
| Prompts may need | More guidance | Less hand-holding |
| Best for | General chat | Complex tasks, coding |

## Version Pinning

For consistent behavior, pin to specific versions:

```python
# Auto-updating (may change behavior)
model="gpt-4.1"

# Pinned (consistent behavior)
model="gpt-4.1-2025-01-01"  # Example, check docs for actual versions
```

## Official Resources
- GPT-4.1 Prompting Guide: https://cookbook.openai.com/examples/gpt4-1_prompting_guide
- Prompt Engineering: https://platform.openai.com/docs/guides/prompt-engineering
