# Exercise 6: Test Multi-Agent Trajectories

## Prerequisites
1. GenAI testing assistant is started locally (`python run.py`).
2. Ability to capture trace/trajectory evidence.
3. GitHub Copilot Chat available in Codespaces.
4. Agent mode enabled in the UI.

## Scenario
You are auditing how a multi-agent crew works together. The key question is whether the workflow is efficient and whether handoffs preserve intent.

## Student tasks
1. Open: `http://localhost:5000/?exercise=6`.
2. In the input bar, switch from **Ask** to **Agent** if the UI is not already in agent mode.
3. Run one sample query from the section below in Agent mode and capture a **baseline single-agent trajectory** from the response metadata.
	- In the response's **Agent Execution** block, capture: `Trajectory` (steps/tools/handoffs/redundant), `Tools Called`, and `Trace` (if shown).
	- Record this as your baseline row for that query.
4. To force **multi-agent crew mode** in Exercise 6, open instructor view: `http://localhost:5000/?exercise=6&instructor=1`.
5. In instructor controls, enable **Agent Mode**, **Show Trace**, and **Crew Mode**.
6. Re-run the **same query** in crew mode and compare crew trajectory efficiency against your baseline single-agent run.
	- Capture the same fields (`Trajectory`, `Tools Called`, `Trace`, `Handoffs`) and record a second row for the same query.
	- Compare baseline vs crew for Actual Steps, handoff quality, and redundant actions.
7. Each person runs 1 unique complex query and captures one trajectory.
8. For each run (baseline and crew), record Actual Steps, Optimal Steps, and one handoff quality note.
9. Calculate Efficiency Score = Optimal Steps / Actual Steps.
10. As a team, pick the single worst loop and propose one orchestrator prompt fix.

## Sample queries
1. Compare two test strategies for a GenAI support bot and recommend one.
2. Create a release test plan with risks, gates, and rollback criteria.
3. Summarize noisy bug reports into top root causes and priorities.
4. Design fairness tests for a multilingual assistant.
5. Write a production readiness memo using retrieval, groundedness, and latency findings.

## Team debrief questions
1. What caused the worst inefficiency: loop, bad handoff, or over-delegation?
2. Which step should have been skipped?
3. What orchestrator rule would prevent this next time?

