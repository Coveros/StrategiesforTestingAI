# Exercise 6: Test Multi-Agent Trajectories

## Prerequisites
1. Agent mode enabled in the UI.
2. Ability to capture trace/trajectory evidence.
3. Team of up to 5 people.
4. Access to precomputed trajectory traces if needed.

## How to run this in the UI
1. Start the app: `python run.py`.
2. Open: `http://localhost:5000/?exercise=6`.
3. In the input bar, switch from **Ask** to **Agent**.
4. Run one sample query and capture trajectory evidence from the response metadata (agent mode + trace).
5. To force **multi-agent crew mode** in Exercise 6, open instructor view: `http://localhost:5000/?exercise=6&instructor=1`.
6. In instructor controls, enable **Agent Mode**, **Show Trace**, and **Crew Mode**.
7. Re-run the same query and compare single-agent vs crew trajectory efficiency.

## Scenario
You are auditing how a multi-agent crew works together. The key question is whether the workflow is efficient and whether handoffs preserve intent.

## Student tasks
1. Each person runs 1 unique complex query and captures one trajectory.
2. For each run, record Actual Steps, Optimal Steps, and one handoff quality note.
3. Calculate Efficiency Score = Optimal Steps / Actual Steps.
4. As a team, pick the single worst loop and propose one orchestrator prompt fix.

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

