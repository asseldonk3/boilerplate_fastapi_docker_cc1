# OpenAI Chat Completions API

The Chat Completions API is the legacy (but stable) way to interact with OpenAI models. For new projects, consider the [Responses API](./responses-api.md).

## Endpoint

```
POST https://api.openai.com/v1/chat/completions
```

## Authentication

```bash
Authorization: Bearer $OPENAI_API_KEY
```

Optional headers for organizations:
```bash
OpenAI-Organization: $ORGANIZATION_ID
OpenAI-Project: $PROJECT_ID
```

## Basic Request

### curl
```bash
curl https://api.openai.com/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -d '{
    "model": "gpt-4.1",
    "messages": [
      {"role": "system", "content": "You are a helpful assistant."},
      {"role": "user", "content": "What is the capital of France?"}
    ]
  }'
```

### Python
```python
from openai import OpenAI

client = OpenAI()  # Uses OPENAI_API_KEY env var

response = client.chat.completions.create(
    model="gpt-4.1",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "What is the capital of France?"}
    ]
)

print(response.choices[0].message.content)
```

### JavaScript/TypeScript
```typescript
import OpenAI from 'openai';

const openai = new OpenAI();  // Uses OPENAI_API_KEY env var

const response = await openai.chat.completions.create({
  model: "gpt-4.1",
  messages: [
    { role: "system", content: "You are a helpful assistant." },
    { role: "user", content: "What is the capital of France?" }
  ]
});

console.log(response.choices[0].message.content);
```

## Request Parameters

### Required
| Parameter | Type | Description |
|-----------|------|-------------|
| `model` | string | Model ID (e.g., `gpt-4.1`, `o3-mini`) |
| `messages` | array | Array of message objects |

### Message Object
```json
{
  "role": "system" | "user" | "assistant" | "tool",
  "content": "string or array of content parts",
  "name": "optional identifier",
  "tool_calls": "array of tool calls (assistant only)",
  "tool_call_id": "ID when role is tool"
}
```

### Optional Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `temperature` | number | 1 | Randomness (0-2). Lower = more deterministic |
| `top_p` | number | 1 | Nucleus sampling. Alternative to temperature |
| `n` | integer | 1 | Number of completions to generate |
| `stream` | boolean | false | Stream partial responses |
| `stop` | string/array | null | Stop sequences |
| `max_tokens` | integer | - | Maximum tokens to generate |
| `max_completion_tokens` | integer | - | Preferred over max_tokens |
| `presence_penalty` | number | 0 | Penalize new topics (-2 to 2) |
| `frequency_penalty` | number | 0 | Penalize repetition (-2 to 2) |
| `logit_bias` | object | null | Modify token likelihood |
| `response_format` | object | - | Force JSON output |
| `seed` | integer | - | For reproducibility |
| `tools` | array | - | Function definitions |
| `tool_choice` | string/object | "auto" | Control tool usage |
| `parallel_tool_calls` | boolean | true | Allow parallel calls |
| `user` | string | - | End-user identifier |

## Response Format

```json
{
  "id": "chatcmpl-abc123",
  "object": "chat.completion",
  "created": 1704067200,
  "model": "gpt-4.1",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "The capital of France is Paris."
      },
      "logprobs": null,
      "finish_reason": "stop"
    }
  ],
  "usage": {
    "prompt_tokens": 25,
    "completion_tokens": 8,
    "total_tokens": 33
  }
}
```

### Finish Reasons
| Reason | Description |
|--------|-------------|
| `stop` | Natural stop or hit stop sequence |
| `length` | Hit max_tokens limit |
| `tool_calls` | Model wants to call a tool |
| `content_filter` | Content was filtered |

## Streaming

### Python
```python
stream = client.chat.completions.create(
    model="gpt-4.1",
    messages=[{"role": "user", "content": "Tell me a story"}],
    stream=True
)

for chunk in stream:
    if chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end="")
```

### curl
```bash
curl https://api.openai.com/v1/chat/completions \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-4.1",
    "messages": [{"role": "user", "content": "Tell me a story"}],
    "stream": true
  }'
```

Stream response format (Server-Sent Events):
```
data: {"id":"chatcmpl-...","choices":[{"delta":{"content":"Once"}}]}
data: {"id":"chatcmpl-...","choices":[{"delta":{"content":" upon"}}]}
data: [DONE]
```

## JSON Mode

Force JSON output:
```python
response = client.chat.completions.create(
    model="gpt-4.1",
    messages=[
        {"role": "system", "content": "Output valid JSON only."},
        {"role": "user", "content": "List 3 colors"}
    ],
    response_format={"type": "json_object"}
)
```

**Important:** You MUST mention "JSON" in your prompt when using JSON mode.

## Vision (Image Input)

```python
response = client.chat.completions.create(
    model="gpt-4.1",
    messages=[
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "What's in this image?"},
                {
                    "type": "image_url",
                    "image_url": {
                        "url": "https://example.com/image.jpg",
                        # Or base64: "data:image/jpeg;base64,{base64_string}"
                        "detail": "auto"  # "low", "high", or "auto"
                    }
                }
            ]
        }
    ]
)
```

## Multi-turn Conversation

```python
messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Hi, my name is Alice."},
    {"role": "assistant", "content": "Hello Alice! How can I help you today?"},
    {"role": "user", "content": "What's my name?"}
]

response = client.chat.completions.create(
    model="gpt-4.1",
    messages=messages
)
# Response: "Your name is Alice."
```

## Error Handling

```python
from openai import OpenAI, APIError, RateLimitError, AuthenticationError

client = OpenAI()

try:
    response = client.chat.completions.create(
        model="gpt-4.1",
        messages=[{"role": "user", "content": "Hello"}]
    )
except AuthenticationError:
    print("Invalid API key")
except RateLimitError:
    print("Rate limit exceeded, retry with backoff")
except APIError as e:
    print(f"API error: {e}")
```

## Common Patterns

### System Prompt Best Practices
```python
# Be specific and clear
system_prompt = """You are a technical support assistant for a software company.
- Always ask clarifying questions before providing solutions
- Format code examples with syntax highlighting
- If unsure, admit it and suggest contacting human support
"""
```

### Temperature Guidelines
| Use Case | Temperature |
|----------|-------------|
| Code generation | 0 - 0.3 |
| Factual Q&A | 0 - 0.5 |
| Creative writing | 0.7 - 1.0 |
| Brainstorming | 1.0 - 1.5 |

## Migration to Responses API

The Responses API is recommended for new projects. Key differences:
- Uses `input` instead of `messages`
- Uses `developer` role instead of `system`
- Built-in tools (web_search, file_search, etc.)
- Agentic loop support

See [Responses API](./responses-api.md) for details.

## Official Documentation
- API Reference: https://platform.openai.com/docs/api-reference/chat
- Text Generation Guide: https://platform.openai.com/docs/guides/text
