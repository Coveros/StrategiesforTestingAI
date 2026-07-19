# Exercise 4: Ask Mode Trace Analysis

## Prerequisites
1. Exercise 3 completed.
2. A running GenAI testing assistant in your Codespace at [http://localhost:5000](http://localhost:5000).
3. A running Arize Phoenix instance in your Codespace at [http://localhost:6006](http://localhost:6006).
4. An Arize Phoenix demo has been completed.

## Scenario
This exercise focuses on **Ask mode**, the deterministic RAG pipeline. A user asks one question, the app retrieves context from the vector database, and then sends the query plus context to the LLM in one straight shot. In Phoenix, students should see a clean linear trace with exactly 3 spans: **Chains -> Retriever -> LLM**.

## Student tasks
1. Open the UI at `http://localhost:5000/?exercise=4` and stay in **Ask** mode.
2. Open Phoenix at `http://localhost:6006` and prepare to inspect traces.
3. Run these 3 target queries in Ask mode:
   - What are the key differences between black-box and white-box testing for GenAI?
   - According to production best practices, what is the recommended batch size for GenAI evaluations?
   - Explain hallucination in the context of GenAI testing.
4. For each query response in the UI, capture these evidence fields:
   - `response`
   - top 3 `sources[*].metadata.source`
   - top 3 `sources[*].similarity`
   - `retrieval_time`, `generation_time`, `total_time`
5. In Phoenix, capture trace evidence and confirm whether the path is the expected straight-line sequence:
   - `Chains`
   - `Retriever`
   - `LLM`
   In this codebase, these conceptual labels appear with concrete span names:
   - `Chains` -> `rag.query`
   - `Retriever` -> `rag.retrieve`
   - `LLM` -> `rag.generate`
   Use this quick interpretation guide while reviewing traces:
   - `Chains` = top-level Ask mode workflow
   - `Retriever` = vector database lookup and ranking
   - `LLM` = answer generation from retrieved context
6. Record results in this table as you run each case:

| Case ID | Query | UI Evidence | Phoenix Evidence | Failure Type | Owner |
|---|---|---|---|---|---|
| case1 |  |  |  |  |  |
| case2 |  |  |  |  |  |
| case3 |  |  |  |  |  |

7. Note whether the trace stays deterministic in structure even when answer wording varies slightly.
8. For each case, classify the main defect as Context Precision, Groundedness, Context Recall, or **No confirmed bug**.
9. Assign an owning team for each defect: AI Engineer (model or prompt behavior), Software Developer (application or integration behavior), or Shared.
10. Write 3 short bug reports with one recommended fix each, using this template:
   - Bug title
   - Expected behavior
   - Actual behavior
   - Failure type
   - Owning team
   - Recommended fix
11. Use the same 3 case IDs (`case1`, `case2`, `case3`) in your bug reports so your evidence is easy to audit.

## Contingency only (if live tracing is unavailable)
Use precomputed evidence only when the live path is blocked (for example: local provider outage, network failure, or Phoenix service unavailable):
- `artifacts/precomputed/trace_samples/exercise4_trace_cases_20260416_190513.json`

## Team debrief questions
1. Did every Ask mode run stay a 3-span linear trace? If not, where did it diverge?
2. What trace evidence was most persuasive for separating retrieval issues from generation issues?
3. Which single fix should be prioritized first?

