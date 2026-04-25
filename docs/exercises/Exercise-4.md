# Exercise 4: Diagnose RAG Failures Quickly

## Prerequisites
1. GenAI testing assistant is started locally (`python run.py`).
2. GitHub Copilot Chat available in Codespaces.
3. Access to `artifacts/precomputed/trace_samples/exercise4_trace_cases_20260416_190513.json` as a fallback if live API calls fail.

## Scenario
The Product Team reported three suspected bugs tied to a fixed query set. Your team must triage each case and decide whether it is mostly retrieval, mostly generation, shared ownership, or no confirmed bug.

## Student tasks
1. Open the UI at `http://localhost:5000/?exercise=4` and run the 3 target queries listed in the section below.
2. For each query response in the UI, capture these evidence fields:
	- `response`
	- top 3 `sources[*].metadata.source`
	- top 3 `sources[*].similarity`
	- `retrieval_time`, `generation_time`, `total_time`
3. Record your findings in a small table with columns: Case ID, Query, Evidence, Failure Type, Owner.
4. If live calls fail (network/rate-limit), use precomputed evidence:
	- `artifacts/precomputed/trace_samples/exercise4_trace_cases_20260416_190513.json`
5. For each case, classify the main defect as Context Precision, Groundedness, Context Recall, or **No confirmed bug**.
6. Assign an owning team for each defect: AI Engineer (model or prompt behavior), Software Developer (application or integration behavior), or Shared.
7. Write 3 short bug reports with one recommended fix each.
8. Use the same 3 case IDs (`case1`, `case2`, `case3`) in your bug reports so your evidence is easy to audit.

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
1. Which case was hardest to classify and why?
2. What trace evidence was most persuasive?
3. Which single fix should be prioritized first?

