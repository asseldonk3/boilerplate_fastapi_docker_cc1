# OpenAI Models Reference (January 2025)

## Current Model Lineup

### Flagship Models

#### GPT-5.2 Series (Latest - December 2025)

| Model | ID | Context | Input $/1M | Output $/1M | Best For |
|-------|-----|---------|------------|-------------|----------|
| GPT-5.2 | `gpt-5.2` | 400K in / 128K out | $1.75 | $14.00 | Enterprise, professional work |
| GPT-5.2 Pro | `gpt-5.2-pro` | 400K in / 128K out | Higher | Higher | Top-quality end-to-end execution |
| GPT-5.2-Codex | `gpt-5.2-codex` | 400K in / 128K out | $1.75 | $14.00 | Agentic coding, refactors |

**GPT-5.2 Variants:**
- **Instant** - Fast responses, lower latency
- **Thinking** - Extended reasoning (uses output tokens for thinking)
- **Pro** - Maximum quality with `xhigh` reasoning effort

**Key Features:**
- Knowledge cutoff: August 31, 2025
- 90% discount on cached input tokens ($0.175/1M cached)
- Better at spreadsheets, presentations, code, images, long context
- Stronger instruction following and less verbosity than GPT-5.1
- GDPval: Beats or ties professionals on 70.9% of comparisons

**GPT-5.2-Codex Improvements:**
- Context compaction for long-horizon agentic work
- Better performance on large refactors and migrations
- Improved Windows environment support

**When to use GPT-5.2:**
- Professional knowledge work
- Complex multi-step projects
- Enterprise applications
- When you need state-of-the-art quality

#### GPT-4.1 Series (Cost-Effective)
| Model | ID | Context | Input $/1M | Output $/1M | Best For |
|-------|-----|---------|------------|-------------|----------|
| GPT-4.1 | `gpt-4.1` | 1M tokens | $2.00 | $8.00 | Coding, instruction following |
| GPT-4.1 mini | `gpt-4.1-mini` | 1M tokens | $0.40 | $1.60 | Cost-effective general use |
| GPT-4.1 nano | `gpt-4.1-nano` | 1M tokens | ~$0.10 | ~$0.40 | High-volume, simple tasks |

**Key improvements over GPT-4o:**
- Major gains in coding and instruction following
- 1M token context window (up from 128K)
- Better at following literal instructions
- State-of-the-art on SWE-bench (55% solve rate)

### Reasoning Models (o-series)

| Model | ID | Context | Input $/1M | Output $/1M | Best For |
|-------|-----|---------|------------|-------------|----------|
| o3 | `o3` | 200K in / 100K out | $2.00 | $8.00 | Complex reasoning, planning |
| o3-mini | `o3-mini` | 200K in / 100K out | $0.55 | $2.20 | Fast reasoning |
| o3-pro | `o3-pro` | 200K | Higher | Higher | Hardest problems, more compute |
| o1 | `o1` | 128K | - | - | Previous reasoning model |
| o1-pro | `o1-pro` | 128K | - | - | More compute than o1 |

**When to use reasoning models:**
- Complex multi-step problems
- Planning and strategy
- Decisions with ambiguous information
- Mathematical reasoning
- Code architecture decisions

### Legacy Models (Still Available)

| Model | ID | Context | Input $/1M | Output $/1M | Notes |
|-------|-----|---------|------------|-------------|-------|
| GPT-4o | `gpt-4o` | 128K | $2.50 | $10.00 | Use for audio I/O |
| GPT-4o mini | `gpt-4o-mini` | 128K | $0.15 | $0.60 | Budget option |
| GPT-4o Audio | `gpt-4o-audio-preview` | 128K | Varies | Varies | Audio in/out |

### Deprecated Models

| Model | Deprecation Date | Replacement |
|-------|------------------|-------------|
| GPT-4.5 Preview | July 14, 2025 | GPT-4.1 |
| GPT-4 Turbo | - | GPT-4.1 |

## Model Selection Guide

### For Coding Tasks
```
Simple code completion → GPT-4.1 nano
General coding → GPT-4.1
Complex refactoring → GPT-4.1
Architecture decisions → o3 or o3-mini
```

### For Reasoning Tasks
```
Quick analysis → o3-mini
Complex reasoning → o3
Hardest problems → o3-pro
```

### For Cost Optimization
```
Highest volume, simple → GPT-4.1 nano
High volume, moderate → GPT-4.1 mini
Quality-sensitive → GPT-4.1
Batch processing → Any model + Batch API (50% off)
```

## Model IDs for API Calls

### Stable (Recommended)
```python
# GPT-5.2 family (Latest)
"gpt-5.2"
"gpt-5.2-pro"
"gpt-5.2-codex"

# GPT-4.1 family
"gpt-4.1"
"gpt-4.1-mini"
"gpt-4.1-nano"

# Reasoning
"o3"
"o3-mini"

# Legacy
"gpt-4o"
"gpt-4o-mini"
```

### Pinned Versions (For Consistency)
```python
# Use pinned versions for reproducibility
"gpt-4o-2024-08-06"
"gpt-4o-2024-05-13"
```

**Note:** Different versions may behave differently with the same prompts. Use pinned versions and implement evals for production.

## Context Windows

| Model | Input Tokens | Output Tokens |
|-------|--------------|---------------|
| GPT-5.2 family | 400,000 | 128,000 |
| GPT-4.1 family | 1,000,000 | 32,768 |
| o3 | 200,000 | 100,000 |
| o3-mini | 200,000 | 100,000 |
| GPT-4o | 128,000 | 16,384 |

## Capabilities Matrix

| Capability | GPT-5.2 | GPT-4.1 | o3 | GPT-4o |
|------------|---------|---------|-----|--------|
| Text generation | ✅ | ✅ | ✅ | ✅ |
| Vision (images) | ✅ | ✅ | ✅ | ✅ |
| Function calling | ✅ | ✅ | ✅ | ✅ |
| JSON mode | ✅ | ✅ | ✅ | ✅ |
| Streaming | ✅ | ✅ | ✅ | ✅ |
| Audio input | ❌ | ❌ | ❌ | ✅ |
| Audio output | ❌ | ❌ | ❌ | ✅ |
| Extended thinking | ✅ | ❌ | ✅ | ❌ |
| Web search (Responses API) | ✅ | ✅ | ✅ | ✅ |
| File search (Responses API) | ✅ | ✅ | ✅ | ✅ |
| Code interpreter | ✅ | ✅ | ✅ | ✅ |
| Computer use | ✅ | ✅ | ✅ | ✅ |
| Cached input discount | 90% | ❌ | ❌ | ❌ |

## Rate Limits

Rate limits vary by tier and model. Check your dashboard at:
https://platform.openai.com/account/limits

Typical limits:
- **Tier 1:** 500 RPM, 30,000 TPM
- **Tier 2:** 5,000 RPM, 450,000 TPM
- **Tier 3+:** Higher limits

**Batch API has separate, higher limits.**

## Official Documentation
- Models: https://platform.openai.com/docs/models
- Pricing: https://openai.com/api/pricing/
- Rate Limits: https://platform.openai.com/docs/guides/rate-limits
