# Exercise 3 Instructor Notes: Audit Test Results and Improve a Metric

## Prerequisites
1. A running GenAI testing assistant in your Codespace at [http://localhost:5000](http://localhost:5000).
2. GitHub Copilot has been activated in Visual Studio Code in this Codespace.
3. A GitHub Copilot demo has been completed.
4. Exercise 2 completed with your 9-test regression suite in Codespaces.
5. Regression test results from your Exercise 2 in `regression_test_results/`.

## Scenario
Your team added 2 new tests to the golden test suite during Exercise 2. Now audit all 9 of your test results and find evaluation issues. The framework uses weighted thresholds (semantic similarity 40%, keyword match 25%, etc.) that might be too strict or too loose. You'll find one false positive and one false negative, then propose a metric improvement.

## Student tasks
1. Run regression tests and open the latest summary report in `regression_test_results/` (pattern: `regression_summary_YYYYMMDD_HHMMSS.txt`). Use this text report as the primary analysis artifact.
2. Analyse test results using the **Analyzing Your Test Results** guide below this task list.
3. Use the JSON file (`regression_results_YYYYMMDD_HHMMSS.json`) only when learners need deeper details beyond the summary report.
4. Look at the scores for each test and identify:
   - One false positive: a test that passed but should have failed based on response quality.
   - One false negative: a test that failed but should have passed based on response quality.
5. For each, document: Test ID, actual similarity/keyword scores, why the threshold decision was wrong.
6. Use Copilot to draft 1 new metric that would catch that gap (e.g., PII detector, source citation checker, JSON validator). Use the **Sample Copilot prompts for new metrics** below if helpful.
7. Propose where this metric would live in the framework and what threshold it should use.

## How to run and open the right artifact
1. Run regression tests:
   - `python -m regression_testing.regression_testing`
2. Open the latest summary report in `regression_test_results/`:
   - File name pattern: `regression_summary_YYYYMMDD_HHMMSS.txt`
3. Coach learners to use:
   - `CRITICAL FAILURES` and `BY CATEGORY` for triage.
   - `DETAILED RESULTS` for query/response previews, component scores, and gate checks.
4. Open JSON only if a learner needs full raw response text or custom parsing.

## Analyzing Your Test Results

Look at each result in the test output:
- **Semantic Similarity** (40% weight): How close to gold standard? Threshold for this exercise: 0.65
- **Keyword Match** (25% weight): % of expected keywords found? Threshold for this exercise: 0.25
- **Length** (15% weight): Does response length fall in expected range?
- **Sources** (10% weight): Does response cite at least 1 source?
- **Performance** (5% weight): Response time < 15 sec?
- **Content** (5% weight): Response > 50 chars?

Use these fixed lab thresholds for all submissions: Semantic Similarity 0.65 and Keyword Match 0.25.

**False Positive Pattern (passed but should fail):**
- A test passes gate checks, but qualitative review shows clear response issues (for example: irrelevant answer, unsafe content, missing grounding).
- Use run data to identify why current metrics allowed this.

**False Negative Pattern (failed but should pass):**
- A test is semantically correct enough for classroom use, but strict thresholding or exact keyword matching causes a fail.
- Use run data to identify which threshold/metric is too strict.

Use findings from your own artifacts in `regression_test_results/`; do not reuse example IDs from this handout.

Note: the framework attempts local Ollama mode first and automatically falls back to deterministic offline mode if provider or connectivity errors occur.

## Evidence template
| Finding Type | Test ID | Your Scores | Threshold Applied | Why Threshold is Wrong | Proposed Fix |
|---|---|---|---|---|---|
| False Positive |  |  |  |  |  |
| False Negative |  |  |  |  |  |

## Sample Copilot prompts for new metrics
1. "Write a Python function that returns True if a response contains any PII patterns (email, phone, SSN, credit card)."
2. "Write a Python function that checks whether a response explicitly cites at least one source, e.g., 'according to X' or 'from X document'."
3. "Write a Python function that validates whether JSON appears in a response and is syntactically valid."
4. "Write a Python function that detects whether a response contains an explicit refusal phrase like 'cannot', 'cannot answer', or 'outside my scope'."

## Team debrief questions
1. Which was easier to find in your results: false positives or false negatives?
2. Did your new metric target a real gap, or would it add false signals?
3. What trade-off does your metric introduce? (e.g., strictness vs. signal quality)


