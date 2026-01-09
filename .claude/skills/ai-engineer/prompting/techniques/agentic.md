# Agentic Prompting Techniques

Techniques for LLMs that use tools, take actions, and work on long-horizon tasks.

## ReAct Framework

**Source:** [Yao et al., 2022](https://arxiv.org/abs/2210.03629)

ReAct (Reason + Act) combines reasoning traces with action execution.

### Pattern

```
Thought: [reasoning about current state]
Action: [tool/action to take]
Observation: [result of action]
... (repeat until done)
Thought: [final reasoning]
Answer: [final answer]
```

### Example

```
Question: What is the population of the capital of France?

Thought: I need to find the capital of France first.
Action: search("capital of France")
Observation: Paris is the capital of France.

Thought: Now I need the population of Paris.
Action: search("population of Paris")
Observation: Paris has a population of approximately 2.1 million.

Thought: I have the answer.
Answer: The population of Paris, the capital of France, is approximately 2.1 million.
```

### Implementation

```python
def react_agent(question, tools):
    prompt = f"""
    Answer this question using available tools: {question}

    Available tools: {list(tools.keys())}

    Format each step as:
    Thought: [your reasoning]
    Action: tool_name(params)

    I will provide the Observation after each action.
    Continue until you have the final answer.
    """

    while True:
        response = llm(prompt)

        if "Answer:" in response:
            return extract_answer(response)

        action = extract_action(response)
        observation = tools[action.name](action.params)
        prompt += f"\nObservation: {observation}\n"
```

---

## Tool Use Configuration

### GPT-5.2 Tool Preambles

GPT-5.2 provides planning before tool use:

```python
response = client.responses.create(
    model="gpt-5.2",
    tools=[...],
    input="Your task"
)
# Model will explain its plan before executing tools
```

Control verbosity:

```
<tool_preamble_config>
- Provide brief plans (1-2 sentences) before tool sequences
- Skip preambles for single, obvious tool calls
- Always explain when switching strategies
</tool_preamble_config>
```

### Gemini Tool Configuration

```python
response = client.models.generate_content(
    model="gemini-3-flash-preview",
    tools=[...],
    tool_config={
        "function_calling_config": {
            "mode": "AUTO"  # AUTO, ANY, NONE
        }
    }
)
```

### Claude Tool Use

```xml
<tool_use_instructions>
When using tools:
1. Plan your approach before calling tools
2. Call independent tools in parallel
3. Verify results before proceeding
4. Report outcomes, not process
</tool_use_instructions>
```

---

## Status Updates

### Brief, Outcome-Focused Updates

```
<status_update_rules>
When providing status updates:
- Keep to 1-2 sentences only
- Update when starting new phases or discovering plan changes
- Do NOT narrate routine tool calls
- Each update must include concrete outcomes: "Found X", "Confirmed Y"
- Don't expand scope without flagging as optional
</status_update_rules>
```

### Example Good vs Bad

```
# Bad - too verbose
"I'm now going to read the file. Reading the file... I have read the file.
Now I will analyze it. Analyzing... The analysis shows..."

# Good - outcome-focused
"Found 3 security vulnerabilities in auth.py. Fixing the SQL injection first."
```

---

## Error Recovery

```
<error_recovery>
If you encounter an error:
1. Analyze the root cause (don't just retry blindly)
2. Attempt a fix
3. If still failing after 3 attempts:
   - Explain what you tried
   - Why it failed
   - Suggest alternative approaches
   - Ask for guidance if blocked
</error_recovery>
```

### Graceful Degradation

```
<graceful_degradation>
If a tool is unavailable or failing:
1. Try alternative tools that could achieve the same goal
2. If no alternatives, explain what you would have done
3. Provide partial results where possible
4. Clearly mark incomplete work
</graceful_degradation>
```

---

## Long-Horizon Task Management

### State Persistence

```xml
<state_management>
For multi-step tasks:

1. Use structured files for status tracking:
   - tasks.json: Current state of all subtasks
   - progress.md: Freeform notes and context

2. Update state after each major milestone

3. Before continuing work:
   - Read state files
   - Verify what's been completed
   - Plan next steps

4. Use git for checkpoints:
   - Commit after completing subtasks
   - Use descriptive commit messages
</state_management>
```

### Task Breakdown

```
<task_decomposition>
For complex tasks:
1. Break into independent subtasks
2. Identify dependencies between subtasks
3. Execute independent tasks in parallel where possible
4. Track progress explicitly
5. Validate each subtask before proceeding
</task_decomposition>
```

### Context Window Management

```
<context_management>
When approaching context limits:
1. Summarize completed work
2. Save detailed state to files
3. Identify what context is essential to continue
4. Document assumptions and decisions made
5. Create a handoff note for the next window
</context_management>
```

---

## Parallel Execution

### When to Parallelize

```
<parallel_execution>
Execute in parallel when:
- Multiple file reads (no dependencies)
- Independent searches
- Gathering information from multiple sources

Execute sequentially when:
- Output of one tool is input to another
- Order matters (write then verify)
- Resource conflicts possible
</parallel_execution>
```

### Implementation Pattern

```python
# Good: Parallel independent reads
await Promise.all([
    read_file("config.json"),
    read_file("schema.json"),
    read_file("data.json")
])

# Good: Sequential dependent operations
result = await process_data()
await write_file("output.json", result)
await verify_output("output.json")
```

---

## Subagent Orchestration

### Natural Delegation

Modern models (Claude 4.5, GPT-5.2) can delegate naturally:

```
<subagent_config>
You can delegate tasks to specialized subagents when beneficial.

Delegate when:
- Task requires fresh context window
- Specialized expertise needed
- Parallel execution would help

Available subagents:
- research_agent: Deep web research
- code_agent: Complex code changes
- review_agent: Code review and testing
</subagent_config>
```

### Conservative Mode

```
<conservative_delegation>
Only delegate to subagents when the task clearly benefits
from a separate agent with a new context window.
Prefer handling tasks yourself when context is sufficient.
</conservative_delegation>
```

---

## Verification Patterns

### Before Critical Actions

```
<pre_action_verification>
Before destructive or irreversible actions:
1. State what you're about to do
2. Show the specific parameters/values
3. Wait for confirmation if configured
4. Create backup/checkpoint if possible
</pre_action_verification>
```

### Post-Execution Verification

```
<post_action_verification>
After write operations:
1. Verify the change was applied
2. Run relevant tests
3. Check for side effects
4. Report what changed and where
</post_action_verification>
```

---

## Risk Assessment

```xml
<risk_assessment>
Before taking actions, assess risk:

HIGH RISK (require confirmation):
- Deleting files or data
- Modifying production systems
- Financial transactions
- External communications

MEDIUM RISK (proceed with caution):
- Modifying shared configuration
- Installing dependencies
- API calls with side effects

LOW RISK (proceed normally):
- Reading files
- Running tests
- Local development changes
</risk_assessment>
```

---

## Agentic Coding Patterns

### Investigate Before Acting

```
<investigate_first>
ALWAYS read and understand relevant files before proposing edits.
Do not speculate about code you have not inspected.
If the user references a file, MUST open it before answering.
Be rigorous in searching for key facts.
Review style and conventions before implementing.
</investigate_first>
```

### Minimal Changes

```
<minimal_changes>
Make the smallest change that solves the problem.
Don't refactor surrounding code unless asked.
Don't add "improvements" beyond the request.
Don't create abstractions for one-time operations.
</minimal_changes>
```

### Test-Driven

```
<test_driven>
When implementing features:
1. Write or identify relevant tests first
2. Make changes to pass tests
3. Verify tests pass
4. Don't modify tests to pass (unless tests are wrong)
</test_driven>
```

---

## Multi-Model Orchestration

When using multiple models:

```python
# Route by task type
def route_task(task):
    if task.type == "reasoning":
        return call_o3(task)
    elif task.type == "coding":
        return call_gpt52_codex(task)
    elif task.type == "simple":
        return call_gemini_flash_lite(task)
    else:
        return call_gpt52(task)
```

```
<orchestration_rules>
- Use fast models for simple subtasks
- Use reasoning models for planning
- Use code models for implementation
- Aggregate results from parallel model calls
- Verify cross-model consistency
</orchestration_rules>
```

## Sources

- [ReAct Paper](https://arxiv.org/abs/2210.03629)
- [OpenAI Responses API](https://platform.openai.com/docs/guides/responses)
- [Claude Agentic Best Practices](https://docs.anthropic.com)
- [Gemini Agentic Configuration](https://ai.google.dev/gemini-api/docs/prompting-strategies)
