# Reasoning Models Prompting Guide (o3, o3-mini, o4-mini)

OpenAI's reasoning models (o-series) are fundamentally different from GPT models. They're trained to think longer and harder about complex problems, making them excellent for planning, strategy, and multi-step reasoning.

## Key Differences: GPT vs Reasoning Models

| Aspect | GPT Models (GPT-4.1) | Reasoning Models (o3) |
|--------|---------------------|----------------------|
| Approach | Follow step-by-step guidance | Figure out approach themselves |
| Prompting style | Tell HOW to do it | Tell WHAT to do |
| Best analogy | Junior colleague | Senior colleague |
| Planning | You provide the plan | Model creates the plan |
| Thinking | Fast, reactive | Extended, deliberate |

## Core Principle: State WHAT, Not HOW

### GPT-4.1 (Tell it how)
```
To solve this math problem:
1. First, identify the variables
2. Then, set up the equation
3. Next, solve for x
4. Finally, verify your answer

Problem: [math problem]
```

### o3 (Tell it what)
```
Solve this math problem and explain your reasoning.

Problem: [math problem]
```

The reasoning model will figure out the best approach itself.

## Using the `developer` Role

In the Responses API, reasoning models respond better to the `developer` role:

```python
response = client.responses.create(
    model="o3",
    input=[
        {"role": "developer", "content": "You are a math tutor. Show your work."},
        {"role": "user", "content": "Solve: 3x + 7 = 22"}
    ]
)
```

The `developer` role signals to reasoning models that this is an authoritative instruction.

## Reasoning Effort Levels

Control how much the model "thinks" before responding:

```python
response = client.responses.create(
    model="o3",
    reasoning={"effort": "high"},  # low, medium, or high
    input="Design a distributed caching system for a social media app"
)
```

| Effort | Use Case | Thinking Time |
|--------|----------|---------------|
| `low` | Simple questions, quick lookups | Minimal |
| `medium` | Standard problems (default) | Moderate |
| `high` | Complex reasoning, research, math | Extended |

## Best Use Cases for Reasoning Models

### 1. Complex Planning
```
Design an architecture for a real-time collaborative document editor
that supports:
- 10,000 concurrent users
- Conflict resolution
- Offline mode
- Version history

Consider trade-offs between consistency and availability.
```

### 2. Multi-step Problem Solving
```
A company has 3 warehouses and 5 stores. Given the following
shipping costs and inventory levels, determine the optimal
distribution plan to minimize costs while meeting all demand.

[data tables here]
```

### 3. Ambiguous Decision Making
```
Review these 5 architectural proposals for our authentication system.
Consider security, scalability, developer experience, and maintenance cost.
Recommend the best option with detailed justification.

[proposals here]
```

### 4. Code Architecture
```
Given this codebase structure, identify the best way to introduce
a new payment provider without modifying existing code paths.
Consider SOLID principles and testing implications.

[codebase description]
```

## Function Calling with Reasoning Models

Reasoning models can use tools effectively but need clear guidance:

### Function Descriptions
```python
tools = [{
    "type": "function",
    "function": {
        "name": "search_codebase",
        "description": """Search the codebase for relevant code.

        When to use: When you need to understand existing code patterns
        or find specific implementations.

        Returns: List of file paths and code snippets matching the query.""",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Natural language description of what to find"
                }
            },
            "required": ["query"]
        }
    }
}]
```

### Developer Prompt for Tool Use
```python
response = client.responses.create(
    model="o3",
    input=[
        {
            "role": "developer",
            "content": """You are an expert software engineer with access to tools.

            Available tools:
            - search_codebase: Find relevant code
            - read_file: Read file contents
            - write_file: Write/update files
            - run_tests: Execute test suite

            When solving problems:
            1. First understand the codebase structure
            2. Plan your approach
            3. Make targeted changes
            4. Verify with tests"""
        },
        {"role": "user", "content": "Refactor the authentication module to use JWT"}
    ],
    tools=tools
)
```

## Tool Limits

Reasoning models handle tools well within these bounds:
- **Max tools:** ~100 (optimal: 10-20)
- **Max arguments per tool:** ~20

## What NOT to Do

### Don't Over-specify Steps
```
# Bad - micromanaging a reasoning model
Step 1: Read the problem
Step 2: Identify the key variables
Step 3: Consider approach A
Step 4: Consider approach B
Step 5: Compare approaches
Step 6: Choose the best one
Step 7: Implement it
Step 8: Verify

# Good - let it reason
Solve this problem. Explain your reasoning process.
```

### Don't Use Low Temperature
Reasoning models don't benefit from temperature tuning the same way. Their reasoning process is internal.

### Don't Expect Instant Responses
Reasoning takes time. High-effort reasoning on complex problems may take 30+ seconds.

## Streaming with Reasoning Models

When streaming, you'll see the reasoning process:

```python
stream = client.responses.create(
    model="o3",
    input="Prove that there are infinitely many prime numbers",
    stream=True
)

for event in stream:
    if event.type == "response.reasoning.delta":
        print(f"[Thinking] {event.delta}", end="")
    elif event.type == "response.output_text.delta":
        print(f"[Answer] {event.delta}", end="")
```

## Model Selection: o3 vs o3-mini vs GPT-4.1

| Task | Best Model | Why |
|------|------------|-----|
| Quick code fix | GPT-4.1 | Fast, doesn't need deep reasoning |
| Algorithm design | o3 | Benefits from extended thinking |
| Simple Q&A | GPT-4.1 nano | Fast and cheap |
| Architecture decision | o3 | Complex trade-offs |
| Bulk data processing | GPT-4.1 mini | Cost-effective |
| Math proofs | o3 with high effort | Extended reasoning |
| Code review | GPT-4.1 | Pattern matching |
| Root cause analysis | o3-mini | Good reasoning, faster than o3 |

## Combining with Web Search

Reasoning models + web search = powerful research:

```python
response = client.responses.create(
    model="o3",
    tools=[{"type": "web_search"}],
    reasoning={"effort": "high"},
    input="""Research the current state of quantum computing applications
    in drug discovery. Compare approaches from at least 3 major companies.
    Analyze technical feasibility and timeline predictions."""
)
```

The model will:
1. Plan search queries
2. Execute searches
3. Analyze results
4. Decide if more searching is needed
5. Synthesize findings

## Cost Considerations

Reasoning models charge for "thinking tokens" as well as output:

| Model | Input $/1M | Output $/1M | Notes |
|-------|-----------|-------------|-------|
| o3 | $2.00 | $8.00 | Includes reasoning tokens |
| o3-mini | $0.55 | $2.20 | Faster, cheaper |
| o3-pro | Higher | Higher | Most compute |

For simple tasks, GPT-4.1 is more cost-effective.

## Best Practices Summary

1. **State the goal, not the steps**
2. **Use `developer` role** for system instructions
3. **Match effort to task complexity**
4. **Provide rich context** - these models use it well
5. **Be patient** - reasoning takes time
6. **Use for complex tasks** - don't waste on simple ones
7. **Write detailed function descriptions**

## Official Resources
- Reasoning Best Practices: https://platform.openai.com/docs/guides/reasoning-best-practices
- o3/o4-mini Function Calling: https://cookbook.openai.com/examples/o-series/o3o4-mini_prompting_guide
- Model Selection Guide: https://cookbook.openai.com/examples/partners/model_selection_guide
