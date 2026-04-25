# Exercise 9: Make a Ship/No-Ship Release Decision

## Prerequisites
1. App running locally (`python run.py`).
2. Copilot Chat in Codespaces.
3. Ability to view tool calls or traces using Agent Mode in the UI.
4. Instructor mode enabled to force trace visibility and crew mode when needed.

## Scenario
You are the release board deciding Ship/No-Ship using baseline versus candidate evidence.

## What baseline vs candidate means in this lab
1. **Baseline**: control run with the default persona. In this lab, treat it as the "current acceptable release behavior" reference.
2. **Candidate**: comparison run with a style-shift persona. In this lab, the style-shift uses a pirate-like response style (for example, "Ahoy matey ... Arrr") to simulate prompt/config drift and stress release gates.
3. You are not comparing two separate deployed systems. You are comparing two test conditions from the same suite to practice release-gate decision-making.
4. Use baseline vs candidate deltas (gate decision, pass-rate drop, and reasons) to decide Ship/No-Ship.

## Student tasks
1. Open `http://localhost:5000/?exercise=9&instructor=1` and enable **Agent Mode**, **Show Trace**, and **Crew Mode**.
2. Run the Section 9 automation suite:
	- `python section9_agentic_test_suite.py`
3. Open the two generated artifacts in `regression_test_results/`:
	- `section9_agentic_ci_*.json`
	- `section9_agentic_ci_summary_*.txt`
4. Extract these fields for your decision table:
	- gate decision: `PASS`, `PASS_WITH_WARNINGS`, or `FAIL`
	- reasons list
	- baseline pass rate
	- candidate (style-shift) pass rate
	- baseline and candidate latency indicators from the summary output
	- pass rate drop
5. Compare pass rate and latency between baseline and candidate.
6. Apply the **Decision workflow (required)** section below before writing recommendations.
7. Each person creates a short decision memo summarizing the evidence and their Ship/No-Ship recommendation with rationale. It should include:
	- A summary of the gate decision and key evidence points.
	- A clear Ship/No-Ship recommendation based on the decision workflow below.
	- If Ship, any accepted risks or mitigations.
	- If No-Ship, the main reasons and proposed next steps to address them.
8. Conduct a final board vote and record your decision for discussion.

## Decision workflow (required)
Use this checklist to make your final decision:
1. Apply gate status first:
	- If gate decision is `FAIL`, default to **No-Ship**.
2. Apply pass-rate threshold next:
	- If pass rate drop is greater than 0.25, default to **No-Ship**.
3. Handle warning cases explicitly:
	- If decision is `PASS_WITH_WARNINGS`, Ship is allowed only with explicit mitigations and rollback triggers.
4. Record the board outcome:
	- Final decision (Ship or No-Ship)
	- Top 2 evidence reasons
	- Required mitigations and rollback criteria

## Team debrief questions
1. Which metric carried the most weight in your decision?
2. What release risk did your team accept on purpose?
3. What condition would make you reverse the decision within 24 hours?

