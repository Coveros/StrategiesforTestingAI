# Exercise 5: Instructor Notes (Simplified)

## Teaching goal
Evaluate agent behavior quality across routing, arguments, state, safety, and error handling.

## Quick prep (5 min)
1. Start app and open `http://localhost:5000/?exercise=5`.
2. Confirm students switch Ask to Agent.
3. Optional: open instructor mode for Show Trace.

## Facilitation flow (40-50 min)
1. 0-10 min: Explain five behavior pillars and evidence expectations.
2. 10-25 min: One focused test per role.
3. 25-35 min: Teams fill result table with expected vs actual.
4. 35-45 min: Rank defects by production risk.
5. 45-50 min: Pick one fix and one regression check.

## Instructor prompts to unblock teams
1. "Did the agent call the right tool for this request?"
2. "Was context preserved or leaked across turns?"
3. "Did the system fail safely when action was invalid?"

## What good output looks like
1. Evidence captured for all five pillars.
2. At least one high-severity defect identified or explicitly ruled out.
3. Prioritized fix list with rationale.

## Common pitfalls and interventions
1. Pitfall: Students grade answer text only.
   Intervention: Force tool/state/safety evidence in table.
2. Pitfall: No negative test for guardrails.
   Intervention: Require one disallowed action test.
3. Pitfall: Ambiguous pass/fail criteria.
   Intervention: Require a one-line expected behavior before each run.

## End-of-exercise checkpoint
Each team reports the single riskiest pillar and one weekly regression test for it.
