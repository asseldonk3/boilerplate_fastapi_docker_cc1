# Hallucination Reduction Techniques

Methods to reduce factual errors and hallucinations in LLM outputs.

## Chain of Verification (CoVe)

**Source:** [Meta Research, 2023](https://arxiv.org/abs/2309.11495)

Chain of Verification is a self-critique technique that reduces hallucinations by having the model verify its own claims through targeted questions.

### How It Works

CoVe uses a four-step process:

```
Step 1: Generate initial response (may contain errors)
    ↓
Step 2: Plan verification questions for key claims
    ↓
Step 3: Answer each verification question independently
    ↓
Step 4: Generate corrected final response
```

### Performance

- **+23% F1 score** on closed-book QA tasks (0.39 → 0.48)
- **Outperforms ChatGPT and PerplexityAI** on longform generation
- Works without any training or fine-tuning

### Implementation

#### Basic CoVe Prompt

```
Question: Name politicians who were born in New York.

Step 1 - Initial Answer:
[Generate your initial list]

Step 2 - Verification Questions:
For each person listed, ask: "Where was [person] born?"

Step 3 - Verify Each:
[Answer each verification question independently]

Step 4 - Corrected Answer:
Based on verifications, provide your final corrected list with only
confirmed New York-born politicians.
```

#### Structured Implementation

```python
def chain_of_verification(question):
    # Step 1: Initial response
    initial = llm(f"Answer this question: {question}")

    # Step 2: Generate verification questions
    verifications = llm(f"""
    Given this response: {initial}

    Generate 3-5 specific verification questions to fact-check
    the key claims in this response.
    """)

    # Step 3: Answer each verification question independently
    # IMPORTANT: Each answer should be independent to avoid bias
    verification_answers = []
    for q in parse_questions(verifications):
        answer = llm(f"Answer only this question: {q}")
        verification_answers.append(answer)

    # Step 4: Generate corrected response
    final = llm(f"""
    Original question: {question}
    Initial response: {initial}

    Verification results:
    {format_verifications(verification_answers)}

    Based on the verification results, provide a corrected final response.
    Remove or correct any claims that failed verification.
    """)

    return final
```

### CoVe Variants

| Variant | Description | Best For |
|---------|-------------|----------|
| **Joint** | All steps in one prompt | Simple queries |
| **2-Step** | Separate initial + verification | Moderate complexity |
| **Factored** | Each verification answered separately | Highest accuracy |
| **Factor+Revise** | Factored + explicit revision step | Complex factual queries |

**Recommendation:** Use Factored or 2-Step. Joint method can repeat hallucinations.

### Single-Prompt CoVe

For simpler implementation:

```
Answer this question: [Your question]

After your initial answer, verify your response by:
1. List 3 specific claims you made
2. For each claim, ask yourself a verification question
3. Answer each verification question
4. Correct any errors in your final response

Format:
INITIAL ANSWER: [your answer]

VERIFICATION:
- Claim 1: [claim] → Question: [q] → Verified: [yes/no + evidence]
- Claim 2: [claim] → Question: [q] → Verified: [yes/no + evidence]
- Claim 3: [claim] → Question: [q] → Verified: [yes/no + evidence]

FINAL CORRECTED ANSWER: [corrected response]
```

### Limitations

- **Reduces but doesn't eliminate hallucinations**
- Only catches factual errors the model can self-identify
- Doesn't help with incorrect reasoning
- Depends on model's self-verification capability

---

## Other Hallucination Reduction Techniques

### 1. Grounding with Context

Provide source material and require citations:

```
<context>
[Your reference documents]
</context>

Answer based ONLY on the provided context.
If the answer is not in the context, say "I don't have information about this."
For each claim, cite the relevant section: [claim] (Source: section X)
```

### 2. Confidence Calibration

Ask the model to rate its confidence:

```
Answer this question and rate your confidence 1-10 for each fact.

For facts rated below 7, either:
- Indicate uncertainty explicitly ("I believe..." / "This may be...")
- Mark as unverified
- Omit if not essential
```

### 3. Retrieval Augmented Generation (RAG)

Ground responses in retrieved documents:

```python
def rag_answer(question):
    # Retrieve relevant documents
    docs = vector_search(question)

    # Ground response in documents
    response = llm(f"""
    Based on these documents:
    {docs}

    Answer: {question}

    Only use information from the provided documents.
    Cite your sources.
    """)

    return response
```

### 4. High-Risk Self-Check

For critical domains (legal, financial, medical):

```xml
<high_risk_self_check>
Before finalizing your response:
1. Re-scan for unstated assumptions
2. Verify all numbers are grounded in provided context
3. Soften overly strong language ("always," "guaranteed," "never")
4. Add caveats where appropriate
5. Recommend professional consultation for decisions
</high_risk_self_check>
```

### 5. Multi-Model Verification

Use different models to cross-check:

```python
def multi_model_verify(question):
    answers = {
        "gpt": openai_call(question),
        "gemini": gemini_call(question),
        "claude": claude_call(question)
    }

    # Compare for consensus
    synthesis = llm(f"""
    Three models answered this question: {question}

    GPT: {answers['gpt']}
    Gemini: {answers['gemini']}
    Claude: {answers['claude']}

    Identify points of agreement and disagreement.
    Flag any claims where models disagree.
    Provide a synthesized answer with confidence levels.
    """)

    return synthesis
```

---

## Technique Selection Guide

| Scenario | Recommended Technique |
|----------|----------------------|
| Factual queries | CoVe (Factored) |
| Document-based Q&A | Grounding + RAG |
| High-stakes decisions | Multi-model + Self-check |
| Research tasks | CoVe + Confidence calibration |
| Simple Q&A | Grounding alone |

## Combining Techniques

For maximum accuracy:

```python
def robust_answer(question, context=None):
    # 1. Ground in context if available
    if context:
        prompt = f"Based on: {context}\n\nQuestion: {question}"
    else:
        prompt = question

    # 2. Get initial response with CoT
    initial = llm(prompt + "\nThink step by step.")

    # 3. Apply CoVe
    verified = chain_of_verification(initial)

    # 4. Confidence calibration
    final = llm(f"""
    Response: {verified}

    Rate confidence 1-10 for each major claim.
    Soften or remove claims with confidence < 7.
    """)

    return final
```

## Sources

- [Chain-of-Verification Paper](https://arxiv.org/abs/2309.11495)
- [Learn Prompting: CoVe](https://learnprompting.org/docs/advanced/self_criticism/chain_of_verification)
- [PromptHub: Reducing Hallucinations](https://www.prompthub.us/blog/three-prompt-engineering-methods-to-reduce-hallucinations)
- [KDnuggets: Reliable Generations](https://www.kdnuggets.com/unlocking-reliable-generations-through-chain-of-verification)
