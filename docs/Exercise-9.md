# Exercise 9: Make a Ship/No-Ship Release Decision

## Prerequisites
1. Access to baseline vs candidate CI output.
2. Team of up to 5 people.
3. Shared understanding of key metrics: pass rate and latency.

## Scenario
Your team is the Release Advisory Board. You must decide whether to ship v2.0 using evidence, not opinion.

## How to run this in the UI
1. Start the app: `python run.py`.
2. Open `http://localhost:5000/?exercise=9`.
3. Switch from **Ask** to **Agent** in the input bar.
4. For release-gate debugging, open `http://localhost:5000/?exercise=9&instructor=1` and enable **Agent Mode**, **Show Trace**, and **Crew Mode**.
5. Use the automation artifacts as primary evidence for the final Ship/No-Ship decision.

## How to generate decision evidence
1. Run the Section 9 automation suite:
	- `python section9_agentic_test_suite.py`
2. Open the two generated artifacts in `regression_test_results/`:
	- `section9_agentic_ci_*.json`
	- `section9_agentic_ci_summary_*.txt`
3. Extract these fields for your decision table:
	- gate decision: `PASS`, `PASS_WITH_WARNINGS`, or `FAIL`
	- reasons list
	- baseline pass rate
	- pirate pass rate
	- pass rate drop
4. Treat baseline run as "current release behavior" and pirate run as "candidate under adversarial regression risk".

## What baseline vs candidate means in this lab
1. **Baseline**: default persona run from the suite.
2. **Candidate**: pirate persona run from the suite (simulates risky config/prompt drift).
3. Use these two runs as your release comparison inputs.

## Student tasks
1. Assign 5 role lenses:
	- Person 1: Safety / Policy Compliance
	- Person 2: Quality / Correctness
	- Person 3: Reliability / Failure Handling
	- Person 4: Latency / Performance
	- Person 5: Release Manager / Final Gate
2. Each person records baseline vs candidate evidence from the same artifact pair.
3. Each person gives one evidence-based recommendation: Ship or No-Ship.
4. Team votes and records one final decision with rationale.
5. Define a minimal shift-right plan: 3 metrics + rollback rule.

## Decision rule (use this first, then discuss)
1. If gate decision is `FAIL`, default to **No-Ship**.
2. If pass rate drop is greater than 0.25, default to **No-Ship**.
3. If decision is `PASS_WITH_WARNINGS`, team may Ship only with explicit mitigations and rollback triggers.

## Sample decision prompts
1. The gate output says `FAIL` due to `showstopper_failure_in_pirate_run`. Do you still ship? Why or why not?
2. Baseline pass rate is 1.0 and candidate pass rate is 0.67. Is this acceptable for release?
3. If latency improves but safety weakens, which metric wins your vote?

Rollback rule: If the release is shipped and any of the key metrics (accuracy, latency, safety) degrade beyond acceptable thresholds, revert to the previous version.

## Team debrief questions
1. Which metric carried the most weight in your decision?
2. What release risk did your team accept on purpose?
3. What condition would make you reverse the decision within 24 hours?

