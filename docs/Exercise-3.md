# Exercise 3: Audit Test Results and Improve a Metric

## Prerequisites
1. Exercise 2 completed with your local 9-test regression suite (7 base + 2 of your own tests).
2. Regression test results from your Exercise 2 run: `python regression_testing/regression_testing.py` (or check the saved results in `regression_test_results/`).
3. Copilot Chat in Codespaces.

## Scenario
Your team added 2 new tests to the golden suite. Now audit all 9 of your results and find evaluation issues. The framework uses weighted thresholds (semantic similarity 40%, keyword match 25%, etc.) that might be too strict or too loose. You'll find one false positive and one false negative, then propose a metric improvement.

## Student tasks
1. Run your 9-test suite: `python regression_testing/regression_testing.py` and save the output.
2. Find 1 false positive (test that failed but should have passed) and 1 false negative (test that passed but should have failed).
3. For each, document: Test ID, actual similarity/keyword scores, why the threshold decision was wrong.
4. Use Copilot to draft 1 new metric that would catch that gap (e.g., PII detector, source citation checker, JSON validator).
5. Propose where this metric would live in the framework and what threshold it should use.

## Analyzing Your Test Results

Look at each result in the test output:
- **Semantic Similarity** (40% weight): How close to gold standard? Threshold: 0.65 (dev) or 0.75 (staging)
- **Keyword Match** (25% weight): % of expected keywords found? Threshold: 0.25 (dev) or 0.6 (staging)
- **Length** (15% weight): Does response length fall in expected range?
- **Sources** (10% weight): Does response cite at least 1 source?
- **Performance** (5% weight): Response time < 15 sec?
- **Content** (5% weight): Response > 50 chars?

**False Positive Example (should pass but failed):**
- Test "hallucination_basic" scored semantic similarity 0.78 (passes threshold 0.75)
- But keyword match was 0.1 (failed threshold 0.6)
- Result: Test fails overall even though semantic similarity is high
- Question: Should keyword match be weighted 25% or 15%?

**False Negative Example (should fail but passed):**
- Test "edge_case_irrelevant" passed because semantic similarity 0.9 and keyword match 0.8
- But the response included irrelevant information mixed with proper refusal
- Question: Do we need a "purity" metric to detect mixed-signal responses?

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

