# Exercise 4: Instructor Notes (Simplified)

## Teaching goal
Train fast RAG diagnosis: retrieval issue, generation issue, or shared ownership.

## Quick prep (5 min)
1. Confirm app is running and UI reachable.
2. Confirm fallback artifact exists: `artifacts/precomputed/trace_samples/exercise4_trace_cases_20260416_190513.json`

## Facilitation flow (40-50 min)
1. 0-5 min: Review failure types: Context Precision, Groundedness, Context Recall.
2. 5-20 min: Teams run 3 target queries in UI and capture evidence.
3. 20-30 min: Teams classify each case and assign owner.
4. 30-40 min: Teams write 3 short bug reports with one fix each.
5. 40-50 min: Cross-team compare hardest classification.

## Instructor prompts to unblock teams
1. "What source evidence supports your classification?"
2. "Is this mostly retrieval miss, generation misuse, or both?"
3. "What is the smallest fix with highest impact?"

## What good output looks like
1. Three cases with evidence fields captured.
2. Clear classification per case.
3. Owner assigned with realistic fix recommendation.

## Common pitfalls and interventions
1. Pitfall: Classification by intuition only.
   Intervention: Require source/similarity/time evidence in each report.
2. Pitfall: Blaming one team for shared failures.
   Intervention: Encourage shared ownership when evidence is mixed.
3. Pitfall: No fallback path used when live calls fail.
   Intervention: Allow precomputed trace sample usage.

## End-of-exercise checkpoint
Each team states: "Highest-priority bug is X because evidence Y implies risk Z."
