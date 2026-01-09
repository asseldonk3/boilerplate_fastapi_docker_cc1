# Gemini Generate Content API

The `generateContent` endpoint is the core API for interacting with Gemini models.

## Endpoints

**Google AI (ai.google.dev):**
```
POST https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent
POST https://generativelanguage.googleapis.com/v1beta/models/{model}:streamGenerateContent
```

**Vertex AI (Google Cloud):**
```
POST https://{region}-aiplatform.googleapis.com/v1/projects/{project}/locations/{region}/publishers/google/models/{model}:generateContent
```

## Authentication

### API Key (Google AI)
```bash
# Set environment variable
export GEMINI_API_KEY="your-api-key"

# Use in URL
?key=$GEMINI_API_KEY
```

### SDK Auto-detection
```python
from google import genai

# Automatically uses GEMINI_API_KEY env var
client = genai.Client()
```

### Vertex AI (Service Account)
```python
from google import genai

client = genai.Client(
    vertexai=True,
    project="your-project-id",
    location="us-central1"
)
```

## Basic Request

### Python SDK (Recommended)
```python
from google import genai

client = genai.Client()

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Explain quantum computing in simple terms"
)

print(response.text)
```

### REST API (curl)
```bash
curl "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key=$GEMINI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "contents": [{
      "parts": [{"text": "Hello, how are you?"}]
    }]
  }'
```

### JavaScript/TypeScript
```typescript
import { GoogleGenAI } from '@google/genai';

const genai = new GoogleGenAI(process.env.GEMINI_API_KEY);
const model = genai.getGenerativeModel({ model: 'gemini-2.5-flash' });

const result = await model.generateContent('Explain AI');
console.log(result.response.text());
```

## Request Structure

### Full Request Format
```python
from google import genai
from google.genai import types

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=[
        types.Content(
            role="user",
            parts=[types.Part(text="What is the capital of France?")]
        )
    ],
    config=types.GenerateContentConfig(
        temperature=1.0,
        top_p=0.95,
        top_k=40,
        max_output_tokens=8192,
        stop_sequences=["END"],
        response_mime_type="text/plain",
        system_instruction="You are a helpful geography expert."
    )
)
```

### REST API Full Format
```json
{
  "contents": [{
    "role": "user",
    "parts": [{"text": "Your message here"}]
  }],
  "systemInstruction": {
    "parts": [{"text": "You are a helpful assistant."}]
  },
  "generationConfig": {
    "temperature": 1.0,
    "topP": 0.95,
    "topK": 40,
    "maxOutputTokens": 8192,
    "stopSequences": ["END"],
    "responseMimeType": "text/plain"
  },
  "safetySettings": [{
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  }]
}
```

## Generation Config Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `temperature` | float | 1.0 | Randomness (0-2). Keep at 1.0 for Gemini 3 |
| `top_p` | float | 0.95 | Nucleus sampling threshold |
| `top_k` | int | 40 | Top-k sampling |
| `max_output_tokens` | int | Model-dependent | Maximum tokens to generate |
| `stop_sequences` | array | [] | Strings that stop generation |
| `response_mime_type` | string | "text/plain" | Output format |
| `candidate_count` | int | 1 | Number of responses |

## System Instructions

```python
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="What should I cook tonight?",
    config=types.GenerateContentConfig(
        system_instruction="""You are a professional chef.
        - Always suggest healthy options first
        - Include cooking time estimates
        - Consider common dietary restrictions"""
    )
)
```

## Multi-turn Conversation

```python
# Build conversation history
history = [
    types.Content(role="user", parts=[types.Part(text="My name is Alice")]),
    types.Content(role="model", parts=[types.Part(text="Hello Alice! Nice to meet you.")]),
    types.Content(role="user", parts=[types.Part(text="What's my name?")])
]

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=history
)
# Response: "Your name is Alice."
```

## Streaming

### Python SDK
```python
response = client.models.generate_content_stream(
    model="gemini-2.5-flash",
    contents="Write a long story about a robot"
)

for chunk in response:
    print(chunk.text, end="")
```

### REST API (SSE)
```bash
curl "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:streamGenerateContent?key=$GEMINI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"contents": [{"parts": [{"text": "Write a poem"}]}]}'
```

## Multimodal Input

### Image Input
```python
import base64

# From URL
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=[
        types.Part(text="What's in this image?"),
        types.Part(
            inline_data=types.Blob(
                mime_type="image/jpeg",
                data=base64.b64encode(image_bytes).decode()
            )
        )
    ]
)

# From file
with open("image.jpg", "rb") as f:
    image_data = base64.b64encode(f.read()).decode()

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=[
        types.Part(text="Describe this image"),
        types.Part(inline_data=types.Blob(
            mime_type="image/jpeg",
            data=image_data
        ))
    ]
)
```

### Video Input
```python
# Upload video first (for large files)
video_file = client.files.upload(path="video.mp4")

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=[
        types.Part(text="Summarize this video"),
        types.Part(file_data=types.FileData(
            file_uri=video_file.uri,
            mime_type="video/mp4"
        ))
    ]
)
```

### PDF Input
```python
# Upload PDF
pdf_file = client.files.upload(path="document.pdf")

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=[
        types.Part(text="Extract key points from this document"),
        types.Part(file_data=types.FileData(
            file_uri=pdf_file.uri,
            mime_type="application/pdf"
        ))
    ]
)
```

### Audio Input
```python
audio_file = client.files.upload(path="audio.mp3")

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=[
        types.Part(text="Transcribe this audio"),
        types.Part(file_data=types.FileData(
            file_uri=audio_file.uri,
            mime_type="audio/mp3"
        ))
    ]
)
```

## JSON Output

```python
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="List 3 programming languages with their paradigms",
    config=types.GenerateContentConfig(
        response_mime_type="application/json"
    )
)

import json
data = json.loads(response.text)
```

## Thinking Mode

Enable extended reasoning for complex problems—or disable it entirely for maximum speed.

### Thinking Budget Configuration

```python
from google import genai
from google.genai import types

# MAXIMUM SPEED: Disable thinking entirely
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Simple question here",
    config=types.GenerateContentConfig(
        thinking_config=types.ThinkingConfig(
            thinking_budget=0  # No thinking = fastest response
        )
    )
)

# DYNAMIC: Model decides based on complexity (recommended default)
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Your question",
    config=types.GenerateContentConfig(
        thinking_config=types.ThinkingConfig(
            thinking_budget=-1  # Dynamic allocation
        )
    )
)

# COMPLEX REASONING: High budget for difficult problems
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Solve this complex math problem: ...",
    config=types.GenerateContentConfig(
        thinking_config=types.ThinkingConfig(
            thinking_budget=10000  # Max thinking tokens
        )
    )
)

# Access thinking process
print("Thinking:", response.candidates[0].content.parts[0].thought)
print("Answer:", response.text)
```

### Thinking Budget Ranges by Model

| Model | Min | Max | Default | Notes |
|-------|-----|-----|---------|-------|
| Gemini 2.5 Pro | 128 | 32,768 | 8,192 | High default for complex tasks |
| Gemini 2.5 Flash | **0** | 24,576 | Dynamic (-1) | Set 0 for max speed |
| Gemini 2.5 Flash-Lite | 512 | 24,576 | **0** (disabled) | Speed-optimized by default |

### Gemini 3 Thinking Levels

Gemini 3 introduces a simpler `thinking_level` parameter instead of token budgets:

```python
from google.genai.types import ThinkingConfig

# MINIMAL: Lowest latency (Gemini 3 Flash only)
# Best for chat, high-throughput apps
config = types.GenerateContentConfig(
    thinking_config=ThinkingConfig(thinking_level="MINIMAL")
)

# LOW: Standard queries
config = types.GenerateContentConfig(
    thinking_config=ThinkingConfig(thinking_level="LOW")
)

# MEDIUM: Balanced (default)
config = types.GenerateContentConfig(
    thinking_config=ThinkingConfig(thinking_level="MEDIUM")
)

# HIGH: Complex reasoning (default for dynamic)
config = types.GenerateContentConfig(
    thinking_config=ThinkingConfig(thinking_level="HIGH")
)
```

**Note:** `MINIMAL` doesn't guarantee thinking is completely off—the model may still think briefly for complex coding tasks. It minimizes latency for most queries.

### Speed vs Cost Optimization

| Goal | Setting | Use Case |
|------|---------|----------|
| Fastest response | `thinking_budget=0` | Chat, classification, simple Q&A |
| Cost-efficient | `thinking_budget=-1` (dynamic) | General use—pays only when needed |
| Best quality | `thinking_budget=10000+` | Complex reasoning, math, coding |

Using dynamic thinking (`-1`) instead of fixed high values can reduce costs by **30-50%** compared to always using maximum thinking budgets.

## Safety Settings

```python
from google.genai.types import HarmCategory, HarmBlockThreshold

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Your content here",
    config=types.GenerateContentConfig(
        safety_settings=[
            types.SafetySetting(
                category=HarmCategory.HARM_CATEGORY_HARASSMENT,
                threshold=HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE
            ),
            types.SafetySetting(
                category=HarmCategory.HARM_CATEGORY_HATE_SPEECH,
                threshold=HarmBlockThreshold.BLOCK_ONLY_HIGH
            )
        ]
    )
)
```

### Harm Categories
- `HARM_CATEGORY_HARASSMENT`
- `HARM_CATEGORY_HATE_SPEECH`
- `HARM_CATEGORY_SEXUALLY_EXPLICIT`
- `HARM_CATEGORY_DANGEROUS_CONTENT`

### Thresholds
- `BLOCK_NONE`
- `BLOCK_ONLY_HIGH`
- `BLOCK_MEDIUM_AND_ABOVE`
- `BLOCK_LOW_AND_ABOVE`

## Response Structure

```python
response = client.models.generate_content(...)

# Access text
print(response.text)

# Access full structure
candidate = response.candidates[0]
print(candidate.content.parts[0].text)
print(candidate.finish_reason)
print(candidate.safety_ratings)

# Usage metadata
print(response.usage_metadata.prompt_token_count)
print(response.usage_metadata.candidates_token_count)
print(response.usage_metadata.total_token_count)
```

## Error Handling

```python
from google.genai import errors

try:
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents="Hello"
    )
except errors.APIError as e:
    print(f"API error: {e}")
except errors.InvalidArgumentError as e:
    print(f"Invalid request: {e}")
except errors.ResourceExhaustedError as e:
    print(f"Rate limit exceeded: {e}")
```

## Token Counting

```python
# Count tokens before sending
token_count = client.models.count_tokens(
    model="gemini-2.5-flash",
    contents="Your content here"
)
print(f"Token count: {token_count.total_tokens}")
```

## Context Caching

### Explicit Caching (Guaranteed Savings)

```python
# Create a cache for repeated content
cache = client.caches.create(
    model="gemini-2.5-flash",
    contents=[
        types.Part(text="[Large document or context here...]")
    ],
    ttl="3600s"  # 1 hour
)

# Use cached content
response = client.models.generate_content(
    model="gemini-2.5-flash",
    cached_content=cache.name,
    contents="Question about the cached document"
)
```

### Implicit Caching (Automatic, Recommended)

Implicit caching is **enabled by default** for Gemini 2.5+ models. No code changes required—savings are automatic when request prefixes match.

**Discounts:**
| Model Series | Discount on Cached Tokens |
|--------------|---------------------------|
| Gemini 2.5 models | **90%** |
| Gemini 2.0 models | **75%** |

**Minimum Token Thresholds:**
| Model | Minimum Tokens for Cache Hit |
|-------|------------------------------|
| Gemini 2.5 Flash | 1,024 tokens |
| Gemini 2.5 Pro | 2,048 tokens |

**Best Practices for Maximum Cache Hits:**

```python
# GOOD: Static content first, variable content last
prompt = """
[SYSTEM INSTRUCTION - same across requests]
[REFERENCE DOCUMENTS - same across requests]
[FEW-SHOT EXAMPLES - same across requests]

User question: {variable_user_input}  ← Put at END
"""

# BAD: Variable content mixed throughout
prompt = """
User: {variable_input}  ← Breaks cache prefix
[SYSTEM INSTRUCTION]
[REFERENCE DOCUMENTS]
"""
```

**Verifying Cache Hits:**
```python
response = client.models.generate_content(...)

# Check usage metadata for cache hits
metadata = response.usage_metadata
if hasattr(metadata, 'cached_content_token_count'):
    cached = metadata.cached_content_token_count
    total = metadata.prompt_token_count
    print(f"Cache hit: {cached}/{total} tokens ({cached/total*100:.1f}%)")
```

**Cache Duration:** Implicit caches are cleared within **24 hours**. Frequent requests keep the cache available longer.

**Explicit vs Implicit:**
| Feature | Explicit Caching | Implicit Caching |
|---------|-----------------|------------------|
| Setup required | Yes (create cache) | No (automatic) |
| Savings guaranteed | Yes | Only on cache hits |
| Control over TTL | Yes | No (≤24 hours) |
| Best for | Predictable, high-volume | General use |

## Official Documentation
- API Reference: https://ai.google.dev/api
- Generate Content: https://ai.google.dev/api/generate-content
- Quickstart: https://ai.google.dev/gemini-api/docs/quickstart
