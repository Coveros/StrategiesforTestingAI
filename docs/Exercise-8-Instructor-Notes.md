# Exercise 8: Instructor Notes (Simplified)

## Teaching goal
Run controlled red-team attacks and prioritize the most dangerous guardrail gap.

## Quick prep (5 min)
1. Confirm controlled classroom scope and safety rules.
2. Open `http://localhost:5000/?exercise=8&instructor=1`.
3. Enable Agent Mode and Show Trace (Crew optional).

## Facilitation flow (40-50 min)
1. 0-10 min: Assign attack vector roles and expected safe behavior.
2. 10-25 min: One primary attack attempt per student.
3. 25-35 min: Classify failures: Input Filter, Output Filter, Both, No Failure.
4. 35-45 min: Choose highest-risk attack path.
5. 45-50 min: Propose one guardrail fix with measurable acceptance criteria.

## Instructor prompts to unblock teams
1. "Did the model refuse clearly and consistently?"
2. "Where exactly did the defense fail: input, output, or retrieval path?"
3. "What is the smallest fix that would have blocked this?"

## What good output looks like
1. One logged attempt per vector with expected vs actual behavior.
2. Clear failure-layer classification.
3. One prioritized guardrail fix.

## Common pitfalls and interventions
1. Pitfall: Attack prompts too generic.
   Intervention: Push concrete adversarial phrasing and roleplay variants.
2. Pitfall: Teams stop after one pass.
   Intervention: Require one retry or variation for confirmation.
3. Pitfall: Unsafe experimentation scope creep.
   Intervention: Reiterate classroom-safe boundaries and no real harm content.

## End-of-exercise checkpoint
Each team shares one "captured flag" and one defense improvement.
