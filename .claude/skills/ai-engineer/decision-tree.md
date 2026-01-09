# Model Selection Decision Tree

Use this guide to choose the right model for your task.

## Quick Decision Flowchart (Updated January 2026)

```
START
  │
  ├─ Is cost the PRIMARY concern?
  │   └─ YES → Is it simple/high-volume?
  │              ├─ YES → Gemini 2.5 Flash-Lite ($0.10/$0.40)
  │              └─ NO  → Gemini 3 Flash ($0.50/$3.00) - best value!
  │
  ├─ Do you need ENTERPRISE-GRADE quality?
  │   └─ YES → GPT-5.2 ($1.75/$14.00) - state-of-the-art
  │            or GPT-5.2-Codex for coding
  │
  ├─ Do you need REASONING (multi-step thinking)?
  │   └─ YES → How complex?
  │              ├─ Simple reasoning → o3-mini ($0.55/$2.20)
  │              ├─ Complex reasoning → o3 ($2.00/$8.00)
  │              ├─ With thinking → GPT-5.2 Thinking
  │              └─ Hardest problems → o3-pro or GPT-5.2 Pro (xhigh)
  │
  ├─ Do you need WEB SEARCH?
  │   └─ YES → Which ecosystem?
  │              ├─ OpenAI → GPT-5.2 + Responses API + web_search
  │              └─ Google → Gemini 3 Flash + Google Search grounding
  │
  ├─ Do you need VERY LONG CONTEXT (>400K tokens)?
  │   └─ YES → Gemini has 1M, GPT-5.2 has 400K:
  │              ├─ Budget → Gemini 2.5 Flash ($0.30)
  │              ├─ Quality → Gemini 3 Flash ($0.50)
  │              └─ Max quality → GPT-4.1 (1M ctx, $2.00)
  │
  ├─ Is it primarily CODING?
  │   └─ YES → Simple or complex?
  │              ├─ Budget → Gemini 3 Flash (78% SWE-bench!)
  │              ├─ Agentic → GPT-5.2-Codex (best for refactors)
  │              ├─ Enterprise → GPT-5.2
  │              └─ Architecture → o3 (reasoning helps)
  │
  ├─ Do you need MULTIMODAL (images/video/audio)?
  │   └─ YES → Gemini 3 Flash (81.2% MMMU-Pro, best score)
  │            OR GPT-5.2 (images only, no video)
  │
  ├─ Do you need BATCH PROCESSING?
  │   └─ YES → Both offer 50% discount
  │              ├─ Gemini: Up to 2GB files, implicit caching
  │              └─ OpenAI: Up to 100MB files, 50K requests
  │
  └─ GENERAL TASKS
       └─ Balance quality vs cost:
            ├─ Budget → Gemini 2.5 Flash-Lite
            ├─ Best Value → Gemini 3 Flash
            ├─ Balanced → GPT-4.1 mini
            └─ Premium → GPT-5.2
```

## Detailed Comparison by Use Case

### Simple Q&A / Chatbots

| Model | Cost/1M (in+out) | Speed | Quality | Recommendation |
|-------|------------------|-------|---------|----------------|
| Gemini 2.5 Flash-Lite | $0.50 | ⚡⚡⚡ | ★★★ | Best value |
| GPT-4o-mini | $0.75 | ⚡⚡⚡ | ★★★ | Good alternative |
| Gemini 2.5 Flash | $2.80 | ⚡⚡⚡ | ★★★★ | Better quality |

**Winner:** Gemini 2.5 Flash-Lite for cost, GPT-4o-mini if you need OpenAI

### Coding Tasks

| Model | Cost/1M | Speed | Code Quality | Recommendation |
|-------|---------|-------|--------------|----------------|
| GPT-5.2-Codex | $15.75 | ⚡⚡ | ★★★★★ | Best for agentic coding |
| GPT-5.2 | $15.75 | ⚡⚡ | ★★★★★ | Enterprise grade |
| Gemini 3 Flash | $3.50 | ⚡⚡⚡ | ★★★★★ | 78% SWE-bench! Best value |
| GPT-4.1 | $10.00 | ⚡⚡ | ★★★★★ | Great 1M context |
| GPT-4.1 mini | $2.00 | ⚡⚡⚡ | ★★★★ | Fast + good |

**Winner:** Gemini 3 Flash for value (78% SWE-bench at $3.50), GPT-5.2-Codex for agentic

### Complex Reasoning

| Model | Cost/1M | Thinking | Quality | Recommendation |
|-------|---------|----------|---------|----------------|
| o3 | $10.00 | ★★★★★ | ★★★★★ | Best reasoning |
| o3-mini | $2.75 | ★★★★ | ★★★★ | Fast reasoning |
| Gemini 2.5 Pro | $11.25 | ★★★★ | ★★★★ | Good alternative |

**Winner:** o3 for reasoning tasks, o3-mini for faster turnaround

### Long Document Analysis

| Model | Context | Cost for 500K input | Recommendation |
|-------|---------|---------------------|----------------|
| Gemini 2.5 Flash | 1M | $0.15 | Best value |
| GPT-4.1 | 1M | $1.00 | Better instruction following |
| Gemini 2.5 Pro | 1M | $1.25* | Complex analysis |

*2x pricing for >200K tokens

**Winner:** Gemini 2.5 Flash for cost, GPT-4.1 for precision

### Multimodal (Images, Video, Audio)

| Model | Images | Video | Audio | Cost | Recommendation |
|-------|--------|-------|-------|------|----------------|
| Gemini 2.5 Flash | ✅ | ✅ | ✅ | Low | Best overall |
| Gemini 2.5 Pro | ✅ | ✅ | ✅ | Medium | Complex tasks |
| GPT-4.1 | ✅ | ❌ | ❌ | Medium | Images only |
| GPT-4o | ✅ | ❌ | ✅ | Medium | Audio support |

**Winner:** Gemini 2.5 Flash (only option with video)

### Agentic Workflows

| Model | Tools | Persistence | Cost | Recommendation |
|-------|-------|-------------|------|----------------|
| GPT-4.1 + Responses API | ★★★★★ | ★★★★ | $10 | Best tooling |
| Gemini 3 Pro | ★★★★ | ★★★★ | $14 | Designed for agents |
| o3 | ★★★★ | ★★★★★ | $10 | Complex decisions |

**Winner:** GPT-4.1 + Responses API for tools, o3 for complex reasoning

### Batch Processing

| Platform | Max File | Discount | Caching | Recommendation |
|----------|----------|----------|---------|----------------|
| OpenAI | 100 MB | 50% | Manual | Standard choice |
| Gemini | 2 GB | 50% | Implicit (90%) | Best for large batches |

**Winner:** Gemini for large batches (caching + larger files)

## Cost Optimization Strategies

### 1. Use the Right Size
```
Task complexity → Model
Simple          → Flash-Lite / GPT-4o-mini ($0.10-$0.75/1M)
Standard        → Flash / GPT-4.1 mini ($2-3/1M)
Complex         → Pro / GPT-4.1 ($10-12/1M)
Reasoning       → o3 ($10/1M)
```

### 2. Batch When Possible
```
50% savings on both platforms
24-hour turnaround usually much faster
```

### 3. Use Caching
```
OpenAI: Manual context caching
Gemini: Automatic implicit caching (90% savings)
```

### 4. Cascade Models
```python
# Start cheap, escalate if needed
def smart_query(prompt):
    # Try cheap model first
    response = gemini_flash_lite(prompt)

    # If low confidence, use better model
    if needs_escalation(response):
        response = gemini_pro(prompt)

    return response
```

## API Feature Comparison

| Feature | OpenAI | Gemini |
|---------|--------|--------|
| **Streaming** | ✅ | ✅ |
| **Function calling** | ✅ | ✅ |
| **JSON mode** | ✅ | ✅ |
| **Vision** | ✅ | ✅ |
| **Video** | ❌ | ✅ |
| **Audio** | GPT-4o only | ✅ |
| **Web search** | Responses API | Google Search |
| **Code execution** | ✅ | ✅ |
| **File search** | ✅ | ✅ |
| **Computer use** | ✅ | ❌ |
| **Batch API** | ✅ (100MB) | ✅ (2GB) |
| **Context caching** | Manual | Automatic |

## When to Use Each Platform

### Choose OpenAI When:
- You need **GPT-5.2** for enterprise/professional workloads
- You need **reasoning models** (o3/o3-mini)
- You need **computer use** capabilities
- You're building with the **Responses API** features
- You need **audio input/output** (GPT-4o)
- You want **GPT-5.2-Codex** for agentic coding
- You want **90% cached input discount** (GPT-5.2)

### Choose Gemini When:
- **Cost is critical** - Gemini 3 Flash is 4x cheaper than GPT-5.2
- You need **best coding value** (Gemini 3 Flash: 78% SWE-bench at $3.50)
- You need **video understanding**
- You need **large batch processing** (2GB files)
- You want **automatic caching** (90% savings)
- You're in the **Google Cloud ecosystem**
- You need **Google Search grounding**
- You want **best multimodal** (Gemini 3 Flash: 81.2% MMMU-Pro)

### Use Both When:
- Different tasks need different strengths
- Redundancy/failover is required
- A/B testing model performance
- Cost optimization through routing

## Quick Reference Card (January 2026)

```
FAST + CHEAP:
  Gemini 2.5 Flash-Lite  $0.50/1M   Simple tasks
  GPT-4o-mini            $0.75/1M   OpenAI ecosystem

BEST VALUE:
  Gemini 3 Flash         $3.50/1M   78% SWE-bench, 81% MMMU-Pro!
  Gemini 2.5 Flash       $2.80/1M   Stable, proven

BALANCED:
  GPT-4.1 mini           $2.00/1M   Fast + capable
  GPT-4.1                $10/1M     1M context, great coding

PREMIUM:
  GPT-5.2                $15.75/1M  Enterprise, professional
  GPT-5.2-Codex          $15.75/1M  Agentic coding, refactors
  Gemini 3 Pro           $14/1M     Complex reasoning

REASONING:
  o3-mini                $2.75/1M   Fast reasoning
  o3                     $10/1M     Complex reasoning

BATCH (50% OFF):
  Gemini 2.5 Flash-Lite  $0.25/1M   High volume
  GPT-4.1 mini           $1.00/1M   OpenAI batch
```

## Model ID Quick Reference

```python
# OpenAI (Latest)
OPENAI_PREMIUM = "gpt-5.2"
OPENAI_PREMIUM_CODEX = "gpt-5.2-codex"
OPENAI_FAST = "gpt-4o-mini"
OPENAI_BALANCED = "gpt-4.1-mini"
OPENAI_QUALITY = "gpt-4.1"
OPENAI_REASONING = "o3"
OPENAI_FAST_REASONING = "o3-mini"

# Gemini (Latest)
GEMINI_BEST_VALUE = "gemini-3-flash-preview"  # 78% SWE-bench!
GEMINI_PREMIUM = "gemini-3-pro-preview"
GEMINI_FAST = "gemini-2.5-flash-lite"
GEMINI_BALANCED = "gemini-2.5-flash"
GEMINI_QUALITY = "gemini-2.5-pro"
```
