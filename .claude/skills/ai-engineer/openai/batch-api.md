# OpenAI Batch API

The Batch API allows asynchronous processing of large numbers of requests with a 50% cost discount and 24-hour completion window.

## Why Use Batch API?

- **50% cost savings** on all models
- **Higher rate limits** (separate from synchronous limits)
- **Up to 50,000 requests** per batch
- **Ideal for:** Data processing, evaluations, embeddings, bulk analysis

## Supported Endpoints

- `/v1/responses` (Responses API)
- `/v1/chat/completions` (Chat Completions)
- `/v1/embeddings` (Embeddings)
- `/v1/completions` (Legacy Completions)

## Workflow Overview

```
1. Create JSONL file with requests
2. Upload file to OpenAI
3. Create batch job
4. Poll for completion (or webhook)
5. Download results
```

## JSONL File Format

Each line is a JSON object with:
- `custom_id`: Your unique identifier (for matching results)
- `method`: HTTP method (`POST`)
- `url`: API endpoint
- `body`: Request body (same as synchronous API)

### Example: Chat Completions Batch

```jsonl
{"custom_id": "req-1", "method": "POST", "url": "/v1/chat/completions", "body": {"model": "gpt-4.1", "messages": [{"role": "user", "content": "What is 2+2?"}]}}
{"custom_id": "req-2", "method": "POST", "url": "/v1/chat/completions", "body": {"model": "gpt-4.1", "messages": [{"role": "user", "content": "What is 3+3?"}]}}
{"custom_id": "req-3", "method": "POST", "url": "/v1/chat/completions", "body": {"model": "gpt-4.1", "messages": [{"role": "user", "content": "What is 4+4?"}]}}
```

### Example: Responses API Batch

```jsonl
{"custom_id": "resp-1", "method": "POST", "url": "/v1/responses", "body": {"model": "gpt-4.1", "input": "Summarize AI news"}}
{"custom_id": "resp-2", "method": "POST", "url": "/v1/responses", "body": {"model": "gpt-4.1", "input": "Explain quantum computing"}}
```

### Example: Embeddings Batch

```jsonl
{"custom_id": "emb-1", "method": "POST", "url": "/v1/embeddings", "body": {"model": "text-embedding-3-small", "input": "Hello world"}}
{"custom_id": "emb-2", "method": "POST", "url": "/v1/embeddings", "body": {"model": "text-embedding-3-small", "input": "Goodbye world"}}
```

## Complete Python Example

```python
from openai import OpenAI
import json
import time

client = OpenAI()

# Step 1: Create JSONL file
requests = [
    {
        "custom_id": f"req-{i}",
        "method": "POST",
        "url": "/v1/chat/completions",
        "body": {
            "model": "gpt-4.1",
            "messages": [{"role": "user", "content": f"What is {i} + {i}?"}],
            "max_tokens": 100
        }
    }
    for i in range(1, 101)  # 100 requests
]

with open("batch_requests.jsonl", "w") as f:
    for req in requests:
        f.write(json.dumps(req) + "\n")

# Step 2: Upload file
batch_file = client.files.create(
    file=open("batch_requests.jsonl", "rb"),
    purpose="batch"
)
print(f"Uploaded file: {batch_file.id}")

# Step 3: Create batch job
batch_job = client.batches.create(
    input_file_id=batch_file.id,
    endpoint="/v1/chat/completions",
    completion_window="24h",
    metadata={"description": "Math problems batch"}
)
print(f"Created batch: {batch_job.id}")

# Step 4: Poll for completion
while True:
    batch_status = client.batches.retrieve(batch_job.id)
    print(f"Status: {batch_status.status}")

    if batch_status.status == "completed":
        break
    elif batch_status.status == "failed":
        print(f"Batch failed: {batch_status.errors}")
        break
    elif batch_status.status == "expired":
        print("Batch expired (exceeded 24h)")
        break

    time.sleep(60)  # Check every minute

# Step 5: Download results
if batch_status.status == "completed":
    # Get output file
    output_file = client.files.content(batch_status.output_file_id)

    # Parse results
    results = []
    for line in output_file.text.strip().split("\n"):
        result = json.loads(line)
        results.append(result)

    # Process results
    for result in results:
        custom_id = result["custom_id"]
        response = result["response"]

        if response["status_code"] == 200:
            content = response["body"]["choices"][0]["message"]["content"]
            print(f"{custom_id}: {content}")
        else:
            print(f"{custom_id}: Error - {response}")

    # Also check for errors
    if batch_status.error_file_id:
        error_file = client.files.content(batch_status.error_file_id)
        print(f"Errors:\n{error_file.text}")
```

## curl Example

### Upload File
```bash
curl https://api.openai.com/v1/files \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -F purpose="batch" \
  -F file="@batch_requests.jsonl"
```

### Create Batch
```bash
curl https://api.openai.com/v1/batches \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "input_file_id": "file-abc123",
    "endpoint": "/v1/chat/completions",
    "completion_window": "24h"
  }'
```

### Check Status
```bash
curl https://api.openai.com/v1/batches/batch_abc123 \
  -H "Authorization: Bearer $OPENAI_API_KEY"
```

### List Batches
```bash
curl https://api.openai.com/v1/batches \
  -H "Authorization: Bearer $OPENAI_API_KEY"
```

### Cancel Batch
```bash
curl https://api.openai.com/v1/batches/batch_abc123/cancel \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -X POST
```

## Output File Format

Results are in JSONL format (order may differ from input!):

```jsonl
{"id": "resp-123", "custom_id": "req-1", "response": {"status_code": 200, "body": {"id": "chatcmpl-...", "choices": [{"message": {"content": "4"}}]}}}
{"id": "resp-124", "custom_id": "req-2", "response": {"status_code": 200, "body": {"id": "chatcmpl-...", "choices": [{"message": {"content": "6"}}]}}}
```

**Important:** Results are NOT in the same order as input. Use `custom_id` to match.

## Batch Status Values

| Status | Description |
|--------|-------------|
| `validating` | File is being validated |
| `failed` | Validation failed |
| `in_progress` | Processing requests |
| `finalizing` | Writing output files |
| `completed` | All done, results ready |
| `expired` | Exceeded 24h window |
| `cancelling` | Cancel requested |
| `cancelled` | Cancelled |

## Limits

| Limit | Value |
|-------|-------|
| Max requests per batch | 50,000 |
| Max file size | 100 MB |
| Completion window | 24 hours |
| Max concurrent batches | Varies by tier |

## Error Handling

### Partial Failures
Batches can partially complete. Check both output and error files:

```python
if batch_status.output_file_id:
    # Successfully processed requests
    output = client.files.content(batch_status.output_file_id)

if batch_status.error_file_id:
    # Failed requests
    errors = client.files.content(batch_status.error_file_id)
```

### Common Errors

| Error | Cause | Solution |
|-------|-------|----------|
| Invalid JSONL | Malformed JSON | Validate each line |
| Missing custom_id | Required field | Add unique IDs |
| Rate limit in body | Token limits | Reduce max_tokens |
| File too large | >100 MB | Split into multiple batches |

## Best Practices

### 1. Use Meaningful custom_ids
```python
# Good - traceable
{"custom_id": "user-123-query-456", ...}

# Bad - not useful
{"custom_id": "1", ...}
```

### 2. Include Metadata
```python
batch_job = client.batches.create(
    input_file_id=file_id,
    endpoint="/v1/chat/completions",
    completion_window="24h",
    metadata={
        "description": "Weekly report generation",
        "run_date": "2025-01-15",
        "version": "1.0"
    }
)
```

### 3. Implement Retry Logic
```python
def process_with_retry(requests, max_retries=3):
    failed_requests = requests

    for attempt in range(max_retries):
        # Create and run batch
        results, errors = run_batch(failed_requests)

        if not errors:
            return results

        # Retry only failed requests
        failed_ids = {e["custom_id"] for e in errors}
        failed_requests = [r for r in failed_requests
                         if r["custom_id"] in failed_ids]

    return results, failed_requests
```

### 4. Monitor Progress
```python
# Request counts are available during processing
status = client.batches.retrieve(batch_id)
print(f"Completed: {status.request_counts.completed}")
print(f"Failed: {status.request_counts.failed}")
print(f"Total: {status.request_counts.total}")
```

## Cost Comparison

| Model | Sync Input | Sync Output | Batch Input | Batch Output |
|-------|-----------|-------------|-------------|--------------|
| GPT-4.1 | $2.00 | $8.00 | $1.00 | $4.00 |
| GPT-4.1 mini | $0.40 | $1.60 | $0.20 | $0.80 |
| o3 | $2.00 | $8.00 | $1.00 | $4.00 |

## Official Documentation
- Batch API Guide: https://platform.openai.com/docs/guides/batch
- API Reference: https://platform.openai.com/docs/api-reference/batch
