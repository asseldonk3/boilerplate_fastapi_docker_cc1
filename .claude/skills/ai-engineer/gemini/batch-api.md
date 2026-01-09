# Gemini Batch API

The Gemini Batch API processes large volumes of requests asynchronously at 50% of the standard cost with a target 24-hour turnaround.

## Why Use Batch API?

- **50% cost savings** on all models
- **Higher throughput** with higher rate limits
- **Up to 2GB** file size (vs 100MB for OpenAI)
- **Automatic retries** and error handling
- **Implicit caching** for additional savings (90% on cached tokens)
- **Tool support** including Google Search

## Two Approaches

### 1. Inline Requests (< 20MB)
For smaller batches, include requests directly in the API call.

### 2. JSONL File (Large Batches)
For larger batches, upload a JSONL file to Google Cloud Storage.

## JSONL File Format

Each line is a JSON object with:
- `key`: Unique identifier (for matching results)
- `request`: The generateContent request payload

```jsonl
{"key": "req-001", "request": {"contents": [{"parts": [{"text": "What is 2+2?"}]}]}}
{"key": "req-002", "request": {"contents": [{"parts": [{"text": "What is 3+3?"}]}]}}
{"key": "req-003", "request": {"contents": [{"parts": [{"text": "What is 4+4?"}]}]}}
```

### With System Instructions

```jsonl
{"key": "req-001", "request": {"contents": [{"parts": [{"text": "Explain quantum computing"}]}], "systemInstruction": {"parts": [{"text": "You are a physics professor. Be concise."}]}}}
```

### With Generation Config

```jsonl
{"key": "req-001", "request": {"contents": [{"parts": [{"text": "Write a haiku"}]}], "generationConfig": {"temperature": 1.5, "maxOutputTokens": 100}}}
```

## Inline Requests Example (Python)

```python
from google import genai

client = genai.Client()

# Create batch with inline requests
batch = client.batches.create(
    model="gemini-2.5-flash",
    requests=[
        {
            "key": "req-001",
            "request": {"contents": "What is Python?"}
        },
        {
            "key": "req-002",
            "request": {"contents": "What is JavaScript?"}
        },
        {
            "key": "req-003",
            "request": {"contents": "What is Rust?"}
        }
    ]
)

print(f"Batch created: {batch.name}")
print(f"Status: {batch.state}")
```

## JSONL File Example (Python)

```python
from google import genai
import json

client = genai.Client()

# Step 1: Create JSONL file
requests = [
    {"key": f"req-{i}", "request": {"contents": [{"parts": [{"text": f"What is {i} * {i}?"}]}]}}
    for i in range(1, 1001)
]

with open("batch_requests.jsonl", "w") as f:
    for req in requests:
        f.write(json.dumps(req) + "\n")

# Step 2: Upload to Google Cloud Storage
# gsutil cp batch_requests.jsonl gs://your-bucket/batch_requests.jsonl

# Step 3: Create batch from GCS file
batch = client.batches.create(
    model="gemini-2.5-flash",
    src="gs://your-bucket/batch_requests.jsonl",
    dest="gs://your-bucket/results/"  # Output location
)

print(f"Batch: {batch.name}")
```

## Checking Batch Status

```python
# Get batch status
batch = client.batches.get(name=batch.name)

print(f"State: {batch.state}")
print(f"Total requests: {batch.total_request_count}")
print(f"Succeeded: {batch.succeeded_request_count}")
print(f"Failed: {batch.failed_request_count}")
```

### Batch States

| State | Description |
|-------|-------------|
| `STATE_PENDING_PROCESSING` | Queued, not started |
| `STATE_PROCESSING` | Currently processing |
| `STATE_SUCCEEDED` | Completed successfully |
| `STATE_PARTIALLY_SUCCEEDED` | Some requests failed |
| `STATE_FAILED` | Batch failed |
| `STATE_CANCELLED` | User cancelled |

## Polling for Completion

```python
import time

batch_name = batch.name

while True:
    batch = client.batches.get(name=batch_name)
    print(f"Status: {batch.state}")

    if batch.state in ["STATE_SUCCEEDED", "STATE_PARTIALLY_SUCCEEDED", "STATE_FAILED"]:
        break

    time.sleep(60)  # Check every minute

print(f"Completed! Succeeded: {batch.succeeded_request_count}, Failed: {batch.failed_request_count}")
```

## Retrieving Results

### For Inline Requests
```python
# Results are available directly
for result in batch.responses:
    print(f"Key: {result.key}")
    if result.response:
        print(f"Response: {result.response.text}")
    if result.error:
        print(f"Error: {result.error}")
```

### For GCS Output
```python
# Download from GCS
# gsutil cp gs://your-bucket/results/* ./results/

# Parse results
with open("results/output.jsonl", "r") as f:
    for line in f:
        result = json.loads(line)
        print(f"Key: {result['key']}")
        print(f"Response: {result['response']['candidates'][0]['content']['parts'][0]['text']}")
```

## Output Format

```jsonl
{"key": "req-001", "response": {"candidates": [{"content": {"parts": [{"text": "4"}], "role": "model"}, "finishReason": "STOP"}], "usageMetadata": {"promptTokenCount": 5, "candidatesTokenCount": 1, "totalTokenCount": 6}}}
{"key": "req-002", "response": {"candidates": [{"content": {"parts": [{"text": "6"}], "role": "model"}, "finishReason": "STOP"}], "usageMetadata": {"promptTokenCount": 5, "candidatesTokenCount": 1, "totalTokenCount": 6}}}
```

## Using Tools in Batch

### Google Search Grounding
```jsonl
{"key": "search-001", "request": {"contents": [{"parts": [{"text": "What is the latest news about AI?"}]}], "tools": [{"googleSearch": {}}]}}
```

### Function Calling
```jsonl
{"key": "func-001", "request": {"contents": [{"parts": [{"text": "What's the weather in Paris?"}]}], "tools": [{"functionDeclarations": [{"name": "get_weather", "description": "Get weather", "parameters": {"type": "object", "properties": {"location": {"type": "string"}}}}]}]}}
```

## Cancelling a Batch

```python
client.batches.cancel(name=batch.name)
```

## Listing Batches

```python
batches = client.batches.list()
for batch in batches:
    print(f"{batch.name}: {batch.state}")
```

## Cost Comparison

| Model | Standard Input | Standard Output | Batch Input | Batch Output |
|-------|----------------|-----------------|-------------|--------------|
| 2.5 Flash | $0.30 | $2.50 | $0.15 | $1.25 |
| 2.5 Flash-Lite | $0.10 | $0.40 | $0.05 | $0.20 |
| 2.5 Pro | $1.25 | $10.00 | $0.625 | $5.00 |

**With implicit caching (90% discount on cached tokens):**
- Standard cached input: $0.03/1M (Flash)
- Batch cached input: $0.015/1M (Flash)

## OpenAI SDK Compatibility

Gemini Batch API now supports OpenAI SDK format:

```python
from openai import OpenAI

# Configure for Gemini
client = OpenAI(
    api_key=os.environ["GEMINI_API_KEY"],
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

# Use OpenAI-style batch format
# (Same JSONL format as OpenAI Batch API)
```

## Limits

| Limit | Value |
|-------|-------|
| Max file size | 2 GB |
| Max requests (inline) | ~20 MB worth |
| Target completion | 24 hours |
| Max concurrent batches | Varies by tier |

## Best Practices

### 1. Use Meaningful Keys
```jsonl
{"key": "user-123-query-456", ...}
```

### 2. Batch Similar Requests
Group requests with similar prompts to maximize caching benefits.

### 3. Handle Partial Failures
```python
if batch.state == "STATE_PARTIALLY_SUCCEEDED":
    # Some requests failed, check individual results
    failed_keys = []
    for result in batch.responses:
        if result.error:
            failed_keys.append(result.key)

    # Retry failed requests
```

### 4. Monitor Progress
```python
def monitor_batch(batch_name, interval=60):
    while True:
        batch = client.batches.get(name=batch_name)
        progress = (batch.succeeded_request_count + batch.failed_request_count) / batch.total_request_count
        print(f"Progress: {progress:.1%} ({batch.succeeded_request_count} succeeded, {batch.failed_request_count} failed)")

        if batch.state not in ["STATE_PENDING_PROCESSING", "STATE_PROCESSING"]:
            break

        time.sleep(interval)
```

### 5. Leverage Implicit Caching
Requests with identical prefixes get automatic caching. Structure your requests to share common prefixes:

```jsonl
{"key": "q1", "request": {"contents": [{"parts": [{"text": "Given the following document: [LONG DOC]\n\nQuestion: What is the main topic?"}]}]}}
{"key": "q2", "request": {"contents": [{"parts": [{"text": "Given the following document: [LONG DOC]\n\nQuestion: Who is the author?"}]}]}}
```

## Error Handling

```python
# Check for errors in results
for result in batch.responses:
    if result.error:
        print(f"Error for {result.key}: {result.error.message}")
        # Common errors:
        # - INVALID_ARGUMENT: Bad request format
        # - RESOURCE_EXHAUSTED: Token limit exceeded
        # - INTERNAL: Temporary failure (retry)
```

## Official Documentation
- Batch API: https://ai.google.dev/gemini-api/docs/batch-api
- Google Blog: https://developers.googleblog.com/en/scale-your-ai-workloads-batch-mode-gemini-api/
