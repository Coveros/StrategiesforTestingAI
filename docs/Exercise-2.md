# Exercise 2: Building and Critiquing a Golden Test Set

Audience: Students
Estimated Duration: 45-55 minutes (Part A: 25 minutes, Part B: 20-30 minutes)
Type: Paper design exercise + code review
Prerequisites: Exercise 1 completed; chatbot running at http://localhost:5000
Deliverable: 10 golden records + critique of existing records + 1 gap record

## Why this exercise
Automated regression testing is only as trustworthy as the golden records it runs against. This exercise builds the skill of designing good golden records from scratch, then sharpens it by critiquing a real example.

## What you receive before starting
1. The four-element anatomy of a golden record (from the lecture):
   - Input: the exact user query
   - Context: any retrieved documents, history, or state the model needs
   - Expectation: exact match or semantic match criteria plus pass thresholds
   - Metadata: tags for priority, category, filtering
2. The running GenAI Testing Chatbot at http://localhost:5000.
3. The chatbot's knowledge base (four source documents in data/documents/):
   - genai_testing_guide.md
   - faq_genai_testing.md
   - production_best_practices.md
   - evaluation_metrics.md
4. Access to regression_testing/regression_testing.py in the course repo (for Part B).

---

## Part A: Design 10 Golden Records (25 minutes)

### Scenario
You are a QA engineer responsible for the GenAI Testing Chatbot you explored in Exercise 1. A new version of the Cohere backend model is being evaluated and you need a golden test set to decide whether the swap is safe to ship.

The chatbot's knowledge base covers four topics: GenAI testing strategies, FAQs about testing challenges, production best practices, and evaluation metrics. Your golden records must be answerable from those documents - if the chatbot cannot know the answer from its knowledge base, neither can your gold standard.

### Task
Design exactly 10 golden records using the distribution below.

| Category | Count | Purpose |
|---|---|---|
| Factual | 3 | Direct lookup questions the knowledge base can answer definitively |
| Reasoning | 3 | Multi-step or comparative questions requiring synthesis across topics |
| Adversarial | 2 | Prompt injection, jailbreak attempts, or out-of-domain abuse |
| Noise | 2 | Typos, gibberish, empty input, or completely off-topic queries |

### Required fields for each record
1. id: short unique string
2. category: one of factual / reasoning / adversarial / noise
3. query: exact input string the test runner will send
4. gold_standard: the ideal answer text (or expected error message)
5. keywords: 3 to 6 words or phrases that MUST appear in an acceptable response
6. expected_length_range: (min_chars, max_chars)
7. pass_criteria: one or two sentences describing what makes a response pass
8. priority: high / medium / low

### Starter template
```
id: hallucination_definition
category: factual
query: What is hallucination in the context of generative AI?
gold_standard: Hallucination in generative AI refers to when a model produces output that sounds plausible but is factually incorrect, fabricated, or unsupported by the provided context or training data. It is a core risk in RAG systems when retrieved context is insufficient or ignored.
keywords: [hallucination, factually incorrect, plausible, context, generative AI]
expected_length_range: (120, 350)
pass_criteria: Response must define hallucination, explain why it occurs in generative models, and mention context or retrieval as a contributing factor. A response that only says "making things up" without explanation fails.
priority: high
```

### Tip: verify against the knowledge base first
Before finalising a gold standard, ask the chatbot the question and compare the response to the source documents. If the chatbot consistently cannot answer it correctly, that is a system limitation - not a useful golden record.

### Things to think about while designing
1. Is your gold standard actually answerable from the four knowledge base documents?
2. Are your keywords specific enough to rule out a hallucinated but fluent response?
3. Does your length range exclude both stub answers and over-verbose padding?
4. For adversarial cases: what is the correct behavior - refusal, redirection, or partial answer?
5. For noise cases: should the system respond helpfully, ask for clarification, or return an error?
6. Would this record still be valid if the backend model was swapped for a different LLM?

---

## Part B: Critique an Existing Golden Test Set (20-30 minutes)

### Task
Open regression_testing/regression_testing.py in the course repo and read the `_load_test_cases()` method.

For each golden record in that file, evaluate it against the anatomy framework using this rubric:

| Dimension | Questions to ask |
|---|---|
| Input quality | Is it specific enough? Could it match too many or too few real queries? |
| Gold standard quality | Is it realistic? Does it contain every fact a passing response needs? |
| Keyword coverage | Are the keywords necessary and sufficient, or would a hallucinated answer also pass? |
| Length range | Does the range actually exclude bad responses (too short = stub, too long = padding)? |
| Edge case handling | For edge cases, is the expected behavior truly what you want in production? |

### Deliverables for Part B
1. A completed rubric for at least 4 of the existing records.
2. One proposed improvement for each record you graded.
3. One record you would add to the existing set that fills a gap you noticed.

### Submission Format (VM)
Submit one file named `exercise2_submission.md` (or PDF) containing:
1. Your 10 golden records from Part A.
2. Your Part B rubric results for at least 4 records.
3. Your proposed improvements and added gap record.

---

## Copilot support guidance
Copilot is useful here for structure and drafting, not for judgment.

Good Copilot uses:
1. Generate additional query variations for a category you are struggling with.
2. Suggest keyword lists for a gold standard you wrote.
3. Convert a prose pass criterion into a structured format.
4. Ask Copilot: "What adversarial prompts might a user try against a GenAI testing chatbot?"

Avoid:
1. Having Copilot write gold standards without verifying them against the knowledge base documents.
2. Accepting keyword lists without checking that they discriminate good responses from fluent hallucinations.
3. Using Copilot to critique the existing records - that analysis must come from you.

---

## Debrief questions
1. Which category was hardest to design: factual, reasoning, adversarial, or noise?
2. What happens to your regression suite if the gold standard itself is wrong?
3. In Part B, did any of the existing records have keywords that a hallucinated response could also satisfy?
4. How would your golden set change if the model was swapped for a different LLM?
