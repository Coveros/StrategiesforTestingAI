# Exercise 3: Analyze UI Golden-Run Evidence

## Prerequisites
1. Exercise 2 completed
2. Updated Playwright Golden UI Test Suite has been run and is available for analysis

## Scenario

Exercise 2 gave you a small, black-box UI golden suite. In this exercise, you
will decide whether those tests are measuring the right things by reviewing the
observable evidence captured during a browser test run. You do not need to read
the application code or diagnose its internal implementation.

The primary artifact is the JSON file produced by the Playwright run under
`artifacts/exercise2/`. It records what the browser and API response observed.

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
   - source count, source names, and similarity values
   - response, retrieval, generation, and total latency
   - whether the UI behavior matched the API payload
4. Review the returned evidence as a black-box tester:
   - Do the sources appear relevant to the question and answer?
   - Is the response useful without requiring one exact wording?
   - Is an error understandable and appropriately bounded?
   - Do the timing values suggest a result that is practical for a user?
5. Identify one **test false positive** or **test false negative**:
   - false positive: the suite passed, but the returned response or source
     evidence is not useful or does not appear grounded
   - false negative: the suite failed, but the returned response and source
     evidence are acceptable despite reasonable model wording variation
6. Ask Copilot to propose one better validation rule. Examples:
   - require a source whose content overlaps the answer's key concept
   - require a minimum source count only for in-scope RAG questions
   - replace one brittle keyword with a small synonym set
   - add a bounded latency warning without failing on latency alone
7. Add the rule to the Playwright suite, rerun it, and compare the new JSON
   artifact with the original.
8. Explain whether the new rule reduced false signals or introduced a new risk.

## Evidence table

| Case | Test result | Response/source evidence | Timing evidence | Classification | Proposed rule |
|---|---|---|---|---|---|
| Selected case 1 |  |  |  |  |  |
| Selected case 2 |  |  |  |  |  |

## What makes a good validation rule?

A useful black-box rule should be:

- observable through the UI or response payload
- tolerant of reasonable wording variation
- tied to a real user or system requirement
- explainable when it fails
- based on returned evidence, rather than an assumption about the internal
  implementation

Do not turn the generated answer into an exact snapshot. Exact prose matching
will make the suite brittle without improving its ability to detect meaningful
regressions.

## Team debrief

1. Which assertion was most useful for judging response quality?
2. Which returned source field gave the strongest grounding signal?
3. Did your improved rule catch a real defect or merely a wording variation?
4. What extra evidence would help you investigate an ambiguous test result?
