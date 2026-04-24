# Exercise 7: Instructor Notes (Simplified)

## Teaching goal
Stress non-functional behavior and identify weakest resilience point.

## Quick prep (5 min)
1. Open `http://localhost:5000/?exercise=7&instructor=1`.
2. Enable Agent Mode and Show Trace (optional Crew Mode).
3. Keep quick-run fallback available: `python section7_nfr_quickrun.py`.

## Facilitation flow (40-50 min)
1. 0-10 min: Assign NFR roles and review simulation prompts.
2. 10-25 min: Students run role-specific stress tests.
3. 25-35 min: Fill NFR scorecard with evidence fields.
4. 35-45 min: Rank weakest link by production impact.
5. 45-50 min: Select one resilience fix and one automation target.

## Instructor prompts to unblock teams
1. "Did failure degrade safely or fail silently?"
2. "What metric proves this issue, not opinion?"
3. "Would this be detectable within 5 minutes in production?"

## What good output looks like
1. One stress result per role with evidence.
2. Clear pass/fail/mixed classification per NFR area.
3. One prioritized resilience fix.

## Common pitfalls and interventions
1. Pitfall: "Simulate" prompts are improvised.
   Intervention: Require exact provided simulation prompts.
2. Pitfall: Teams claim cost analysis without data.
   Intervention: Keep focus on response_time and trajectory metrics available in UI.
3. Pitfall: No repeat run for stability.
   Intervention: Require at least one repeated prompt for consistency check.

## End-of-exercise checkpoint
Each team reports: weakest NFR area, evidence, and first automation check.
