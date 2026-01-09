---
name: ai-engineer
description: Comprehensive AI engineering reference for OpenAI, Google Gemini, and Claude APIs. Use when working with GPT-5.2, Gemini 3, Claude 4.5 models, function calling, batch processing, or prompting techniques. Includes latest 2026 API endpoints, pricing, and advanced prompting best practices (CoT, CoVe, ToT).
triggers:
  - openai api
  - gemini api
  - gpt-4
  - gpt-5
  - gpt-5.2
  - o3 model
  - o3-mini
  - reasoning model
  - function calling
  - batch api
  - chat completions
  - responses api
  - generateContent
  - which model should i use
  - llm pricing
  - token pricing
  - gemini 3
  - gemini 3 flash
  - claude api
  - claude 4.5
  - prompting
  - prompt engineering
  - chain of thought
  - chain of verification
  - tree of thoughts
  - reduce hallucinations
  - agentic prompting
  - how to prompt
---

# AI Engineering Reference: OpenAI & Gemini (January 2026)

This skill provides comprehensive, up-to-date reference documentation for OpenAI and Google Gemini APIs.

## Quick Model Selection Guide

### Choose OpenAI when:
- You need **GPT-5.2** for enterprise/professional workloads
- You need **GPT-5.2-Codex** for agentic coding and refactors
- You need **reasoning models** (o3, o3-mini, o3-pro) for complex problems
- You need **built-in web search** with citation sources
- You need **computer use** capabilities
- You want **90% cached input discount** (GPT-5.2)
- You need **audio I/O** (GPT-4o Audio)

### Choose Gemini when:
- **Best coding value** - Gemini 3 Flash: 78% SWE-bench at $3.50/1M!
- **Best multimodal** - Gemini 3 Flash: 81.2% MMMU-Pro score
- **Cost is critical** - Gemini 3 Flash is 4x cheaper than GPT-5.2
- You need **very long context** (1M tokens standard on all models)
- You need **video understanding** (only Gemini supports video)
- You're in the **Google Cloud ecosystem**
- You need **Google Search grounding** with real-time data

### Quick Model Picker (January 2026)

| Task | Best OpenAI | Best Gemini |
|------|-------------|-------------|
| Simple chat/Q&A | GPT-4.1 nano | Gemini 2.5 Flash-Lite |
| General coding | GPT-5.2-Codex | **Gemini 3 Flash (78% SWE!)** |
| Complex reasoning | o3 or GPT-5.2 Thinking | Gemini 3 Pro |
| Agentic workflows | GPT-5.2-Codex | Gemini 3 Flash |
| Enterprise/Professional | GPT-5.2 | Gemini 3 Pro |
| Budget batch processing | GPT-4.1 mini (batch) | Gemini 2.5 Flash-Lite (batch) |
| Multimodal (images/video) | GPT-5.2 (no video) | **Gemini 3 Flash (81% MMMU!)** |
| Long documents (>400K) | GPT-4.1 (1M ctx) | Gemini 3 Flash (1M ctx) |

## Documentation Structure

### OpenAI
- [Models Reference](./openai/models.md) - All models, pricing, capabilities
- [Chat Completions API](./openai/chat-completions.md) - Legacy but stable API
- [Responses API](./openai/responses-api.md) - Recommended for new projects
- [Function Calling](./openai/function-calling.md) - Tools and function definitions
- [Batch API](./openai/batch-api.md) - JSONL async processing, 50% discount
- [GPT-5.2 Prompting](./openai/prompting/gpt-5.2-guide.md) - **NEW** Best practices for GPT-5.2
- [GPT-4.1 Prompting](./openai/prompting/gpt-4.1-guide.md) - Best practices for GPT-4.1
- [Reasoning Models](./openai/prompting/reasoning-models.md) - o3/o4-mini prompting

### Gemini
- [Models Reference](./gemini/models.md) - All models, pricing, capabilities
- [Generate Content API](./gemini/generate-content.md) - Core API endpoint
- [Function Calling](./gemini/function-calling.md) - Tools and function declarations
- [Batch API](./gemini/batch-api.md) - JSONL async processing, 50% discount
- [Gemini 3 Prompting](./gemini/prompting/gemini-3-guide.md) - Latest prompting practices

### Prompting (NEW)
- [Prompting Guide](./prompting/README.md) - Overview and technique selection
- [GPT-5.2 Prompting](./prompting/gpt-5.2.md) - OpenAI's latest flagship
- [Gemini 3 Prompting](./prompting/gemini-3.md) - Google's latest models
- [Claude 4.5 Prompting](./prompting/claude-4.5.md) - Anthropic's Claude family
- [Reasoning Techniques](./prompting/techniques/reasoning.md) - CoT, ToT, Self-Consistency
- [Hallucination Reduction](./prompting/techniques/hallucination-reduction.md) - CoVe and verification
- [Agentic Prompting](./prompting/techniques/agentic.md) - Tool use, multi-step tasks

### Cross-Platform
- [Decision Tree](./decision-tree.md) - Detailed model selection flowchart

## Quick Start Examples

### OpenAI - Chat Completions (curl)
```bash
curl https://api.openai.com/v1/chat/completions \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-4.1",
    "messages": [
      {"role": "system", "content": "You are a helpful assistant."},
      {"role": "user", "content": "Hello!"}
    ]
  }'
```

### OpenAI - Responses API with Web Search (curl)
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

### Gemini - Python SDK
```python
from google import genai

client = genai.Client()  # Uses GEMINI_API_KEY env var
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Explain quantum computing"
)
print(response.text)
```

### Gemini - REST API (curl)
```bash
curl "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key=$GEMINI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"contents": [{"parts": [{"text": "Hello!"}]}]}'
```

## Current Pricing Summary (January 2026)

### OpenAI (per 1M tokens)
| Model | Input | Output | Notes |
|-------|-------|--------|-------|
| **GPT-5.2** | $1.75 | $14.00 | Enterprise, professional (90% cached discount) |
| **GPT-5.2-Codex** | $1.75 | $14.00 | Agentic coding |
| GPT-4.1 | $2.00 | $8.00 | Great 1M context |
| GPT-4.1 mini | $0.40 | $1.60 | Fast & cheap |
| o3 | $2.00 | $8.00 | Complex reasoning |
| o3-mini | $0.55 | $2.20 | Fast reasoning |
| GPT-4o-mini | $0.15 | $0.60 | Legacy budget |

### Gemini (per 1M tokens)
| Model | Input | Output | Notes |
|-------|-------|--------|-------|
| **Gemini 3 Flash** | $0.50 | $3.00 | **BEST VALUE** - 78% SWE-bench! |
| Gemini 3 Pro | $2.00 | $12.00 | Complex agentic |
| Gemini 2.5 Flash | $0.30 | $2.50 | Stable, proven |
| Gemini 2.5 Flash-Lite | $0.10 | $0.40 | Budget |
| Gemini 2.5 Pro | $1.25 | $10.00 | Complex tasks |

**Batch discounts:** Both APIs offer 50% off for batch processing.
**Caching:** GPT-5.2 has 90% cached input discount. Gemini has automatic implicit caching.

## Authentication Quick Reference

### OpenAI
```bash
export OPENAI_API_KEY="sk-..."
# Header: Authorization: Bearer $OPENAI_API_KEY
```

### Gemini
```bash
export GEMINI_API_KEY="..."
# URL param: ?key=$GEMINI_API_KEY
# Or SDK auto-detects from env
```

## Key Differences Summary

| Feature | OpenAI | Gemini |
|---------|--------|--------|
| Latest flagship | GPT-5.2 (Dec 2025) | Gemini 3 Flash (Dec 2025) |
| Message format | `messages: [{role, content}]` | `contents: [{parts: [{text}]}]` |
| System prompt | `role: "system"` | `systemInstruction: {parts}` |
| Reasoning control | `reasoning: {effort}` | `thinking_level` parameter |
| Max context | 400K (GPT-5.2) / 1M (GPT-4.1) | 1M (all models) |
| Function schema | Nested under `function:` | Direct in declaration |
| Batch file limit | 100 MB, 50K requests | 2 GB |
| Built-in tools | web_search, file_search, code_interpreter, computer_use | Google Search, code execution |
| Video support | ❌ | ✅ |
| Cached input discount | 90% (GPT-5.2) | 90% (implicit) |

## Version Info
- **Last Updated:** January 2026
- **GPT-5.2 Knowledge Cutoff:** August 31, 2025
- **Gemini Knowledge Cutoff:** January 2025
