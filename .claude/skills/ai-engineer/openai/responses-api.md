# OpenAI Responses API (New 2025)

The Responses API is OpenAI's new recommended API for text generation, released March 2025. It combines the best of Chat Completions and Assistants APIs with built-in tools.

## Why Use Responses API?

- **Built-in tools:** web_search, file_search, code_interpreter, computer_use
- **Agentic loops:** Model can call multiple tools in one request
- **Simpler:** Unified interface for chat and tools
- **Recommended:** OpenAI's preferred API for new projects

## Endpoint

```
POST https://api.openai.com/v1/responses
```

## Basic Request

### curl
```bash
curl https://api.openai.com/v1/responses \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-4.1",
    "input": "What is the capital of France?"
  }'
```

### With Developer Instructions
```bash
curl https://api.openai.com/v1/responses \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-4.1",
    "input": [
      {"role": "developer", "content": "You are a helpful assistant. Be concise."},
      {"role": "user", "content": "What is the capital of France?"}
    ]
  }'
```

### Python
```python
from openai import OpenAI

client = OpenAI()

response = client.responses.create(
    model="gpt-4.1",
    input=[
        {"role": "developer", "content": "You are a helpful assistant."},
        {"role": "user", "content": "What is the capital of France?"}
    ]
)

print(response.output_text)
```

## Key Differences from Chat Completions

| Feature | Chat Completions | Responses API |
|---------|------------------|---------------|
| Input field | `messages` | `input` |
| System role | `role: "system"` | `role: "developer"` |
| Tools | Manual function calling | Built-in + custom |
| Multi-tool | Requires orchestration | Automatic loops |
| Recommended for | Legacy code | New projects |

## Built-in Tools

### Web Search
```bash
curl https://api.openai.com/v1/responses \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-4.1",
    "tools": [{"type": "web_search"}],
    "input": "What happened in tech news today?"
  }'
```

### Web Search with Domain Filtering
```bash
curl https://api.openai.com/v1/responses \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-4.1",
    "tools": [{
      "type": "web_search",
      "filters": {
        "allowed_domains": [
          "docs.python.org",
          "stackoverflow.com",
          "github.com"
        ]
      }
    }],
    "input": "How do I use asyncio in Python?"
  }'
```

**Domain filter limits:** Up to 100 URLs in the allow-list.

### File Search
```python
response = client.responses.create(
    model="gpt-4.1",
    tools=[{"type": "file_search"}],
    input="Search my documents for information about Q4 revenue"
)
```

### Code Interpreter
```python
response = client.responses.create(
    model="gpt-4.1",
    tools=[{"type": "code_interpreter"}],
    input="Calculate the factorial of 20 and plot a bar chart"
)
```

### Computer Use
```python
response = client.responses.create(
    model="gpt-4.1",
    tools=[{"type": "computer_use"}],
    input="Open the browser and go to example.com"
)
```

### Combining Multiple Tools
```python
response = client.responses.create(
    model="gpt-4.1",
    tools=[
        {"type": "web_search"},
        {"type": "code_interpreter"},
        {
            "type": "function",
            "function": {
                "name": "save_result",
                "description": "Save a result to the database",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "data": {"type": "string"}
                    },
                    "required": ["data"]
                }
            }
        }
    ],
    input="Search for today's Bitcoin price, calculate 30-day average, save it"
)
```

## Custom Functions

```python
response = client.responses.create(
    model="gpt-4.1",
    tools=[{
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get current weather for a location",
            "strict": True,  # Recommended: guarantees schema adherence
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "City name"
                    },
                    "unit": {
                        "type": "string",
                        "enum": ["celsius", "fahrenheit"]
                    }
                },
                "required": ["location"],
                "additionalProperties": False
            }
        }
    }],
    input="What's the weather in Paris?"
)
```

## Web Search Types

### Non-reasoning Search (Fast)
The model passes the query directly to web search and returns results. Fast, ideal for quick lookups.

### Agentic Search with Reasoning Models
When using o3 or o3-mini, the model:
1. Analyzes the query
2. Performs web searches as part of chain of thought
3. Analyzes results
4. Decides whether to keep searching
5. Synthesizes final answer

```python
response = client.responses.create(
    model="o3",
    tools=[{"type": "web_search"}],
    reasoning={"effort": "high"},
    input="Compare the latest AI regulations in EU vs US"
)
```

## Getting Sources from Web Search

```bash
curl https://api.openai.com/v1/responses \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-4.1",
    "tools": [{"type": "web_search"}],
    "include": ["web_search_call.action.sources"],
    "input": "What is the current price of Bitcoin?"
  }'
```

The `sources` field returns all URLs consulted, labeled as:
- Regular web sources
- `oai-sports` - Sports data feeds
- `oai-weather` - Weather data feeds
- `oai-finance` - Financial data feeds

## Reasoning Parameters (for o3/o4-mini)

```python
response = client.responses.create(
    model="o3",
    reasoning={
        "effort": "low"  # "low", "medium", or "high"
    },
    input="Solve this complex math problem..."
)
```

| Effort | Use Case |
|--------|----------|
| `low` | Quick questions, simple tasks |
| `medium` | Default, balanced |
| `high` | Complex reasoning, research |

## Tool Choice

```python
# Auto (default) - model decides
tool_choice="auto"

# Required - must use a tool
tool_choice="required"

# Specific function
tool_choice={"type": "function", "function": {"name": "get_weather"}}

# None - no tools
tool_choice="none"
```

## Streaming

```python
stream = client.responses.create(
    model="gpt-4.1",
    input="Tell me a long story",
    stream=True
)

for event in stream:
    if event.type == "response.output_text.delta":
        print(event.delta, end="")
```

## Response Format

```json
{
  "id": "resp_abc123",
  "object": "response",
  "created_at": 1704067200,
  "model": "gpt-4.1",
  "output": [
    {
      "type": "message",
      "role": "assistant",
      "content": [
        {
          "type": "text",
          "text": "The capital of France is Paris."
        }
      ]
    }
  ],
  "output_text": "The capital of France is Paris.",
  "usage": {
    "input_tokens": 25,
    "output_tokens": 8,
    "total_tokens": 33
  }
}
```

## Migration from Chat Completions

### Before (Chat Completions)
```python
response = client.chat.completions.create(
    model="gpt-4.1",
    messages=[
        {"role": "system", "content": "You are helpful."},
        {"role": "user", "content": "Hello"}
    ]
)
print(response.choices[0].message.content)
```

### After (Responses API)
```python
response = client.responses.create(
    model="gpt-4.1",
    input=[
        {"role": "developer", "content": "You are helpful."},
        {"role": "user", "content": "Hello"}
    ]
)
print(response.output_text)
```

## Best Practices

1. **Use `strict: true`** for function definitions
2. **Use `developer` role** instead of `system`
3. **Combine tools** for complex agentic tasks
4. **Use domain filtering** for web search quality
5. **Include sources** when you need citations

## Official Documentation
- Responses API: https://platform.openai.com/docs/api-reference/responses
- Web Search: https://platform.openai.com/docs/guides/tools-web-search
- Migration Guide: https://platform.openai.com/docs/guides/migrate-to-responses
