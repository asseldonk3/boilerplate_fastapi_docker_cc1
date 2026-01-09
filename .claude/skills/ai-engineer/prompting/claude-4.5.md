# Claude 4.5 Prompting Guide

Based on [Anthropic's official Claude 4 best practices](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/claude-4-best-practices).

## Key Characteristics

Claude 4.5 models (Opus, Sonnet, Haiku) have distinct traits:

1. **Precise instruction following** - Does exactly what you ask
2. **More concise** - Direct, less verbose by default
3. **Highly steerable** - Responds well to system prompts
4. **Long-horizon reasoning** - Excellent at multi-step tasks
5. **Native subagent orchestration** - Delegates tasks intelligently

## Critical Differences from Previous Models

### Be Explicit

Claude 4.x does exactly what you ask - no more, no less:

```
# If you say this:
"Suggest some changes"
# Claude will suggest, not implement

# If you want action:
"Make these changes"
# or
"Change this function to improve performance"
```

### Avoid Aggressive Language

Opus 4.5 is more responsive to prompts. Tone down aggressive instructions:

```
# Old style (can cause overtriggering)
CRITICAL: You MUST use this tool when...

# New style
Use this tool when...
```

### "Think" Sensitivity

When extended thinking is disabled, Claude is sensitive to "think":

```
# May trigger unexpected behavior
"Think about this problem..."

# Better alternatives
"Consider this problem..."
"Evaluate this scenario..."
"Analyze this situation..."
```

## Core Prompting Patterns

### 1. Add Context/Motivation

Explain *why*, not just *what*:

```
# Less effective
NEVER use ellipses

# More effective
Your response will be read aloud by a text-to-speech engine,
so never use ellipses since they cannot be pronounced.
```

Claude generalizes from explanations.

### 2. Request "Above and Beyond" Explicitly

Claude 4.x is more restrained. Ask for more when you want it:

```
# Basic
Create an analytics dashboard

# Better
Create an analytics dashboard. Include as many relevant features
and interactions as possible. Go beyond the basics to create a
fully-featured implementation.
```

### 3. Careful with Examples

Claude pays close attention to examples. Ensure they demonstrate desired behavior:

```
# Your examples should match your goals exactly
# Don't include behaviors in examples you don't want replicated
```

## Tool Usage Patterns

### Making Claude Act

```xml
<default_to_action>
By default, implement changes rather than only suggesting them.
If the user's intent is unclear, infer the most useful likely action
and proceed, using tools to discover any missing details instead of guessing.
</default_to_action>
```

### Making Claude Conservative

```xml
<do_not_act_before_instructions>
Do not jump into implementation or change files unless clearly instructed.
When the user's intent is ambiguous, default to providing information,
doing research, and providing recommendations rather than taking action.
</do_not_act_before_instructions>
```

### Parallel Tool Calling

Sonnet 4.5 is aggressive with parallel execution. Control it:

```xml
<use_parallel_tool_calls>
If you intend to call multiple tools and there are no dependencies
between the calls, make all independent calls in parallel.
Maximize parallel tool calls where possible to increase speed.
However, if some calls depend on previous results, call sequentially.
Never use placeholders or guess missing parameters.
</use_parallel_tool_calls>
```

Or reduce parallelism:

```
Execute operations sequentially with brief pauses between each step.
```

## Long-Horizon Reasoning

### Context Awareness

Claude 4.5 tracks its remaining context window. Help it manage this:

```
Your context window will be automatically compacted as it approaches its limit.
Do not stop tasks early due to token budget concerns.
Save your progress to memory before context refreshes.
Be persistent and complete tasks fully.
```

### Multi-Window Workflows

For tasks spanning multiple sessions:

1. **First window**: Set up framework (tests, scripts)
2. **Subsequent windows**: Iterate on todo-list

```
# State tracking with structured files
# tests.json - for test status
# progress.txt - for freeform notes
# Use git for checkpoints
```

### State Management

```json
// Structured state (tests.json)
{
  "tests": [
    {"id": 1, "name": "auth_flow", "status": "passing"},
    {"id": 2, "name": "user_mgmt", "status": "failing"}
  ],
  "passing": 150,
  "failing": 25
}
```

```text
// Progress notes (progress.txt)
Session 3:
- Fixed token validation
- Next: investigate test #2 failures
- Note: Do not remove tests
```

## Format Control

### Method 1: Tell What TO Do

```
# Instead of
Do not use markdown

# Say
Write in smoothly flowing prose paragraphs.
```

### Method 2: XML Format Indicators

```
Write the prose sections in <smoothly_flowing_prose_paragraphs> tags.
```

### Method 3: Match Prompt to Output

Your prompt's formatting style influences Claude's response style.
Remove markdown from prompts if you don't want markdown in outputs.

### Method 4: Detailed Format Specification

```xml
<avoid_excessive_markdown>
Write in clear, flowing prose using complete paragraphs.
Reserve markdown for:
- `inline code`
- code blocks (```...```)
- simple headings (### )

DO NOT use bullet lists unless:
a) Items are truly discrete
b) User explicitly requests lists

Never output a series of short bullet points.
Your goal is readable, flowing text.
</avoid_excessive_markdown>
```

## Verbosity Control

Claude 4.5 may skip summaries after tool calls. Request them:

```
After completing tool use, provide a quick summary of what you did.
```

## Research & Information Gathering

```
Search in a structured way:
1. Develop competing hypotheses
2. Track confidence levels
3. Self-critique your approach
4. Update a research notes file
5. Break down complex research systematically
```

## Code Exploration

Prevent speculation:

```xml
<investigate_before_answering>
Never speculate about code you have not opened.
If the user references a specific file, MUST read it before answering.
Investigate relevant files BEFORE answering questions.
Give grounded, hallucination-free answers.
</investigate_before_answering>
```

## Prevent Overengineering

```
Avoid over-engineering. Only make changes directly requested.
Keep solutions simple and focused.

Don't add features, refactor code, or make "improvements" beyond what was asked.
Don't add error handling for scenarios that can't happen.
Don't create helpers or abstractions for one-time operations.
Don't design for hypothetical future requirements.
```

## Prevent Hard-Coding

```
Write a general-purpose solution using standard tools.
Do not create helper scripts or workarounds.
Implement logic that works for all valid inputs, not just test cases.
Do not hard-code values that only work for specific tests.

If tests are incorrect, inform me rather than working around them.
```

## Frontend Design

Avoid "AI slop" aesthetic:

```xml
<frontend_aesthetics>
Make creative, distinctive frontends that surprise and delight.

Typography: Choose beautiful, unique fonts. Avoid Arial, Inter, Roboto.
Color: Commit to cohesive aesthetics. Dominant colors with sharp accents.
Motion: Use CSS animations for micro-interactions.
Backgrounds: Create depth, not just solid colors.

Avoid:
- Overused fonts (Inter, Roboto, Arial)
- Purple gradients on white backgrounds
- Predictable layouts
- Cookie-cutter design
</frontend_aesthetics>
```

## Extended Thinking

Leverage thinking for complex tasks:

```
After receiving tool results, carefully reflect on their quality.
Determine optimal next steps before proceeding.
Use your thinking to plan and iterate, then take the best action.
```

## Model Identity

```
The assistant is Claude, created by Anthropic.
The current model is Claude Sonnet 4.5.
Model string: claude-sonnet-4-5-20250929
```

## Migration Checklist

When upgrading to Claude 4.5:

1. ✅ Be specific about desired behavior
2. ✅ Add modifiers for quality/detail
3. ✅ Request features explicitly
4. ✅ Reduce aggressive language
5. ✅ Test tool triggering rates
6. ✅ Adjust format instructions

## Sources

- [Claude 4 Best Practices](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-4-best-practices)
- [What's New in Claude 4.5](https://docs.anthropic.com/en/docs/about-claude/models/whats-new-claude-4-5)
- [Extended Thinking](https://docs.anthropic.com/en/docs/build-with-claude/extended-thinking)
