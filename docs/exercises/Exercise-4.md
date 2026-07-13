# Exercise 4: Ask Mode Trace Analysis

## Prerequisites
1. GenAI testing assistant is started locally (`python run.py`).
2. Arize Phoenix is available locally and reachable on port `6006`.
3. GitHub Copilot Chat available in Codespaces.
4. Access to `artifacts/precomputed/trace_samples/exercise4_trace_cases_20260416_190513.json` as a fallback if live API calls fail.

## Scenario
This exercise focuses on **Ask mode**, the deterministic RAG pipeline. A user asks one question, the app retrieves context from the vector database, and then sends the query plus context to the LLM in one straight shot. In Phoenix, students should see a clean linear trace with exactly 3 spans: **Chains → Retriever → LLM**.

## Student tasks
1. Open the UI at `http://localhost:5000/?exercise=4` and stay in **Ask** mode.
2. Open Phoenix at `http://localhost:6006` and prepare to inspect traces while you run the 3 target queries listed below.
3. For each query response in the UI, capture these evidence fields:
	- `response`
	- top 3 `sources[*].metadata.source`
	- top 3 `sources[*].similarity`
	- `retrieval_time`, `generation_time`, `total_time`
4. In Phoenix, confirm whether the trace is the expected straight-line path:
	- `Chains`
	- `Retriever`
	- `LLM`
5. Note whether the trace stays deterministic in structure even when answer wording varies slightly.
6. Record your findings in a small table with columns: Case ID, Query, Evidence, Failure Type, Owner.
7. If live calls fail (network/rate-limit), use precomputed evidence:
	- `artifacts/precomputed/trace_samples/exercise4_trace_cases_20260416_190513.json`
8. For each case, classify the main defect as Context Precision, Groundedness, Context Recall, or **No confirmed bug**.
9. Assign an owning team for each defect: AI Engineer (model or prompt behavior), Software Developer (application or integration behavior), or Shared.
10. Write 3 short bug reports with one recommended fix each.
11. Use the same 3 case IDs (`case1`, `case2`, `case3`) in your bug reports so your evidence is easy to audit.

## Trace interpretation guide
1. `Chains` represents the top-level Ask mode workflow.
2. `Retriever` represents vector database lookup and ranking.
3. `LLM` represents answer generation from the retrieved context.
4. The main testing focus is groundedness, context relevance, and regression stability.
5. If the trace is not linear, treat that as an application bug because Ask mode is supposed to be a straight-through pipeline.

## Target queries
1. What are the key differences between black-box and white-box testing for GenAI?
2. According to production best practices, what is the recommended batch size for GenAI evaluations?
3. Explain hallucination in the context of GenAI testing.

## Bug report template
- Bug title
- Expected behavior
- Actual behavior
- Failure type
- Owning team
- Recommended fix

## Team debrief questions
1. Did every Ask mode run stay a 3-span linear trace? If not, where did it diverge?
2. What trace evidence was most persuasive for separating retrieval issues from generation issues?
3. Which single fix should be prioritized first?

