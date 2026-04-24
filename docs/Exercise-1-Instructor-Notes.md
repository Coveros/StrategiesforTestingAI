# Exercise 1: Instructor Notes (Simplified)

## Teaching goal
Help students discover why GenAI testing needs human judgment, variability handling, and risk-focused evaluation.

## Quick prep (5 min)
1. Confirm app is running: `python run.py`
2. Open `http://localhost:5000/?exercise=1`
3. Confirm each student has one charter role.

## Facilitation flow (40-50 min)
1. 0-5 min: Brief scenario and role split.
2. 5-20 min: Each student runs 2 prompts in their charter.
3. 20-30 min: Students rerun same prompts and compare output variation.
4. 30-40 min: Team classifies outcomes: Acceptable, Needs Follow-up, Risky, Out-of-Scope.
5. 40-50 min: Debrief with risk-first discussion.

## Instructor prompts to unblock teams
1. "What changed between run 1 and run 2, and does that change matter?"
2. "Which failures are true risk vs cosmetic variation?"
3. "Where would exact string assertions fail unfairly?"

## What good output looks like
1. Each charter has 2 prompts with observations.
2. Team identifies at least 2 examples of acceptable variation.
3. Team identifies at least 1 high-risk behavior needing follow-up.

## Common pitfalls and interventions
1. Pitfall: Students treat all variation as failure.
   Intervention: Ask them to define user impact and risk level.
2. Pitfall: Prompts are too easy.
   Intervention: Push boundary, adversarial, and factual prompts.
3. Pitfall: No rerun comparison.
   Intervention: Require second run evidence before debrief.

## End-of-exercise checkpoint
Ask each team for one statement: "The most important GenAI-specific testing insight we learned is..."
