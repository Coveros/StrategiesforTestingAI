# Exercise 4: Decompose a RAG Failure - Retriever vs. Generator Diagnosis

**Estimated Duration:** 50-60 minutes  
**Prerequisites:** Completion of Exercise 2 (at least 3 golden records with real outputs)  
**Deliverable:** Diagnosis report for 3-4 failing queries, with root cause (Retriever or Generator) and proposed fix  

---

## Overview

A chatbot's answer is only as good as the documents it retrieves. If the retriever pulls the wrong chunk, the generator - no matter how powerful - will hallucinate, summarize incorrectly, or refuse to answer.

This exercise teaches you to **decompose failures** along the RAG pipeline:

1. **Retriever Failure:** Wrong document retrieved, or right document ranked too low.
2. **Generator Failure:** Retrieved documents were good, but the LLM misused or ignored them.

By instrumenting the chatbot, you'll learn to fix problems at their source - not downstream.

---

## Key Concepts

### The Dependency Chain

```
User Query
    ↓
Query Embedding
    ↓
Similarity Search (Retriever) ← Failure here = wrong context
    ↓
Top K Documents -> Injected into prompt
    ↓
LLM Generation (Generator) ← Failure here = wrong use of context
    ↓
Answer
```

**Principle:** If retrieval fails, generation fails. Fix the retriever first.

### Three Root Causes

| Failure Mode | Symptom | Likely Cause |
|-|-|-|
| **Hallucination** | Answer includes info not in knowledge base | Retriever pulled weak/irrelevant docs; Generator filled gaps from training data |
| **Incomplete Answer** | "I don't know" despite having relevant docs | Retriever pulled right docs but ranked them too low (position bias); Or docs didn't make it to prompt context window |
| **Wrong Answer** | Answer is fluent but addresses a different question | Retriever prioritized semantic similarity over relevance; Generator used out-of-context docs |

---

## Part A: Inspect the Retriever (20 minutes)

### Step 1: Run Your Exercise 2 Queries

Open the GenAI Testing Chatbot at [http://localhost:5000](http://localhost:5000).

Pick **3-4 queries from your Exercise 2 golden records** that either:
- Failed in Exercise 3 regression testing, OR
- You suspect the chatbot struggled with, OR
- You know it hallucinated or gave an incomplete answer.

**For each query, submit it to the chatbot (via the web UI).**

### Step 2: Examine the "Sources" Metadata

After the chatbot responds, you'll see metadata (sources, timing, temperature). This is the **retriever's output**.

**Look at each source:**

```
Source 1: genai_testing_guide.md (Chunk 5)
  Similarity: 87%
  Preview: "The GenAI Testing Guide covers methodologies..."

Source 2: faq_genai_testing.md (Chunk 12)
  Similarity: 71%
  Preview: "Q: What is a hallucination?..."

Source 3: production_best_practices.md (Chunk 8)
  Similarity: 64%
  Preview: "Best practices for deploying..."
```

### Step 3: Grade the Retriever

For each query, fill out the worksheet below:

| Query | Expected Source | Actual Top Source | Actual Top Similarity | On Target? (Y/N) | Notes |
|-|-|-|-|-|-|
| `"What evaluation metrics matter?"` | `evaluation_metrics.md` | `genai_testing_guide.md` | 87% | N | Should have prioritized eval metrics doc |
| | | | | | |

**Grading Criteria:**
- **Y (On Target):** The top-ranked source is the correct knowledge base doc with ≥75% similarity.
- **N (Off Target):** Top source is wrong, OR similarity is too low (<70%), OR number of relevant docs is insufficient.

### Step 4: Root Cause Analysis

For each "N" grade, propose why the retriever failed:

```
Query: "What evaluation metrics matter?"
  Status: Off Target (wrong doc ranked first)
  Root Cause Hypothesis:
    [ ] Embedding mismatch - Query about "evaluation" found "safety"
    [ ] Chunk size issue - Key content split across chunks; top chunk lacks context
    [ ] Vocabulary gap - Query uses "metrics" but docs use "dimensions" or "measurements"
    [ ] Too many results retrieved - Not filtering by relevance threshold
```

---

## Part B: Inspect the Generator (15-20 minutes)

Now assume the **retriever did its job**. Did the generator use that context correctly?

### Step 1: Examine the Response Quality

For each query, re-read the chatbot's response. Ask:

1. **Did it stick to the retrieved context?**
   - Yes: Response directly paraphrases or quotes the sources.
   - No: Response includes facts not in the sources (hallucination).
   - Partial: Mix of grounded + speculative content.

2. **Did it answer the specific question?**
   - Yes: Response directly addresses the user's intent.
   - No: Response is tangentially relevant or off-topic.
   - Partial: Answers part of the question.

3. **Was the reasoning sound?**
   - Yes: Logical flow; cites evidence.
   - Partial: Some leaps in logic; missing connections.
   - No: Non-sequiturs; incoherent.

### Step 2: Root Cause Analysis

If the generator underperformed, choose the likely culprit:

```
Query: "What evaluation metrics matter?"
  Retrieved Sources: genai_testing_guide.md, evaluation_metrics.md (good!)
  Response Quality Assessment:
    ❌ Did NOT stick to context - included claims about "bias metrics" not in docs
    Likely Generator Failure Cause:
      [ ] Prompt not strict enough ("answer only from context" unclear)
      [ ] Context window cut off - docs were truncated before reaching the LLM
      [ ] Position bias - Relevant info was in the middle of context; LLM ignored it
      [ ] Hallucination from pre-training - Model filled gaps with training knowledge
```

---

## Part C: Propose a Fix (15-20 minutes)

For each of your 3-4 failing queries, you identified whether the problem was:
- **Retriever:** Wrong docs, low similarity, insufficient quantity
- **Generator:** Right docs but misused them

Now propose **one concrete fix** for each failure category.

### Option 1: Retriever Tuning

**Examples:**
- **Increase retrieval count:** From `top_k=5` to `top_k=10` to capture more context.
- **Lower similarity threshold:** From 0.75 to 0.65 to include useful documents even if not perfectly aligned.
- **Adjust chunk size:** From 2000 chars to 1000 chars to improve granularity (smaller, focused chunks).
- **Add keyword boosting:** Prioritize documents containing specific keywords (e.g., "evaluation," "metrics") in the query.
- **Hybrid search:** Combine semantic similarity with keyword matching (e.g., BM25) for better precision on technical terms.

**Deliverable:** Write a one-sentence fix proposal with expected impact.

```
Example:
  Failure: Query "What is faithfulness?" retrieved faq_genai_testing.md (71% sim) 
  before production_best_practices.md (63% sim), but FAQ had only a definition.
  
  Fix: Reduce chunk size from 2000 to 1000 characters. Smaller chunks will isolate 
  the key definitions and examples, improving similarity scores for targeted queries.
  
  Expected Impact: Increase relevant doc rank; reduce hallucination from LLM padding weak context.
```

### Option 2: Generator Constraint

**Examples:**
- **Stricter system prompt:** Add explicit penalty for external knowledge (e.g., "Do not use facts from your training data. Refuse if the context is insufficient.").
- **Citation requirement:** Force the model to cite source filenames (e.g., "(from genai_testing_guide.md)").
- **Length constraint:** If the generated answer exceeds a threshold, truncate and flag for human review.
- **Confidence threshold:** If the model's internal confidence is low, respond with "I don't have confident information" instead of guessing.

**Deliverable:** Write a new system prompt rule or constraint.

```
Example:
  Failure: Query "What evaluation metrics matter?" retrieved genai_testing_guide.md, 
  but response also mentioned "inter-rater reliability" which isn't in that doc.
  
  Fix: Add to system prompt: "You must cite the source document in parentheses for 
  every claim (e.g., 'Faithfulness is key (from Evaluation Metrics)').  If a claim 
  is not in the provided context, do not make it."
  
  Expected Impact: Force hallucinations to surface as unsupported claims; make bias more visible for human review.
```

### Option 3: Context Engineering

**Examples:**
- **Re-rank retrieved documents:** Use a secondary model (Cross-Encoder) to reorder Top K results by relevance.
- **Summarize long chunks:** Before injecting into prompt, distill each document to the top 200 characters to save tokens and improve signal-to-noise.
- **Metadata annotation:** Prepend each source with a label (e.g., "[Source: Evaluation Metrics] ...") to help the LLM identify and cite sources.
- **Context distillation:** Extract only the most relevant sentences from each document rather than entire chunks.

**Deliverable:** Describe the transformation applied to context before it reaches the generator.

```
Example:
  Failure: Response was tangentially relevant; did address "evaluation" but drifted 
  to "testing frameworks" which are different topics.
  
  Fix: Implement metadata enrichment. Before injecting context into prompt, prepend 
  each source with "[Context from: <FILENAME>] ". Additionally, add a separator 
  between sources: "---\n". This makes the LLM aware of source boundaries and less 
  likely to conflate ideas from different documents.
  
  Expected Impact: Reduce off-topic drift; improve citation accuracy.
```

---

## Part D: Document Your Findings (10 minutes)

Create a **Diagnosis Report** with the following structure:

### Report Template

**Query 1: "[Your Query Text Here]"**

| Item | Finding |
|-|-|
| **Ground Truth** | Expected documents: ___; Expected answer summary: ___ |
| **Retrieved Docs** | Source 1: _____ (Sim: __%); Source 2: _____ (Sim: __%); Source 3: _____ (Sim: _%) |
| **Actual Response** | [Copy response text] |
| **Retriever Diagnosis** | On Target / Off Target. Root cause: ________________ |
| **Generator Diagnosis** | Stuck to context / Hallucinated / Off-topic. Root cause: ________________ |
| **Primary Failure** | Retriever / Generator |
| **Proposed Fix** | **Category:** [Tuning / Constraint / Engineering]. **Description:** ________________ |
| **Expected Impact** | ________________ |

---

## Deliverable Checklist

- [ ] Worksheet completed for 3-4 queries with retriever grades (On Target / Off Target).
- [ ] Root cause analysis for each Off-Target grade.
- [ ] Generator quality assessment (Stuck to context / Hallucinated / Off-topic).
- [ ] At least one retriever fix proposal and one generator fix proposal drafted.
- [ ] Diagnosis Report completed with all 3-4 queries documented.

## Submission Format (VM)
Submit one file named `exercise4_submission.md` (or PDF) containing:
1. Retriever worksheet for 3-4 queries.
2. Generator analysis for the same queries.
3. Proposed fixes and final diagnosis report.

---

## Reflection Questions

1. **Dependency Insight:** Of your 3-4 failures, how many were retriever-only vs. generator-only vs. both? What does this suggest about where to invest effort?

2. **Threshold Sensitivity:** A small similarity threshold change (e.g., 0.75 -> 0.60) can dramatically shift which documents get retrieved. How would you tune this without overfitting to your 4 test cases?

3. **Position Bias:** If the most relevant document is ranked 4th instead of 1st, will the LLM use it? Why or why not? (Hint: Think about context window limits.)

4. **Generalization:** Your fixes are tailored to your 3-4 test queries. How would you avoid overfitting? (Hint: What if the fix works for "evaluation metrics" but breaks "hallucination detection"?)

5. **Production Implication:** In production, you can't manually diagnose every query. How would you automate this decomposition for thousands of daily queries?

---

## Resources

- **Running Chatbot:** [http://localhost:5000](http://localhost:5000)
- **RAG Pipeline Code:** [app/rag_pipeline.py](../app/rag_pipeline.py) - Inspect the `_retrieve_documents()` and `_generate_response()` methods
- **Retrieval Experiments:** [experiments/retrieval_experiments.py](../experiments/retrieval_experiments.py) - Reference for tuning retrieval parameters
- **Knowledge Base:** [data/documents/](../data/documents/) - The source of truth your retriever should find
- **Vector Database Stats:** Run `python -c "from app.rag_pipeline import RAGPipeline; p = RAGPipeline(); print(f'Total docs: {p.collection.count()}')"` to see database stats

---

## Key Takeaway

**The best RAG debugging skill is tracing the dependency chain:** If the retriever pulls garbage, the generator is fighting an uphill battle. Conversely, a perfect retriever with a weak generator wastes resources. Know which system is failing, fix it at source, and validate your fix with a before/after comparison.

In Exercise 5, you'll learn to automate this decomposition for production monitoring-so you catch failures as they happen, not after users complain.
