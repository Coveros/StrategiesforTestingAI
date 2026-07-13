# Exercise 6: Multi-Agent Handoff and Trajectory Analysis

## Prerequisites
1. GenAI testing assistant is started locally (`python run.py`).
2. Ability to capture trace/trajectory evidence.
3. Arize Phoenix installed in the environment (`arize-phoenix`).
4. GitHub Copilot Chat available in Codespaces.
5. Agent mode enabled in the UI.
6. Phoenix is reachable at `http://localhost:6006`.

## Scenario
You are auditing a real multi-agent flow in LangChain with three roles: **Triage Agent**, **RAG Specialist**, and **Validator Agent**. The orchestrator routes work between specialist capabilities instead of forcing retrieval every time. Your goal is to study the hand-off graph in Phoenix and diagnose how corrupted state can break retrieval.

## Student tasks
1. Open: `http://localhost:5000/?exercise=6`.
2. Keep startup mode as **Ask**, then switch to **Agent**.
3. Ensure **Crew Mode is ON** (Exercise 6 defaults this automatically outside instructor mode).
4. Run one sample query and capture a baseline multi-agent trajectory from metadata.
	- In the response's **Agent Execution** block, capture: `Trajectory` (steps/tools/handoffs/redundant), `Tools Called`, and `Trace` (if shown).
	- Record this as your baseline row for that query.
5. In Phoenix, inspect the baseline run as an agent graph. Confirm you can see the flow between **Triage Agent**, **RAG Specialist**, and **Validator Agent**.
6. Run the handoff-corruption scenario: `simulate handoff corruption for retrieval query about 2024 regression failures`.
7. Compare baseline vs corrupted run for: handoff count, retrieval quality, and redundant tool calls.
8. In Phoenix, click into the hand-off between **Triage Agent** and **RAG Specialist** and compare the original query with the routed query.
9. For each run, record Actual Steps, Optimal Steps, and one handoff quality note.
10. Calculate Efficiency Score = Optimal Steps / Actual Steps.
11. As a team, propose one fix for handoff integrity and one guardrail for loop control.
12. As a control, run the same corruption prompt once with **Crew Mode OFF** and note that the handoff mutation should not appear in the single-agent path.

## Sample queries
1. Compare two test strategies for a GenAI support bot and recommend one.
2. Create a release test plan with risks, gates, and rollback criteria.
3. Summarize noisy bug reports into top root causes and priorities.
4. Design fairness tests for a multilingual assistant.
5. Write a production readiness memo using retrieval, groundedness, and latency findings.
6. simulate handoff corruption for retrieval query about 2024 regression failures.

## Team debrief questions
1. What caused the worst inefficiency: loop, bad handoff, or over-delegation?
2. Where exactly was input corrupted in the handoff chain?
3. What orchestrator rule or schema check would prevent this next time?

