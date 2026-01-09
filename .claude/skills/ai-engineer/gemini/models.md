# Gemini Models Reference (January 2025)

## Current Model Lineup

### Gemini 3 Series (Latest - December 2025)

| Model | ID | Context | Input $/1M | Output $/1M | Best For |
|-------|-----|---------|------------|-------------|----------|
| Gemini 3 Pro | `gemini-3-pro-preview` | 1M in / 65K out | $2.00 | $12.00 | Complex agentic workflows |
| Gemini 3 Flash | `gemini-3-flash-preview` | 1M in / 65K out | $0.50 | $3.00 | Best balance of speed + quality |

**Gemini 3 Flash Key Features (Released Dec 17, 2025):**
- **78% on SWE-bench Verified** - Outperforms Gemini 3 Pro on coding!
- **81.2% on MMMU-Pro** - Best multimodal reasoning score
- Combines Gemini 3 Pro reasoning with Flash efficiency
- New `thinking_level` parameter: `minimal`, `low`, `medium`, `high`
- Media resolution control: `low`, `medium`, `high`, `ultra high`
- Streaming function calling with partial arguments
- Multimodal function responses (images + PDFs)
- Less than 1/4 the cost of Gemini 3 Pro

**Gemini 3 Pro Key Features:**
- Reasoning-first architecture
- Adaptive thinking
- Integrated grounding
- 37.5% on Humanity's Last Exam benchmark

**When to use Gemini 3 Flash:**
- Agentic coding tasks (best SWE-bench score)
- Complex reasoning at low cost
- Multimodal understanding
- Production workloads needing Gemini 3 quality

### Gemini 2.5 Series (Stable - Recommended)

| Model | ID | Context | Input $/1M | Output $/1M | Best For |
|-------|-----|---------|------------|-------------|----------|
| Gemini 2.5 Pro | `gemini-2.5-pro` | 1M in / 65K out | $1.25 | $10.00 | Complex reasoning, coding |
| Gemini 2.5 Flash | `gemini-2.5-flash` | 1M in / 65K out | $0.30 | $2.50 | Most tasks (best value) |
| Gemini 2.5 Flash-Lite | `gemini-2.5-flash-lite` | 1M in / 65K out | $0.10 | $0.40 | High-volume, budget |

**Thinking Mode Pricing (2.5 Flash):**
- Standard output: $2.50/1M
- With thinking enabled: $3.50/1M

### Gemini 2.0 Series (Previous Generation)

| Model | ID | Context | Input $/1M | Output $/1M | Notes |
|-------|-----|---------|------------|-------------|-------|
| Gemini 2.0 Flash | `gemini-2.0-flash` | 1M in / 8K out | $0.10 | $0.40 | Stable, proven |
| Gemini 2.0 Flash-Lite | `gemini-2.0-flash-lite` | 1M in / 8K out | $0.10 | $0.40 | Ultra-efficient |

### Specialized Models

| Model | ID | Purpose |
|-------|-----|---------|
| Image Generation | `gemini-3-pro-image-preview` | Generate images |
| Image Generation | `gemini-2.5-flash-image` | Fast image generation |
| TTS | `gemini-2.5-flash-preview-tts` | Text-to-speech |
| Native Audio | `gemini-2.5-flash-native-audio-preview-12-2025` | Audio processing |

### Retired Models (Return 404)

- All Gemini 1.0 models
- All Gemini 1.5 models
- Update to `gemini-2.5-flash-lite` or newer

## Model Versioning

### Stable Models (Recommended for Production)
```python
# No suffix - auto-updates to latest stable
"gemini-2.5-flash"
"gemini-2.5-pro"
"gemini-2.5-flash-lite"
```

### Preview Models (Experimental)
```python
# With suffix - specific preview version
"gemini-2.5-flash-preview-09-2025"
"gemini-2.5-pro-preview-05-06"
"gemini-3-pro-preview"
```

**Note:** Preview models may have breaking changes. Use stable models for production.

## Capabilities Matrix

| Capability | 3 Flash | 3 Pro | 2.5 Pro | 2.5 Flash | 2.5 Flash-Lite |
|------------|---------|-------|---------|-----------|----------------|
| Text generation | ✅ | ✅ | ✅ | ✅ | ✅ |
| Image input | ✅ | ✅ | ✅ | ✅ | ✅ |
| Video input | ✅ | ✅ | ✅ | ✅ | ✅ |
| Audio input | ✅ | ✅ | ✅ | ✅ | ✅ |
| PDF input | ✅ | ✅ | ✅ | ✅ | ✅ |
| Thinking mode | ✅ | ✅ | ✅ | ✅ | ✅ |
| Function calling | ✅ | ✅ | ✅ | ✅ | ✅ |
| Streaming fn calls | ✅ | ✅ | ❌ | ❌ | ❌ |
| Multimodal fn resp | ✅ | ✅ | ❌ | ❌ | ❌ |
| Structured output | ✅ | ✅ | ✅ | ✅ | ✅ |
| Code execution | ✅ | ✅ | ✅ | ✅ | ✅ |
| File search | ✅ | ✅ | ✅ | ✅ | ✅ |
| Search grounding | ✅ | ✅ | ✅ | ✅ | ✅ |
| Media resolution | ✅ | ✅ | ❌ | ❌ | ❌ |
| URL context | ✅ | ✅ | ✅ | ✅ | ✅ |
| Batch API | ✅ | ✅ | ✅ | ✅ | ✅ |
| Context caching | ✅ | ✅ | ✅ | ✅ | ✅ |
| Fine-tuning | ❌ | ❌ | ✅ | ✅ | ✅ |

## Model Selection Guide

### By Task Type

| Task | Recommended Model | Why |
|------|-------------------|-----|
| Simple Q&A | 2.5 Flash-Lite | Fast, cheap |
| General coding | 3 Flash | 78% SWE-bench, great value |
| Complex reasoning | 3 Flash or 2.5 Pro | Strong reasoning |
| Agentic workflows | 3 Flash | Best coding + low cost |
| High-volume processing | 2.5 Flash-Lite + Batch | 50% batch discount |
| Long documents | 2.5 Flash | 1M context, good price |
| Creative writing | 2.5 Flash | Good balance |
| Research/analysis | 3 Pro | Deep reasoning |
| Multimodal | 3 Flash | 81.2% MMMU-Pro score |

### By Budget

| Budget | Input Cost/1M | Model |
|--------|---------------|-------|
| Minimal | $0.05 | 2.5 Flash-Lite (batch) |
| Budget | $0.10 | 2.5 Flash-Lite |
| Balanced | $0.30 | 2.5 Flash |
| Best Value | $0.50 | 3 Flash (best quality/price) |
| Quality | $1.25 | 2.5 Pro |
| Premium | $2.00 | 3 Pro |

## Context Windows

All current models support **1M tokens input** (~750,000 words).

| Model | Input Tokens | Output Tokens |
|-------|--------------|---------------|
| Gemini 3 series | 1,048,576 | 65,536 |
| Gemini 2.5 series | 1,048,576 | 65,536 |
| Gemini 2.0 Flash | 1,048,576 | 8,192 |

**Note:** 2.5 Pro charges 2x for prompts >200K tokens.

## Rate Limits

Rate limits vary by model and tier. Typical free tier limits:

| Model | RPM | TPM | RPD |
|-------|-----|-----|-----|
| 2.5 Flash | 15 | 1M | 1,500 |
| 2.5 Pro | 2 | 32K | 50 |
| 2.5 Flash-Lite | 30 | 1M | 1,500 |

Paid tiers have significantly higher limits.

## Speed & Latency Benchmarks

### Throughput (Output Tokens/Second)

| Model | Throughput | TTFT | Notes |
|-------|-----------|------|-------|
| Gemini 2.5 Flash-Lite | ~300+ t/s | <300ms | Fastest option |
| Gemini 2.5 Flash | ~280 t/s | <400ms | Fast when thinking disabled |
| Gemini 3 Flash | **218 t/s** | <500ms | 22% slower due to reasoning |
| Gemini 2.5 Pro | ~150 t/s | <600ms | Quality over speed |
| GPT-5.1 high | ~125 t/s | - | For comparison |
| DeepSeek V3.2 | ~30 t/s | - | For comparison |

*Source: Artificial Analysis benchmarks (December 2025)*

**Key Insight:** Gemini 3 Flash is 22% slower than Gemini 2.5 Flash because it includes reasoning capabilities. For pure speed without reasoning, use 2.5 Flash with `thinking_budget=0`.

### Latency Characteristics

- **Sub-500ms TTFT** for complex queries (Gemini 3 Flash)
- **Sub-second latency** for short prompts across all Flash models
- **50-70% latency reduction** compared to previous generation models

### Token Usage Trade-off

Gemini 3 Flash uses **2x+ more tokens** than 2.5 Flash for equivalent tasks (~160M tokens on benchmark suite). This is the "reasoning tax" for enhanced capabilities.

**Implication:** For simple tasks, Gemini 2.5 Flash with disabled thinking may be both faster AND cheaper than Gemini 3 Flash.

## Model Selection for Speed

### Decision Tree by Latency Requirements

```
Need lowest latency?
├── Yes → Gemini 2.5 Flash-Lite (fastest)
│         OR Gemini 2.5 Flash with thinking_budget=0
│
├── Need reasoning + speed balance?
│   └── Gemini 3 Flash with thinking_level=MINIMAL
│
└── Quality matters more than speed?
    └── Gemini 3 Flash (default) or 2.5 Pro
```

### Speed vs Quality Comparison

| Use Case | Fastest Option | Best Quality | Recommendation |
|----------|---------------|--------------|----------------|
| Chat/high-volume | 2.5 Flash-Lite | 3 Flash | Flash-Lite for <100ms response |
| Classification | 2.5 Flash (no thinking) | 3 Flash | Flash-Lite unless accuracy critical |
| Translation | 2.5 Flash-Lite | 2.5 Flash | Flash-Lite (optimized for this) |
| Code generation | 2.5 Flash (no thinking) | 3 Flash | 3 Flash (78% SWE-bench worth it) |
| Complex reasoning | 3 Flash (minimal) | 3 Flash (high) | Tune thinking_level |
| Real-time audio | 2.5 Flash Native Audio | - | ~25 tokens/sec audio rate |

### Throughput Optimization Strategies

1. **Disable thinking** for simple tasks: `thinking_budget=0`
2. **Use Batch API** for non-real-time workloads (50% cost reduction)
3. **Leverage implicit caching** (automatic 90% savings on repeated prefixes)
4. **Stream responses** for perceived latency improvement
5. **Use async/batching patterns** with LangChain/LlamaIndex
6. **Implement exponential back-off** for rate limit handling

## Cost Optimization

### 1. Use Context Caching
Cache reads cost only 10% of base input price.
```python
# First request: full price
# Subsequent with same prefix: 90% savings on cached portion
```

### 2. Use Batch API
50% discount for async processing within 24 hours.

### 3. Use Implicit Caching
Enabled by default for 2.5 models - automatic 90% discount on repeated content.

### 4. Choose Right Model Size
Don't use Pro for tasks Flash can handle.

## Pricing Comparison with OpenAI

| Task | Gemini Cost | OpenAI Cost | Savings |
|------|-------------|-------------|---------|
| Simple (1M tokens) | $0.50 (2.5 Flash-Lite) | $0.75 (GPT-4o-mini) | 33% |
| Standard (1M tokens) | $2.80 (2.5 Flash) | $10.00 (GPT-4.1) | 72% |
| Complex (1M tokens) | $11.25 (2.5 Pro) | $10.00 (GPT-4.1) | -12% |

## Model IDs Quick Reference

```python
# Stable (auto-updating to latest stable)
GEMINI_PRO = "gemini-2.5-pro"
GEMINI_FLASH = "gemini-2.5-flash"
GEMINI_FLASH_LITE = "gemini-2.5-flash-lite"
GEMINI_2_FLASH = "gemini-2.0-flash"

# Preview (experimental)
GEMINI_3_PRO = "gemini-3-pro-preview"
GEMINI_3_FLASH = "gemini-3-flash-preview"

# Specialized
GEMINI_IMAGE = "gemini-2.5-flash-image"
GEMINI_TTS = "gemini-2.5-flash-preview-tts"
```

## Official Documentation
- Models: https://ai.google.dev/gemini-api/docs/models
- Pricing: https://ai.google.dev/gemini-api/docs/pricing
- Vertex AI Models: https://docs.cloud.google.com/vertex-ai/generative-ai/docs/models
