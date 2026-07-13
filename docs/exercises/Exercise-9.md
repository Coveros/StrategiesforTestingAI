# Exercise 9: Make a Ship / No-Ship Release Decision

## Prerequisites
1. App running locally (`python run.py`).
2. Copilot Chat in Codespaces.
3. Ability to view tool calls or traces using Agent Mode in the UI.
4. Instructor mode enabled to force trace visibility and crew mode when needed.
5. Section 9 automation suite available: `python section9_agentic_test_suite.py`.

## Scenario
You are the release board deciding Ship / No-Ship using baseline versus candidate evidence for the **current** agentic implementation.

## What baseline vs candidate means in this lab
1. **Baseline**: the current default persona and orchestration behavior.
2. **Candidate**: a style-drift configuration where the agent persona is switched to pirate mode to simulate prompt/config drift.
3. You are not comparing two separate deployed systems. You are comparing two controlled conditions from the same suite to practice release-gate decision-making.
4. The current suite focuses on behaviors that are actually implemented today:
	- routed factual answering
	- general-chat routing
	- harmful-content blocking
	- handoff-corruption observability

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
	- candidate pass rate
	- baseline and candidate latency indicators from the summary output
	- pass rate drop
5. Compare pass rate and latency between baseline and candidate.
6. Apply the **Decision workflow (required)** section below before writing recommendations.
7. Each person creates a short decision memo summarizing the evidence and their Ship / No-Ship recommendation with rationale. Include:
	- a summary of the gate decision and key evidence points
	- a clear Ship / No-Ship recommendation based on the workflow below
	- if Ship, any accepted risks or mitigations
	- if No-Ship, the main reasons and the first corrective action
8. Conduct a final board vote and record your decision.

## Decision workflow (required)
Use this checklist to make your final decision:
1. Apply gate status first:
	- If gate decision is `FAIL`, default to **No-Ship**.
2. Apply pass-rate threshold next:
	- If pass-rate drop is greater than `0.25`, default to **No-Ship**.
3. Handle warning cases explicitly:
	- If decision is `PASS_WITH_WARNINGS`, Ship is allowed only with explicit mitigations and rollback triggers.
4. Record the board outcome:
	- Final decision (Ship or No-Ship)
	- Top 2 evidence reasons
	- Required mitigations and rollback criteria

## What the current automation suite checks
1. **Routed factual answer** still works in crew mode.
2. **General-chat routing** still works in crew mode.
3. **Harmful content** is still blocked.
4. **Handoff corruption** is still observable in metrics and handoff state.
5. **Candidate drift** is detected when pirate-style output contaminates otherwise acceptable responses.

## Decision table
| Decision Area | Baseline Evidence | Candidate Evidence | Risk Level | Decision Impact |
|---|---|---|---|---|
| Routed factual answer |  |  |  |  |
| General-chat routing |  |  |  |  |
| Harmful-content blocking |  |  |  |  |
| Handoff-corruption observability |  |  |  |  |
| Overall gate result |  |  |  |  |

## Team debrief questions
1. Which metric carried the most weight in your decision?
2. Was the candidate rejected because of safety, orchestration quality, or style drift?
3. What single condition would make you reverse the decision within 24 hours?

