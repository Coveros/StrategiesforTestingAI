# Exercise 3: Audit & Extend the Evaluation Framework

**Estimated Duration:** 45-55 minutes  
**Prerequisites:** Completion of Exercise 2 (golden records designed and verified)  
**Deliverable:** A new evaluation heuristic or threshold adjustment, tested against the GenAI Testing Chatbot  

---

## Overview

In Exercise 2, you designed and verified golden records - test cases with expected outputs. But how do we *automatically* grade the chatbot against those records at scale?

This exercise flips the question: **What makes a good evaluation metric?**

You will:
1. **Audit** the existing regression test framework to understand which metrics catch which failures.
2. **Identify gaps** where the current metrics miss real problems.
3. **Extend** the framework with a new evaluation rule tailored to the chatbot's behavior.

This moves you from testing the system (Exercises 1-2) to testing the *tests themselves* - a critical production skill.

---

## Key Concepts

### Why Audit the Auditors?

Evaluation metrics are not perfect. A scoring system can:
- **False Negative:** Miss a hallucination because the paraphrasing is fluent.
- **False Positive:** Flag a correct answer as wrong because it didn't match the exact phrasing.

Your job: Find these mistakes and propose a fix.

### Three Layers of Evaluation

1. **Deterministic (Cheap & Fast):** Regex checks, length limits, keyword presence/absence, valid JSON.
2. **Semantic (Medium Cost):** Embedding-based similarity, cosine distance thresholds.
3. **LLM-as-Judge (Expensive & Powerful):** Use a model to evaluate another model's output.

The regression testing framework layers all three. Your task is to strengthen one.

---

## Part A: Explore & Map (25 minutes)

### Step 1: Run the Regression Test Suite

Open a terminal and navigate to the repo root.

```bash
python -m regression_testing.regression_testing --quick
```

This runs a quick pass of the golden records from Exercise 2 against the chatbot.

**Expected output:**
- A summary table with columns: Test ID | Status | Metric | Score | Message
- Some tests will **PASS** (score ≥ threshold, typically 0.75).
- Some will **FAIL** (score < threshold or rule violation).
- Some will have **WARNINGS** (edge cases).

### Step 2: Review Low-Scoring Tests

Examine the failing or warning tests. For each one, note:

1. **What was the query?** (Look back at your Exercise 2 golden record.)
2. **What did the chatbot output?** (Examine the response.)
3. **Which metric failed?**
   - *Faithfulness:* Did the response stick to the knowledge base, or did it hallucinate?
   - *Relevance:* Did it answer the question asked, or go off-topic?
   - *Coherence:* Is the output malformed, repetitive, or dangerous?

**Use the worksheet below to organize your findings:**

| Test ID | Query | Metric Failed | Why? | Is This a Real Failure? (Y/N) | Notes |
|-|-|-|-|-|-|
| Ex: `hallucination_basic` | "What AI safety practices..." | Faithfulness | Semantic similarity 0.62 vs threshold 0.75 | ? | Output paraphrased but was accurate. False positive? |
| | | | | | |
| | | | | | |

### Step 3: Identify False Positives & Negatives

- **False Positive:** A test flagged as failing but the chatbot's answer was actually correct.
  - *Example:* Semantic similarity scored low because the output paraphrased the knowledge base in a different style.
- **False Negative:** A test passed but the answer was actually bad.
  - *Example:* A hallucination slipped through because the made-up claim was semantically similar to a real one.

**Key Question:** "If the model phrasing changed slightly but the meaning remained true, would the test still pass?"

### Step 4: Document Gaps

Based on your failures:

1. **Which evaluation layer is weakest?** (Deterministic, Semantic, or LLM-as-Judge)
2. **What type of failure does the framework not catch well?**
   - Off-topic refusals?
   - Subtle hallucinations (high semantic similarity to parts of the knowledge base but not valid inferences)?
   - Length or verbosity issues?
   - Missing citations where required?

---

## Part B: Propose & Implement a Fix (20-30 minutes)

Choose **one** of the following approaches to strengthen the evaluation framework:

### Option 1: Add a Deterministic Heuristic

**Goal:** Catch obvious failures with a simple rule.

**Examples:**
- **Refusal Detection:** Check if the response contains "I don't have information about" or "beyond my knowledge base" for out-of-domain queries. Flag it as PASS if present, FAIL if absent.
- **Length Guardrail:** Ensure responses are between 50 and 500 tokens. Flag excessively verbose or truncated outputs.
- **Citation Requirement:** Does the response include a reference to the knowledge base documents (e.g., "according to the GenAI Testing Guide...")? Flag if absent for certain query types.
- **Keyword Detector:** For queries about "safety" or "hallucinations," ensure the response mentions at least one of these keywords.

**Deliverable:** Pseudo-code or Python snippet that implements the heuristic.

```python
# Example: Check for refusal on out-of-scope queries
def check_refusal_on_oob(query: str, response: str) -> bool:
    """Returns True if response appropriately refuses out-of-scope query."""
    oob_terms = ["python", "recipe", "code golf"]  # Adjust per knowledge base
    
    is_oob = any(term in query.lower() for term in oob_terms)
    has_refusal = "don't have information" in response.lower()
    
    if is_oob:
        return has_refusal  # Should refuse if out-of-scope
    return True  # In-scope queries don't require refusal
```

### Option 2: Adjust a Semantic Threshold

**Goal:** Tune the embedding-based similarity score for fewer false positives or false negatives.

**Examples:**
- **Looser Threshold:** Change similarity threshold from 0.75 to 0.70 if too many correct answers are flagged as failures.
- **Response vs. Query Alignment:** Create a new metric that measures semantic alignment between the query intent and response content (separate from faithfulness).
- **Context Utilization:** Check that the response genuinely incorporates multiple documents from the knowledge base (not just one).

**Deliverable:** Justification for the threshold change and re-run test results.

```python
# Example: Calculate semantic alignment between query and response
from app.rag_pipeline import RAGPipeline

pipeline = RAGPipeline()
query = "What are best practices for evaluating GenAI?"
response = "Based on the knowledge base, here are key practices: ..."

# Embed both
query_embedding = pipeline.embedder.embed_query(query)
response_embedding = pipeline.embedder.embed_query(response)

# Cosine similarity (higher = more aligned)
similarity = cosine_similarity([query_embedding], [response_embedding])[0][0]
print(f"Query-Response Alignment: {similarity:.2f}")

# Propose new rule: Alignment must be > 0.80
if similarity > 0.80:
    print("PASS: Response is well-aligned to query intent")
else:
    print("FAIL: Response drifts from query intent")
```

### Option 3: Propose a Custom Citation Rule

**Goal:** Ensure responses cite or reference their sources.

**Examples:**
- **Explicit Citation:** For claims about hallucination or safety, the response must mention "GenAI Testing Guide" or "Production Best Practices."
- **Knowledge Base Traceability:** Flag responses that claim facts not explicitly in the knowledge base documents.
- **Disclosure Requirement:** Responses should include a footer like "Sources: GenAI Testing Guide, FAQ" summarizing which documents were used.

**Deliverable:** A new rule in the evaluation framework that validates citations.

```python
# Example: Check for explicit citation
def require_citation_for_safety_topics(query: str, response: str) -> bool:
    """Ensure safety-related responses cite the knowledge base."""
    safety_keywords = ["hallucination", "best practice", "safety", "evaluation"]
    
    is_safety_query = any(kw in query.lower() for kw in safety_keywords)
    has_citation = any(doc in response for doc in 
        ["GenAI Testing Guide", "Production Best Practices", "Evaluation"])
    
    if is_safety_query:
        return has_citation
    return True  # Non-safety queries don't require citations
```

---

## Part C: Test Your Fix (10-15 minutes)

Once you've proposed a heuristic, semantic adjustment, or citation rule:

1. **Implement it** (or write clear pseudo-code if implementing feels too ambitious).
2. **Re-run the regression suite** with your new rule enabled.
3. **Document the impact:**
   - How many previously failing tests now pass?
   - How many previously passing tests now fail? (These are new false positives-investigate!)
4. **Propose an adjustment** if needed.

---

## Deliverable Checklist

- [ ] Worksheet completed with all failing tests identified and categorized.
- [ ] At least one false positive and one false negative identified.
- [ ] One of the three approaches chosen (Deterministic, Semantic, or Citation).
- [ ] Pseudo-code or implementation written.
- [ ] Regression suite re-run with new rule.
- [ ] Impact analysis documented (how many tests changed status?).

## Submission Format (VM)
Submit one file named `exercise3_submission.md` (or PDF) containing:
1. Your completed worksheet.
2. The chosen approach and pseudo-code/implementation notes.
3. Before/after test impact summary.

---

## Reflection Questions

1. **Metric vs. Implementation Gap:** Did the metric work in theory but fail in practice? Why?
2. **Threshold Sensitivity:** How much does a small change in threshold dramatically shift pass/fail rates? What does that tell you about robustness?
3. **Production Implication:** If you deployed this metric, what would be the cost of false positives vs. false negatives? Which is worse for a safety-critical chatbot?
4. **Scaling Question:** As the golden dataset grows from 10 records to 1,000, does your rule scale? Will it catch subtle issues or only obvious ones?

---

## Resources

- **Code Reference:** [regression_testing/regression_testing.py](../regression_testing/regression_testing.py)
- **Evaluation Framework:** [tests/evaluation_framework.py](../tests/evaluation_framework.py)
- **Knowledge Base:** [data/documents/](../data/documents/)
- **Running Chatbot:** [http://localhost:5000](http://localhost:5000)

---

## Key Takeaway

Evaluation metrics are not oracles-they're tools you design and refine. **The best tests fail gracefully and tell you why.** By auditing your own metrics, you build the judgment needed for production AI systems where no perfect answer exists.
