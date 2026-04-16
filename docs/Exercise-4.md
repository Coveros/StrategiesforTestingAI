# Exercise 4: Lab - Diagnosing RAG Failures with Root Cause Analysis

**Estimated Duration:** 45-60 minutes  
**Prerequisites:** Exercises 1-3 completed, Trace UI access in the chatbot  
**Deliverable:** Three case diagnoses and three production bug reports with team ownership

---

## Overview

You are the on-call QA/TestOps engineer. Product just escalated **three critical chatbot bugs** from production users. Your job is to triage each failure by using the Trace UI and determine whether the issue belongs to:

- **Data Engineering** (retriever/search quality)
- **Prompt Engineering** (generator/LLM behavior)
- **Shared ownership** (both layers contribute)

This lab is about **root cause analysis**, not guesswork. You will inspect retrieved documents, context quality, and generated responses to identify where the failure actually occurs.

---

## Scenario: Three Production Bugs

You must diagnose these three cases:

1. **Case A: Bad Librarian**  
The bot returns unrelated or weakly related sources for a query.

2. **Case B: The Liar**  
The bot retrieves relevant sources, but the response adds facts not grounded in those sources.

3. **Case C: Lazy Bot**  
The bot retrieves relevant context that contains the answer, but still responds incompletely (or says it does not know).

---

## Group Setup

- **Individual Work:** Each student reviews the three provided Trace cases or verifies one live query if instructed, then drafts case diagnoses.
- **Table Discussion:** Teams compare diagnoses, challenge ownership decisions, and align on the strongest remediation plan per case.

---

## Key Concepts

| Failure Type | What Failed | Typical Signal | Likely Owner |
|---|---|---|---|
| **Context Precision Failure** | Retriever | Top docs are weak/off-topic despite similar wording | Data Engineering |
| **Groundedness Failure** | Generator | Response includes claims not present in retrieved context | Prompt Engineering |
| **Context Recall Failure** | Retriever and/or Generator | Useful context exists, but answer is missed | Data or Prompt Engineering |

**Important:** Always diagnose retrieval first. If context is wrong, generation cannot be right.

---

## Part A: Trigger and Inspect the Bugs (10-15 minutes)

Use the instructor-provided Trace captures first. If your instructor asks for live verification, run these exact queries in the chatbot at [http://localhost:5000](http://localhost:5000):

If live trace generation is unavailable, use precomputed trace samples from:

- `artifacts/precomputed/trace_samples/exercise4_trace_cases_*.json`

These files include query, response, and trace metadata for the three lab cases.

1. `What are the key differences between black-box and white-box testing for GenAI?`
2. `According to the production best practices, what is the recommended batch size for processing GenAI evaluations?`
3. `Explain the concept of hallucination in the context of GenAI testing.`

For each query, capture Trace evidence:

- Retrieved Documents (file names + similarity)
- Context snippets or source previews
- Final generated response

Use screenshots or copy/paste text evidence. Focus on evidence quality, not on re-creating every trace from scratch.

---

## Part B: Diagnose Case A - Bad Librarian (10-12 minutes)

### Goal
Determine whether this is a **Context Precision Failure**.

### Diagnosis Template

- **Query:**
- **Expected primary source(s):**
- **Actual top retrieved source(s):**
- **Similarity pattern (high/medium/low):**
- **Are top sources actually relevant?** Yes/No
- **Root cause category:**
  - [ ] Query-retrieval mismatch
  - [ ] Poor ranking / noisy top-k
  - [ ] Chunking/index quality issue
- **Owning team:** Data Engineering / Shared
- **Justification (1-3 sentences with Trace evidence):**

### Decision Rule
If retrieved docs are weak or off-topic, this is primarily a retriever problem.

---

## Part C: Diagnose Case B - The Liar (10-12 minutes)

### Goal
Determine whether this is a **Groundedness Failure**.

### Diagnosis Template

- **Query:**
- **Were retrieved docs relevant?** Yes/No
- **Key claim in response to verify:**
- **Is claim directly supported by retrieved context?** Yes/No
- **Unsupported additions detected?** Yes/No
- **Root cause category:**
  - [ ] Hallucination from model prior knowledge
  - [ ] Prompt allows unsupported inference
  - [ ] Citation/grounding constraints missing
- **Owning team:** Prompt Engineering / Shared
- **Justification (1-3 sentences with Trace evidence):**

### Decision Rule
If retrieval is good but the response invents or extends facts, this is primarily a generator/prompt problem.

---

## Part D: Diagnose Case C - Lazy Bot (10-12 minutes)

### Goal
Determine whether this is a **Context Recall / Lost-in-the-Middle Failure**.

### Diagnosis Template

- **Query:**
- **Does retrieved context contain the answer?** Yes/No
- **Did final response use that answer?** Yes/No
- **Potential failure pattern:**
  - [ ] Answer buried in long context (position bias)
  - [ ] Too much noisy context
  - [ ] Retrieval incomplete for the full intent
  - [ ] Prompt did not prioritize evidence use
- **Owning team:** Data Engineering / Prompt Engineering / Shared
- **Justification (1-3 sentences with Trace evidence):**

### Decision Rule
If answer evidence exists but is not used, investigate both ranking/context design and prompt behavior.

---

## Part E: Write Production Bug Reports (5-8 minutes)

For each case (A, B, C), write one concise bug report:

### Bug Report Template

- **Bug Title:**
- **Severity:** High / Medium / Low
- **Expected Behavior:**
- **Actual Behavior:**
- **Root Cause Category:** Context Precision / Groundedness / Context Recall
- **Owning Team:** Data Engineering / Prompt Engineering / Shared
- **Recommended Action:**
- **Acceptance Criteria (how we verify fix):**

Focus on clear, actionable language that engineering can execute.

If time is short, use bullet-point bug reports instead of full prose paragraphs.

---

## Deliverable Checklist

- [ ] Three Trace outputs captured (screenshots or text copies)
- [ ] Case A diagnosis completed and root cause identified
- [ ] Case B diagnosis completed and root cause identified
- [ ] Case C diagnosis completed and root cause identified
- [ ] Each case assigned to the correct owning team
- [ ] Three production bug reports written with actionable recommendations

## Submission Format

Submit one file named `exercise4_submission.md` containing:

1. **Case A Report:** Context Precision failure diagnosis + bug report
2. **Case B Report:** Groundedness failure diagnosis + bug report
3. **Case C Report:** Context Recall failure diagnosis + bug report

---

## Key Takeaway

Root cause analysis in RAG is a pipeline discipline:

- If retrieval fails, generation cannot recover reliably.
- If retrieval succeeds but response drifts, grounding/prompt controls are weak.
- If evidence exists but is missed, context ranking and prompt strategy both need review.

Use Trace evidence to triage quickly and route work to the right team.

---

## Resources

- Chatbot: [http://localhost:5000](http://localhost:5000)
- Pipeline code: [app/rag_pipeline.py](../app/rag_pipeline.py)
- Knowledge base: [data/documents/](../data/documents/)
