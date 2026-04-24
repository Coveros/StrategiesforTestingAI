# Exercise 9: Instructor Notes (Simplified)

## Teaching goal
Make a release decision using evidence from automated and/or manual gate checks.

## Quick prep (5 min)
1. Run: `python section9_agentic_test_suite.py`
2. Locate artifacts in `regression_test_results/`.
3. Confirm teams understand baseline vs candidate mapping in this lab.

## Facilitation flow (40-50 min)
1. 0-10 min: Review gate outputs and decision rules.
2. 10-25 min: Each role lens builds one ship/no-ship argument from artifacts.
3. 25-35 min: Team vote and rationale.
4. 35-45 min: Draft shift-right plan and rollback rule.
5. 45-50 min: Compare decisions across teams.

## Instructor prompts to unblock teams
1. "If gate says FAIL, what evidence would justify override?"
2. "Which single metric would trigger rollback first?"
3. "What risk are you consciously accepting?"

## What good output looks like
1. Decision table completed with evidence per role.
2. Explicit ship/no-ship rationale tied to gate metrics.
3. Three-metric monitoring plan plus rollback trigger.

## Common pitfalls and interventions
1. Pitfall: Opinion-based decisions.
   Intervention: Require each claim to cite artifact field(s).
2. Pitfall: Ignoring warning-level risk.
   Intervention: Require mitigation even when not FAIL.
3. Pitfall: No operational follow-through.
   Intervention: Enforce concrete alert thresholds and owner actions.

## End-of-exercise checkpoint
Each team states final decision, top reason, and first 24-hour reversal trigger.
