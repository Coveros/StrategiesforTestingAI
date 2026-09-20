# Exercise 4 Instructor Notes: Ask Mode Trace Analysis
Facilitator reference: [Instructor Facilitation Rubric](Exercise-Instructor-Facilitation-Rubric.md)

## Prerequisites
1. Exercise 3 completed.
2. A running GenAI testing assistant in your Codespace at [http://localhost:5000](http://localhost:5000).
3. A running MLflow instance in your Codespace at [http://localhost:5001](http://localhost:5001).
4. An MLflow demo has been completed.

## Scenario
This exercise focuses on **Ask mode**, the deterministic RAG pipeline. A user asks one question, the app retrieves context from the vector database, and then sends the query plus context to the LLM in one straight shot. In MLflow, students should see a clean linear trace with the expected 3-span structure: **Chains -> Retriever -> LLM**.

## Review Workflow: Shared Cross-Mode Demo

Before teams begin, run this prompt once as the instructor demonstration:

```text
How do I detect hallucinations in RAG systems?
```

Review it in **Ask** mode and show the class:

1. The answer, source names, similarity values, and timing fields in the UI.
2. The matching MLflow trace with `rag.query`, `rag.retrieve`, and `rag.generate`.
3. The retrieved document outputs and generated answer in the Inputs/Outputs panels.

Tell teams to keep their Exercise 4 case assignments. Each student will run
that same prompt in Agent mode for Exercise 5 and Crew mode for Exercise 6,
then compare answer quality, tool calls, handoffs, latency, and trace shape.

The demonstration prompt is not one of the assigned prompts, so it provides a
shared example without duplicating a student's case.

## Instructor Preparation: What to Watch For

### Signals Students Should Notice
1. Ask mode should present a stable 3-span flow (`rag.query` -> `rag.retrieve` -> `rag.generate`).
2. Retrieval quality and generation quality are separate failure surfaces.
3. Similarity values and source metadata should be used as evidence, not just answer fluency.

### Likely Issues, Defects, or Quality Challenges
1. Students may misclassify generation defects as retrieval defects without trace evidence.
2. Low-similarity sources may still yield plausible answers that mask grounding issues.
3. Teams may treat timing variance as correctness variance.

### Prompt-Specific Teaching Issue to Highlight
If students do not identify the issue, highlight the exact failure mode in the case prompts:
- The assigned cases are deliberately chosen so that a fluent answer may still be weak if the source evidence is irrelevant, low-similarity, or missing.
- Students should notice that a response can sound polished yet still fail context precision or grounding checks.
- The key teaching issue is separating retrieval quality from generation quality: the app may answer confidently, but the trace reveals whether it used relevant context.
- In the shared demo prompt, the issue to flag is the difference between a plausible answer and a grounded answer supported by relevant sources.

### Recommended Modifications to Discuss
1. Add explicit retrieval acceptance checks (minimum similarity/source expectations by case).
2. Improve chunking or metadata filtering when recall/precision failures dominate.
3. Add one automated trace-shape assertion for Ask mode in CI/smoke runs.

## Student tasks
1. Open the UI at `http://localhost:5000/?exercise=4` and stay in **Ask** mode.
2. Open MLflow at `http://localhost:5001` and prepare to inspect traces.
3. Use the five case assignments from Exercise 4, keeping the same person-to-case mapping for Exercises 5 and 6.
   - `case1`: What are the key differences between black-box and white-box testing for GenAI?
   - `case2`: According to production best practices, what is the recommended batch size for GenAI evaluations?
   - `case3`: Explain hallucination in the context of GenAI testing.
   - `case4`: What evidence should a golden UI test use instead of exact generated prose?
   - `case5`: What should a tester do when a GenAI response has no relevant source evidence?
4. For each query response in the UI, capture these evidence fields:
   - `response`
   - top 3 `sources[*].metadata.source`
   - top 3 `sources[*].similarity`
   - `retrieval_time`, `generation_time`, `total_time`
5. In MLflow, locate the trace that matches the request and confirm its path is the expected straight-line sequence:
   - `Chains` -> `rag.query`
   - `Retriever` -> `rag.retrieve`
   - `LLM` -> `rag.generate`
6. Inspect the Inputs/Outputs panels and record, when present:
   - query and prompt inputs
   - retrieved document outputs
   - generated answer output
   - `generation_metrics.prompt_tokens`, `generation_metrics.completion_tokens`, and `generation_metrics.total_tokens`
   - total trace duration compared with API `total_time`
7. Classify the result as Context Precision, Groundedness, Context Recall, or **No confirmed bug**.
8. Assign an owning team for each defect: AI Engineer, Software Developer, or Shared.
9. Add one concise row to the team evidence table.
10. Write one short bug report using this template:
   - Case ID
   - Bug title
   - Expected behavior
   - Actual behavior
   - Trace and UI/API evidence
   - Failure type
   - Owning team
   - Recommended fix

## Team Evidence Table

| Case ID | Analyst | UI/API evidence | MLflow trace evidence | Classification | Owner |
|---|---|---|---|---|---|
| case1 |  |  |  |  |  |
| case2 |  |  |  |  |  |
| case3 |  |  |  |  |  |
| case4 |  |  |  |  |  |
| case5 |  |  |  |  |  |

## Contingency only (if live tracing is unavailable)
Use precomputed evidence only when the live path is blocked (for example: local provider outage, network failure, or MLflow service unavailable):
- `artifacts/precomputed/trace_samples/exercise4_trace_cases_20260416_190513.json`

## Team debrief questions
1. Did every assigned Ask-mode run stay a 3-span linear trace? If not, where did it diverge?
2. Which trace evidence most clearly explained something the UI/API evidence alone could not?
3. Which single fix should be prioritized first, and what evidence supports that decision?


