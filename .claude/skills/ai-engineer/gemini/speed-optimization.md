# Gemini Flash Speed Optimization Guide

A comprehensive guide to maximizing speed and minimizing latency with Gemini Flash models.

## Quick Reference: Speed Settings

```python
from google import genai
from google.genai import types

client = genai.Client()

# FASTEST: 2.5 Flash-Lite (no config needed)
response = client.models.generate_content(
    model="gemini-2.5-flash-lite",
    contents="Your prompt"
)

# FAST + QUALITY: 2.5 Flash with thinking disabled
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Your prompt",
    config=types.GenerateContentConfig(
        thinking_config=types.ThinkingConfig(thinking_budget=0)
    )
)

# BALANCED: Gemini 3 Flash with minimal thinking
response = client.models.generate_content(
    model="gemini-3-flash-preview",
    contents="Your prompt",
    config=types.GenerateContentConfig(
        thinking_config=types.ThinkingConfig(thinking_level="MINIMAL")
    )
)
```

## Model Speed Comparison

| Model | Throughput | TTFT | Best For |
|-------|-----------|------|----------|
| 2.5 Flash-Lite | ~300+ t/s | <300ms | Maximum speed, high volume |
| 2.5 Flash (no thinking) | ~280 t/s | <400ms | Speed + better quality |
| 3 Flash (minimal) | ~220 t/s | <500ms | Speed + reasoning when needed |
| 3 Flash (default) | ~218 t/s | <500ms | Quality + good speed |

*t/s = tokens per second, TTFT = Time To First Token*

## Optimization Strategies

### 1. Disable Thinking for Simple Tasks

The biggest speed gain comes from disabling thinking for tasks that don't need it.

```python
# Classification - no thinking needed
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Classify this text as positive/negative/neutral: 'Great product!'",
    config=types.GenerateContentConfig(
        thinking_config=types.ThinkingConfig(thinking_budget=0)
    )
)

# Simple extraction - no thinking needed
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Extract all email addresses from: ...",
    config=types.GenerateContentConfig(
        thinking_config=types.ThinkingConfig(thinking_budget=0)
    )
)
```

**Tasks that DON'T need thinking:**
- Classification
- Simple extraction
- Translation
- Summarization
- Format conversion
- Chat responses

**Tasks that BENEFIT from thinking:**
- Complex math/logic
- Multi-step reasoning
- Code generation
- Strategic planning

### 2. Leverage Implicit Caching

Structure prompts for automatic cache hits (90% discount on cached tokens):

```python
# Template with static prefix
SYSTEM_PROMPT = """You are a helpful assistant specializing in customer support.

Guidelines:
- Be concise and professional
- Always acknowledge the customer's concern
- Provide actionable solutions
"""

def generate_response(user_message: str):
    return client.models.generate_content(
        model="gemini-2.5-flash",
        contents=f"{SYSTEM_PROMPT}\n\nCustomer message: {user_message}",
        config=types.GenerateContentConfig(
            thinking_config=types.ThinkingConfig(thinking_budget=0)
        )
    )

# All calls with same SYSTEM_PROMPT prefix get 90% discount on those tokens!
```

**Cache optimization tips:**
- Keep static content (system prompts, examples) at the START
- Put variable content (user input) at the END
- Minimum 1,024 tokens for 2.5 Flash cache hits
- Cache persists up to 24 hours with activity

### 3. Use Streaming for Perceived Latency

Even if total time is the same, streaming feels faster:

```python
# Streaming - user sees tokens immediately
response = client.models.generate_content_stream(
    model="gemini-2.5-flash",
    contents="Explain quantum computing"
)

for chunk in response:
    print(chunk.text, end="", flush=True)
```

### 4. Batch Processing for Non-Real-Time

Use Batch API for 50% cost savings when latency isn't critical:

```python
# Create batch request
batch = client.batches.create(
    model="gemini-2.5-flash",
    requests=[
        {"contents": "Request 1"},
        {"contents": "Request 2"},
        # ... up to thousands of requests
    ]
)

# Results available within 24 hours
# 50% cost reduction vs real-time API
```

### 5. Async Patterns for High Throughput

```python
import asyncio
from google import genai

async def process_batch(prompts: list[str]):
    client = genai.Client()

    async def single_request(prompt):
        return await client.models.generate_content_async(
            model="gemini-2.5-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                thinking_config=types.ThinkingConfig(thinking_budget=0)
            )
        )

    # Process all prompts concurrently
    results = await asyncio.gather(*[single_request(p) for p in prompts])
    return results

# Run with: asyncio.run(process_batch(my_prompts))
```

### 6. Rate Limit Handling

Implement exponential back-off to avoid rate limit penalties:

```python
import time
from google.genai import errors

def generate_with_retry(prompt: str, max_retries: int = 5):
    for attempt in range(max_retries):
        try:
            return client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )
        except errors.ResourceExhaustedError:
            if attempt == max_retries - 1:
                raise
            wait_time = 2 ** attempt  # 1, 2, 4, 8, 16 seconds
            time.sleep(wait_time)
```

## Decision Tree: Choosing the Right Configuration

```
What's your priority?
│
├─ SPEED above all else
│  └─ Use: gemini-2.5-flash-lite
│     No config needed, fastest option
│
├─ SPEED + some quality
│  └─ Use: gemini-2.5-flash
│     Config: thinking_budget=0
│
├─ SPEED + reasoning when needed
│  └─ Use: gemini-3-flash-preview
│     Config: thinking_level="MINIMAL"
│
├─ BALANCED (recommended default)
│  └─ Use: gemini-2.5-flash
│     Config: thinking_budget=-1 (dynamic)
│
└─ QUALITY above speed
   └─ Use: gemini-3-flash-preview
      Config: thinking_level="HIGH" or default
```

## Latency Budget Examples

### Chat Application (<200ms target)
```python
# Use Flash-Lite for instant responses
response = client.models.generate_content(
    model="gemini-2.5-flash-lite",
    contents=user_message
)
```

### Customer Support Bot (<500ms target)
```python
# Use Flash with no thinking
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=f"{STATIC_PROMPT}\n{user_query}",
    config=types.GenerateContentConfig(
        thinking_config=types.ThinkingConfig(thinking_budget=0)
    )
)
```

### Code Assistant (<1s acceptable)
```python
# Use Gemini 3 Flash with minimal thinking
response = client.models.generate_content(
    model="gemini-3-flash-preview",
    contents=code_question,
    config=types.GenerateContentConfig(
        thinking_config=types.ThinkingConfig(thinking_level="MINIMAL")
    )
)
```

### Data Processing (latency flexible)
```python
# Use Batch API for 50% cost savings
# Results within 24 hours
```

## Real-Time Audio Optimization

For voice/audio applications with Gemini Live API:

```python
# Audio chunk best practices
AUDIO_CHUNK_MS = 20  # Send every 20-40ms, not 1 second
SAMPLE_RATE = 16000  # Resample to 16kHz before sending

# Use ContextWindowCompressionConfig for long sessions
# Audio accumulates at ~25 tokens/second
```

## Cost vs Speed Trade-offs

| Configuration | Relative Speed | Relative Cost | Use When |
|---------------|----------------|---------------|----------|
| 2.5 Flash-Lite | 100% (fastest) | $0.50/1M | Speed critical, simple tasks |
| 2.5 Flash (no think) | ~93% | $2.80/1M | Need better quality |
| 2.5 Flash (dynamic) | ~85% | ~$3.00/1M | General use |
| 3 Flash (minimal) | ~73% | $3.50/1M | Need occasional reasoning |
| 3 Flash (default) | ~72% | $3.50/1M | Quality matters |

*Costs include typical input/output mix. Actual costs vary by usage pattern.*

## Monitoring Performance

```python
import time

def timed_generation(prompt: str, model: str, config=None):
    start = time.perf_counter()

    response = client.models.generate_content(
        model=model,
        contents=prompt,
        config=config
    )

    elapsed = time.perf_counter() - start
    tokens = response.usage_metadata.candidates_token_count

    print(f"Time: {elapsed:.2f}s")
    print(f"Tokens: {tokens}")
    print(f"Throughput: {tokens/elapsed:.0f} t/s")

    # Check for cache hits
    if hasattr(response.usage_metadata, 'cached_content_token_count'):
        cached = response.usage_metadata.cached_content_token_count
        print(f"Cached tokens: {cached} (90% discount)")

    return response
```

## Summary: Top 5 Speed Optimizations

1. **Disable thinking** (`thinking_budget=0`) for simple tasks
2. **Use 2.5 Flash-Lite** for maximum throughput
3. **Structure prompts** for implicit caching (static prefix, variable suffix)
4. **Stream responses** for better perceived latency
5. **Use Batch API** for non-real-time workloads (50% savings)

## Official Documentation

- Thinking Mode: https://ai.google.dev/gemini-api/docs/thinking
- Context Caching: https://ai.google.dev/gemini-api/docs/caching
- Implicit Caching: https://developers.googleblog.com/en/gemini-2-5-models-now-support-implicit-caching/
- Batch API: https://ai.google.dev/gemini-api/docs/batch
- Live API Best Practices: https://docs.cloud.google.com/vertex-ai/generative-ai/docs/live-api/best-practices
