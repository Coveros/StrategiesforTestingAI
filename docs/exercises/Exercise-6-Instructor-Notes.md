# Exercise 6 Instructor Notes: Multi-Agent Handoff and Trajectory Analysis

## Prerequisites
1. A running GenAI testing assistant in your Codespace at [http://localhost:5000](http://localhost:5000).
2. A running Arize Phoenix instance in your Codespace at [http://localhost:6006](http://localhost:6006).
3. An Arize Phoenix demo has been completed.
4. GitHub Copilot has been activated in Visual Studio Code in this Codespace.
5. A GitHub Copilot demo has been completed.
6. Agent mode enabled in the UI.
7. Ability to capture trace/trajectory evidence.

## Scenario
You are auditing a real multi-agent flow in LangChain with three roles: **Triage Agent**, **RAG Specialist**, and **Validator Agent**. The orchestrator routes work between specialist capabilities instead of forcing retrieval every time. Your goal is to study the hand-off graph in Phoenix and diagnose how corrupted state can break retrieval.

## Student tasks
1. Open: `http://localhost:5000/?exercise=6`.
2. Keep startup mode as **Ask**, then switch to **Agent**.
3. Ensure **Crew Mode is ON** (Exercise 6 defaults this automatically outside instructor mode).
4. Use these queries during this exercise:
	- Compare two test strategies for a GenAI support bot and recommend one.
	- Create a release test plan with risks, gates, and rollback criteria.
	- Summarize noisy bug reports into top root causes and priorities.
	- Design fairness tests for a multilingual assistant.
	- Write a production readiness memo using retrieval, groundedness, and latency findings.
	- simulate handoff corruption for retrieval query about 2024 regression failures.
5. Run one non-corruption query first and capture baseline evidence from metadata.
	- In the response's **Agent Execution** block, capture: `Trajectory` (steps/tools/handoffs/redundant), `Tools Called`, and `Trace` (if shown).
	- Record this as your baseline row for that query.
6. In Phoenix, inspect the baseline run as an agent graph and confirm you can see the flow between **Triage Agent**, **RAG Specialist**, and **Validator Agent**.
7. Run the handoff-corruption scenario: `simulate handoff corruption for retrieval query about 2024 regression failures`.
8. Capture corrupted-run evidence from UI metadata and Phoenix traces.
9. Compare baseline vs corrupted run for handoff count, retrieval quality, and redundant tool calls.
10. Record results in this table for both runs:

| Run Type | Query | Actual Steps | Optimal Steps | Efficiency Score | Handoff Quality Note | Evidence |
|---|---|---:|---:|---:|---|---|
| Baseline |  |  |  |  |  |  |
| Corrupted |  |  |  |  |  |  |

11. In Phoenix, click into the hand-off between **Triage Agent** and **RAG Specialist** and compare the original query with the routed query.
12. Calculate Efficiency Score = Optimal Steps / Actual Steps.
13. As a team, propose one fix for handoff integrity and one guardrail for loop control.
14. As a control, run the same corruption prompt once with **Crew Mode OFF** and note that the handoff mutation should not appear in the single-agent path.

## Team debrief questions
1. What caused the worst inefficiency: loop, bad handoff, or over-delegation?
2. Where exactly was input corrupted in the handoff chain?
3. What orchestrator rule or schema check would prevent this next time?


