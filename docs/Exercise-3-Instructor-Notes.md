# Exercise 3: Instructor Notes (Simplified)

## Teaching goal
Teach students to audit evaluation signals and improve one metric using evidence.

## Quick prep (5 min)
1. Confirm each student has local 9-test suite output from Exercise 2.
2. Point students to latest result file in `regression_test_results/`.

## Facilitation flow (40-50 min)
1. 0-10 min: Explain false positive vs false negative in this context.
2. 10-25 min: Students find one FP and one FN from real outputs.
3. 25-35 min: Students propose one metric improvement.
4. 35-45 min: Teams discuss metric trade-offs and threshold choices.
5. 45-50 min: Share one "keep" and one "change" to framework.

## Instructor prompts to unblock teams
1. "Which threshold caused this wrong decision?"
2. "Would your new metric reduce noise or add noise?"
3. "What failure can still slip through after your fix?"

## What good output looks like
1. One documented FP and one documented FN with scores.
2. One concrete metric proposal with threshold and placement.
3. One explicit trade-off statement.

## Common pitfalls and interventions
1. Pitfall: Students invent issues not visible in results.
   Intervention: Require test ID + score evidence for every claim.
2. Pitfall: Metric proposals are vague.
   Intervention: Require function behavior and threshold in plain terms.
3. Pitfall: Overfitting to one case.
   Intervention: Ask how metric performs on at least one other test.

## End-of-exercise checkpoint
Each team submits one row: problem, metric change, expected improvement, residual risk.
