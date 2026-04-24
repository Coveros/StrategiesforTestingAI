# Exercise 6: Instructor Notes (Simplified)

## Teaching goal
Measure trajectory efficiency and handoff quality in agent and multi-agent runs.

## Quick prep (5 min)
1. Open `http://localhost:5000/?exercise=6`.
2. Confirm students can switch Ask to Agent.
3. Confirm instructor mode path for Crew toggle: `?exercise=6&instructor=1`.

## Facilitation flow (40-50 min)
1. 0-10 min: Explain Actual Steps, Optimal Steps, Efficiency Score.
2. 10-25 min: Students run one complex query and capture trajectory metrics.
3. 25-35 min: Students rerun with Crew mode (optional comparison).
4. 35-45 min: Teams compute efficiency and identify worst loop.
5. 45-50 min: Propose one orchestrator rule fix.

## Instructor prompts to unblock teams
1. "Where did unnecessary steps appear?"
2. "Did handoffs preserve intent or distort it?"
3. "Which step can be removed without quality loss?"

## What good output looks like
1. One trajectory per student with metrics captured.
2. Efficiency score calculated and discussed.
3. One concrete loop-reduction fix proposed.

## Common pitfalls and interventions
1. Pitfall: Confusing trace verbosity with inefficiency.
   Intervention: Focus on steps/tool calls/handoffs, not just output length.
2. Pitfall: No baseline for "optimal".
   Intervention: Require one-sentence optimal-path estimate before scoring.
3. Pitfall: No crew comparison when possible.
   Intervention: Encourage one side-by-side run.

## End-of-exercise checkpoint
Each team submits: worst trajectory, why it is costly, and one prevention rule.
