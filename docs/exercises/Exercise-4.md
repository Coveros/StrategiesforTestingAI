# Exercise 4: Ask Mode Trace Analysis

## Prerequisites
1. Exercise 3 completed.
2. The GenAI testing assistant is running at [http://localhost:5000](http://localhost:5000).
3. MLflow is running at [http://localhost:5001](http://localhost:5001).

## Scenario

Exercise 3 showed what a black-box test can observe from the UI and API
response. This group activity introduces MLflow tracing so you can see how an
Ask-mode request was executed.

In Ask mode, the app retrieves context from the vector database and sends the
query plus context to the LLM in one straight shot. Each request should produce
a clean linear trace with exactly three conceptual spans: **Chains -> Retriever
-> LLM**. Your team will divide the cases, inspect traces in parallel, then
compare findings and select one improvement to prioritize.

## Assign Cases

Form a team of three to five people. Assign one case to each person. For teams
of three or four, complete only the first three or four cases. Each person runs
their assigned query once in **Ask** mode and analyzes its matching trace.

| Case ID | Assigned query |
|---|---|
| case1 | What are the key differences between black-box and white-box testing for GenAI? |
| case2 | According to production best practices, what is the recommended batch size for GenAI evaluations? |
| case3 | Explain hallucination in the context of GenAI testing. |
| case4 | What evidence should a golden UI test use instead of exact generated prose? |
| case5 | What should a tester do when a GenAI response has no relevant source evidence? |

## Individual Trace Analysis

For your assigned case:

1. Open the UI at `http://localhost:5000/?exercise=4` and confirm **Ask** mode
   is selected.
2. Submit your assigned query. Record these UI/API evidence fields:
   - `response`
   - top 3 `sources[*].metadata.source`
   - top 3 `sources[*].similarity`
   - `retrieval_time`, `generation_time`, `total_time`
3. In MLflow, locate the trace that matches your request. Confirm its path is
   the expected straight-line sequence:
   - `Chains` -> `rag.query`
   - `Retriever` -> `rag.retrieve`
   - `LLM` -> `rag.generate`
4. Inspect the Inputs/Outputs panels and record, when present:
   - query and prompt inputs
   - retrieved document outputs
   - generated answer output
   - `generation_metrics.prompt_tokens`, `generation_metrics.completion_tokens`, and `generation_metrics.total_tokens`
   - total trace duration compared with API `total_time`
5. Classify the result as Context Precision, Groundedness, Context Recall, or
   **No confirmed bug**. If you identify a defect, propose its likely owner:
   AI Engineer, Software Developer, or Shared.
6. Add one concise row to the team evidence table.

## Team Synthesis

When every assigned case is complete, compare the traces and evidence together.

1. Confirm whether every case followed the expected three-span structure.
2. Compare the retrieved sources with the final answer for each case.
3. Identify one difference between UI/API evidence and trace evidence that
   changed, clarified, or strengthened your interpretation.
4. Select the most important confirmed issue, or state that no issue was
   confirmed.
5. Write one short, evidence-based bug report using this template:
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
1. Did every assigned Ask-mode run stay a three-span linear trace? If not, where did it diverge?
2. Which trace evidence most clearly explained something the UI/API evidence alone could not?
3. Which single fix should be prioritized first, and what evidence supports that decision?

