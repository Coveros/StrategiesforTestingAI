# Exercise 3: Audit Test Results and Improve a Metric

## Prerequisites
1. Exercise 2 completed with your local 9-test regression suite.
2. Regression test results from your Exercise 2 in `regression_test_results/`.
3. Copilot Chat in Codespaces.

## Scenario
Your team added 2 new tests to the golden test suite during Exercise 2. Now audit all 9 of your test results and find evaluation issues. The framework uses weighted thresholds (semantic similarity 40%, keyword match 25%, etc.) that might be too strict or too loose. You'll find one false positive and one false negative, then propose a metric improvement.

## Student tasks
1. Analyse your test results from Exercise 2 located in `regression_test_results/` using the **Analyzing Your Test Results** guide below this task list. 
2. Look at the scores for each test and identify:
   - One false positive: a test that failed but should have passed based on the response quality.
   - One false negative: a test that passed but should have failed due to issues in the response.
3. For each, document: Test ID, actual similarity/keyword scores, why the threshold decision was wrong.
4. Use Copilot to draft 1 new metric that would catch that gap (e.g., PII detector, source citation checker, JSON validator). Use the **Sample Copilot prompts for new metrics** below if helpful.
5. Propose where this metric would live in the framework and what threshold it should use.

## Analyzing Your Test Results

Look at each result in the test output:
- **Semantic Similarity** (40% weight): How close to gold standard? Threshold: 0.65 (dev) or 0.75 (staging)
- **Keyword Match** (25% weight): % of expected keywords found? Threshold: 0.25 (dev) or 0.6 (staging)
- **Length** (15% weight): Does response length fall in expected range?
- **Sources** (10% weight): Does response cite at least 1 source?
- **Performance** (5% weight): Response time < 15 sec?
- **Content** (5% weight): Response > 50 chars?

**False Positive Pattern (should pass but failed):**
- A test has strong semantic similarity, but one strict sub-score (for example, keyword match) drives the final decision to fail.
- Use your own run data to decide whether the weighting or threshold was too strict.

**False Negative Pattern (should fail but passed):**
- A test passes on aggregate scoring, but qualitative review shows a clear response quality issue (for example, mixed-signal, irrelevant, or unsafe content).
- Use your own run data to identify why the current metrics missed it.

Use findings from your own artifacts in `regression_test_results/`; do not reuse example IDs from this handout.

Note: the framework attempts live API mode first and automatically falls back to deterministic offline mode if network or rate-limit errors occur.

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

