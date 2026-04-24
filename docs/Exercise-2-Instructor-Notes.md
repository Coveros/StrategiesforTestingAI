# Exercise 2: Instructor Notes (Simplified)

## Teaching goal
Move from exploratory prompts to a reusable golden test pack with clear pass/fail rules.

## Quick prep (5 min)
1. Confirm students completed Exercise 1 prompts.
2. Confirm regression framework runs: `python regression_testing/regression_testing.py`
3. Confirm fallback behavior message appears if API/rate limit issues occur.

## Facilitation flow (40-50 min)
1. 0-10 min: Run baseline 7-test suite and review output format.
2. 10-25 min: Each student drafts 1 new test case for assigned category.
3. 25-35 min: Add tests into `_load_test_cases()` and rerun suite.
4. 35-45 min: Review pass/fail disagreements and tighten rubrics.
5. 45-50 min: Confirm final mini pack and pass rate.

## Instructor prompts to unblock teams
1. "Is this gold standard measurable or subjective?"
2. "What keyword evidence is essential vs optional?"
3. "If this test fails, do we learn something actionable?"

## What good output looks like
1. Baseline run executed successfully.
2. New tests added and suite rerun.
3. Team can explain why each pass/fail rule is deterministic.

## Common pitfalls and interventions
1. Pitfall: Gold standards too long/ambiguous.
   Intervention: Force 1-2 sentence expected response with explicit must-include terms.
2. Pitfall: Duplicate tests.
   Intervention: Require unique risk intent per test.
3. Pitfall: Ignoring fallback mode.
   Intervention: Ask team to record execution mode (live vs offline fallback).

## End-of-exercise checkpoint
Each team reports: final test count, pass rate, and one test they would run weekly.
