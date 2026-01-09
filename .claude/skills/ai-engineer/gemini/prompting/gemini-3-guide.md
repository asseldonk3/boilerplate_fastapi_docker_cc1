# Gemini 3 Prompting Guide

Gemini 3 (released November 2025) brings major improvements to instruction understanding and multimodal reasoning. If you wrote elaborate prompts for Gemini 2.x, you're likely over-engineering now.

## Core Philosophy

**Gemini 3 likes three things:**
1. Clear instructions
2. Consistent structure
3. Freedom from fluff

## Key Changes from Gemini 2.x

| Aspect | Gemini 2.x | Gemini 3 |
|--------|------------|----------|
| Prompt complexity | More guidance needed | Simpler is better |
| Temperature | Tune for your use case | Keep at 1.0 (default) |
| Structure | Free-form OK | XML/Markdown preferred |
| Constraints | Early in prompt | At the END |
| Verbosity | Default chattier | More concise by default |

## Structure Your Prompts

Use XML-style tags OR Markdown headings (don't mix!):

### XML Style (Recommended for Complex Tasks)
```xml
<context>
You are an expert code reviewer specializing in Python.
</context>

<task>
Review the following code for bugs, security issues, and performance.
</task>

<code>
def calculate_total(items):
    total = 0
    for item in items:
        total += item['price'] * item['quantity']
    return total
</code>

<output_format>
- List each issue with severity (high/medium/low)
- Provide the corrected code
</output_format>
```

### Markdown Style
```markdown
# Context
You are an expert code reviewer specializing in Python.

# Task
Review the following code for bugs, security issues, and performance.

# Code
```python
def calculate_total(items):
    ...
```

# Output Format
- List each issue with severity
- Provide corrected code
```

**Important:** Choose ONE format and stick with it throughout the prompt.

## Place Constraints at the END

Gemini 3 may drop constraints that appear too early. Put critical restrictions last:

### Bad (Constraints at start)
```
Do not include code examples.
Do not exceed 100 words.
Explain how neural networks work.
```

### Good (Constraints at end)
```
Explain how neural networks work.

Important constraints:
- Do not include code examples
- Keep response under 100 words
```

## System Instructions

Place behavioral constraints and role definitions in the system instruction:

```python
response = client.models.generate_content(
    model="gemini-3-pro-preview",
    contents="Explain quantum entanglement",
    config=types.GenerateContentConfig(
        system_instruction="""You are a physics professor at MIT.

        Behavioral guidelines:
        - Use analogies from everyday life
        - Avoid unnecessary jargon
        - Be enthusiastic but accurate"""
    )
)
```

## Temperature Settings

**Keep temperature at 1.0 for Gemini 3.**

Gemini 3's reasoning capabilities are optimized for the default temperature. Unlike GPT models, lowering temperature doesn't necessarily improve quality.

```python
# Recommended for Gemini 3
config = types.GenerateContentConfig(
    temperature=1.0  # Default, optimal
)
```

## Long Context Handling

For large documents (books, codebases, long videos):

1. **Place instructions at the END** of the prompt
2. **Anchor with explicit references**

```
[200 pages of document content...]

Based on the entire document above:
1. What are the three main arguments presented?
2. What evidence supports each argument?
3. What are the potential counterarguments?

Remember to cite specific sections when answering.
```

## Simplify Your Prompts

### Gemini 2.x Style (Over-engineered)
```
I need you to act as a helpful assistant who will carefully and thoughtfully
analyze the following text. Please take your time to consider all aspects of
the text before providing your response. Your response should be well-structured
and comprehensive. You should identify the main themes, supporting arguments,
and any logical fallacies present. Please format your response using bullet
points for clarity. Remember to be objective and balanced in your analysis.
Additionally, please cite specific passages from the text to support your points.
Make sure to consider both strengths and weaknesses of the arguments presented.
Finally, provide a brief summary of your findings at the end of your response.

Text: [text here]
```

### Gemini 3 Style (Clean)
```
Analyze this text:

[text here]

Identify:
- Main themes
- Supporting arguments
- Logical fallacies

Cite specific passages. Include strengths and weaknesses.
End with a brief summary.
```

## Controlling Verbosity

Gemini 3 is less verbose by default. If you need more detail:

```
# For more conversational/detailed responses:
Be thorough and conversational in your response. Explain your reasoning step by step.

# For concise responses (default behavior):
Be concise and direct.
```

## Persona Handling

Gemini 3 takes personas seriously and may prioritize persona adherence over other instructions:

```python
# Be careful with persona conflicts
system_instruction = """You are Marcus, a grumpy but knowledgeable librarian.
You've been working at the library for 40 years.
You're skeptical of new technology but secretly curious about AI."""

# If you then ask it to be "enthusiastic", it may conflict with the grumpy persona
# Be consistent with your persona definition
```

## Date and Time Awareness

Add current date context for time-sensitive queries:

```python
system_instruction = """Current date: January 15, 2025
Your knowledge cutoff: January 2025

For time-sensitive queries, acknowledge the current date.
When searching, use 2025 in queries for recent information."""
```

## Multi-turn Conversations

Gemini 3 has excellent context retention. Keep conversations flowing naturally:

```python
history = [
    {"role": "user", "parts": [{"text": "I'm planning a trip to Japan"}]},
    {"role": "model", "parts": [{"text": "Great choice! What aspects of Japan interest you most?"}]},
    {"role": "user", "parts": [{"text": "I love technology and traditional culture"}]},
    # Model remembers the context and interests
]
```

## Multimodal Best Practices

### Image Analysis
```
<image>
[uploaded image]
</image>

<task>
Describe this image in detail, focusing on:
1. Main subjects
2. Colors and composition
3. Any text visible
4. Emotional tone or mood
</task>
```

### Video Analysis
```
<video>
[uploaded video]
</video>

<task>
Summarize this video:
- Main topic
- Key points (timestamped if possible)
- Overall quality assessment
</task>
```

## Thinking Mode (for Complex Reasoning)

Enable thinking for complex problems:

```python
response = client.models.generate_content(
    model="gemini-3-pro-preview",
    contents="Solve this complex math problem: [problem]",
    config=types.GenerateContentConfig(
        thinking_config=types.ThinkingConfig(
            thinking_budget=10000
        )
    )
)

# Access thinking process
thinking = response.candidates[0].content.parts[0].thought
answer = response.text
```

## Function Calling Best Practices

```python
# Clear, concise function descriptions work best
function = types.FunctionDeclaration(
    name="search_products",
    description="Search the product catalog by query. Returns top 10 matches.",
    parameters=types.Schema(
        type="object",
        properties={
            "query": types.Schema(
                type="string",
                description="Search keywords, e.g., 'wireless headphones'"
            ),
            "category": types.Schema(
                type="string",
                enum=["electronics", "clothing", "home", "all"]
            ),
            "max_price": types.Schema(
                type="number",
                description="Maximum price in USD"
            )
        },
        required=["query"]
    )
)
```

## Common Patterns

### Code Generation
```
Write a Python function to [description].

Requirements:
- Type hints
- Docstring with example
- Handle edge cases: [list]

Output only the code, no explanation.
```

### Structured Extraction
```xml
<document>
[document content]
</document>

<extraction_task>
Extract the following fields as JSON:
- company_name (string)
- revenue (number, in millions USD)
- year (integer)
- key_products (array of strings)
</extraction_task>

Return valid JSON only.
```

### Analysis Tasks
```
Analyze this [dataset/text/code]:

[content]

Provide:
1. Summary (2-3 sentences)
2. Key findings (bullet points)
3. Recommendations (prioritized list)

Keep total response under 300 words.
```

## What NOT to Do

### Don't Over-explain
```
# Bad
I want you to understand that this is very important and I need you to
carefully think about this before responding...

# Good
[Just ask the question directly]
```

### Don't Mix Formats
```
# Bad - mixing XML and Markdown
<context>
# Background
You are an assistant...
</context>

# Good - consistent format
<context>
<background>You are an assistant...</background>
</context>
```

### Don't Repeat Instructions
```
# Bad
Be concise. Remember to be concise. Your response should be concise.

# Good
Be concise. Under 100 words.
```

## Quick Reference

| Task | Key Tip |
|------|---------|
| Simple Q&A | Ask directly, no preamble |
| Complex reasoning | Use thinking mode |
| Long context | Instructions at END |
| Structured output | Use JSON mode |
| Code tasks | Specify language, constraints |
| Creative | Embrace temperature=1.0 |
| Precise formatting | Put constraints LAST |

## Official Resources
- Gemini 3 Prompting Guide: https://docs.cloud.google.com/vertex-ai/generative-ai/docs/start/gemini-3-prompting-guide
- Prompt Design Strategies: https://ai.google.dev/gemini-api/docs/prompting-strategies
