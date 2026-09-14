# Exercise 3: Analyze UI Golden-Run Evidence

## Prerequisites
1. Exercise 2 completed.
2. The Flask application and MLflow are running.
3. The Exercise 2 Playwright suite is available in the Testing beaker.

## Scenario

Exercise 2 gave you a small, black-box UI golden suite. Exercise 3 teaches you
to decide whether those tests are measuring the right things. You will analyze
the evidence captured by the browser suite, compare it with the corresponding
MLflow traces, and improve one validation rule.

This exercise does **not** use the legacy code-based regression suite as the
student workflow. The primary artifact is the JSON file produced by the
Playwright run under `artifacts/exercise2/`.

## Run the golden suite

From the Testing beaker, run all seven Exercise 2 tests. Or run:

```bash
python -m pytest tests/e2e/test_exercise2_ui.py -v
```

The suite writes an artifact named like:

```text
artifacts/exercise2/ui_golden_run_YYYYMMDD_HHMMSS.json
```

The artifact contains the test name, prompt, response text, sources, timing
fields, session ID, exercise number, and observed validation data. It is the
starting point for your analysis.

## Student tasks

1. Open the newest `ui_golden_run_*.json` file.
2. Select one successful in-scope case and one case that failed or returned a
   bounded validation error.
3. For each selected case, record:
   - response status and mode
   - response length
   - source count and source metadata
   - response, retrieval, generation, and total latency
   - whether the UI behavior matched the API payload
4. Use `session_id` and `exercise_number` to find the matching trace in MLflow.
5. Compare the trace to the browser evidence:
   - Did the trace contain `rag.query`, `rag.retrieve`, and `rag.generate`?
   - Did retriever and generator spans contain inputs and outputs?
   - Did the trace duration agree with the API timing?
   - Was the answer grounded in the retrieved source content?
6. Identify one **test false positive** or **test false negative**:
   - false positive: the suite passed, but trace/source evidence shows the
     answer was not grounded or not useful
   - false negative: the suite failed, but trace/source evidence shows the
     response was an acceptable answer with expected model variation
7. Ask Copilot to propose one better validation rule. Examples:
   - require a source whose content overlaps the answer's key concept
   - require a minimum source count only for in-scope RAG questions
   - replace one brittle keyword with a small synonym set
   - add a bounded latency warning without failing on latency alone
8. Add the rule to the Playwright suite, rerun it, and compare the new JSON
   artifact with the original.
9. Explain whether the new rule reduced false signals or introduced a new risk.

## Evidence table

| Case | Test result | Response/source evidence | MLflow trace evidence | Classification | Proposed rule |
|---|---|---|---|---|---|
| Selected case 1 |  |  |  |  |  |
| Selected case 2 |  |  |  |  |  |

## What makes a good validation rule?

A useful rule should be:

- observable through the UI or response payload
- tolerant of reasonable wording variation
- tied to a real user or system requirement
- explainable when it fails
- connected to trace evidence when the issue is grounding, retrieval, latency,
  tool behavior, or an orchestration decision

Do not turn the generated answer into an exact snapshot. Exact prose matching
will make the suite brittle without improving its ability to detect meaningful
regressions.

## Team debrief

1. Which UI assertion was insufficient without MLflow trace evidence?
2. Which source or span field gave the strongest grounding signal?
3. Did your improved rule catch a real defect or merely a wording variation?
4. Which validation belongs in the browser suite, and which belongs in a trace
   or evaluation report?
