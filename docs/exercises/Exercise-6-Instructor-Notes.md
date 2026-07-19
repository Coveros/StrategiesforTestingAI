# Exercise 6 Instructor Notes: Multi-Agent Handoff and Trajectory Analysis
Facilitator reference: [Instructor Facilitation Rubric](Exercise-Instructor-Facilitation-Rubric.md)

## Prerequisites
1. Exercise 5 completed.
2. Agent mode enabled in the UI.
3. Crew Mode enabled in the UI.
4. Ability to capture trace/trajectory evidence.

## Scenario
You are auditing a real multi-agent flow in LangChain with core roles **Triage Agent** and **RAG Specialist** (and an optional **Validator Agent** when enabled). The orchestrator routes work between specialist capabilities instead of forcing retrieval every time. Your goal is to study the hand-off graph in Phoenix and diagnose how corrupted state can break retrieval.

## Instructor Preparation: What to Watch For

### Signals Students Should Notice
1. Baseline crew runs should show coherent handoff purpose and routed-query continuity.
2. Corruption scenarios should surface changed routed-query state and retrieval degradation.
3. Crew OFF control runs should not exhibit multi-agent handoff mutation indicators.

### Likely Issues, Defects, or Quality Challenges
1. Students may treat shallow crew traces as failure instead of checking handoff fields.
2. Handoff quality may degrade without obvious user-facing text changes.
3. Over-delegation or unnecessary handoffs can increase overhead without quality gains.

### Recommended Modifications to Discuss
1. Enforce handoff schema checks (required fields and immutable original query reference).
2. Add integrity assertions comparing original and routed query for high-risk cases.
3. Add a handoff-efficiency guardrail (max handoffs or min utility per handoff).

## Student tasks
1. Open `http://localhost:5000/?exercise=6`.
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
6. In Phoenix, inspect the baseline run as an agent graph and confirm you can see the flow between **Triage Agent** and **RAG Specialist**. If Validator is enabled in your environment, include it in the observed flow.
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


