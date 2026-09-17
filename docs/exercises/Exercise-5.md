# Exercise 5: Single-Agent Trajectory Analysis

## Prerequisites
1. Exercise 4 completed.
2. Agent mode turned on. Crew mode turned off.
3. The MLflow tracking server is running at [http://localhost:5001](http://localhost:5001).

## Scenario

In this exercise, you test a LangChain ReAct single-agent workflow in **Agent
mode** with **Crew Mode OFF**. The agent has one tool, `query_knowledge_base`,
which reuses the retrieval logic from Ask mode.

Your team will continue the five case assignments from Exercise 4. Each person
will run the same assigned prompt in **Agent** mode that they previously ran in
Ask mode. This lets the team compare how the same question changes as the
system moves from direct retrieval to single-agent orchestration.

## Assign Cases

Form a team of three to five people and keep the same case assignments from
Exercise 4. For teams of three or four, complete only the first three or four
cases. Every person uses **Agent** mode with **Crew Mode OFF** and runs the
same assigned prompt once.

| Case ID | Scenario | Assigned prompt | Expected observation |
|---|---|---|---|
| case1 | Black-box and white-box testing | Use the same prompt assigned in Exercise 4. | Compare direct retrieval with a bounded agent trajectory. |
| case2 | Evaluation best practices | Use the same prompt assigned in Exercise 4. | Compare answer and tool evidence with Ask mode. |
| case3 | Hallucination concepts | Use the same prompt assigned in Exercise 4. | Compare grounding and termination evidence. |
| case4 | Golden UI evidence | Use the same prompt assigned in Exercise 4. | Compare orchestration overhead with Ask mode. |
| case5 | Missing source evidence | Use the same prompt assigned in Exercise 4. | Observe bounded handling of insufficient context. |

## Individual Agent Trace Analysis

For your assigned case:

1. Confirm **Agent** mode is selected and **Crew Mode is OFF**.
2. Submit your assigned prompt and record the response metadata from the
   **Agent Execution** block:
   - trajectory steps
   - tool calls
   - redundant calls
   - `Trajectory`, `Tools Called`, and `Trace` values when displayed
3. In MLflow, locate the trace that matches your request. Record the top-level
   agent span and each `query_knowledge_base` child span.
4. Capture the actual trajectory fields rather than inferring them from span
   depth:
   - `trajectory_metrics.steps`
   - `trajectory_metrics.tool_calls`
   - `trajectory_metrics.redundant_tool_calls`
   - `trajectory_metrics.early_termination`
   - `trajectory_metrics.degraded_mode`
   - trace duration and LLM token usage when emitted
5. Compare the observed trajectory with the expected observation in the case
   table. Record any retries, recovery behavior, redundant calls, or incomplete
   reasoning visible in the UI or trace. For the trajectory-hacking case, look
   for repeated `query_knowledge_base` spans and record whether repetition
   actually occurred.
6. Classify the result as **Expected behavior**, **Inefficient trajectory**,
   **Safety concern**, or **No confirmed conclusion**. Add one concise row to
   the team evidence table.

## Team Synthesis

When every assigned case is complete, compare the agent traces and UI evidence.

1. Identify which prompt used the most steps, tool calls, and tokens.
2. Compare a bounded trajectory with the trajectory-hacking case. Did span
   repetition, recovery, or incomplete reasoning occur? What evidence shows
   whether the behavior was redundant?
3. Decide whether the safety-challenge case controlled tool use appropriately.
4. Agree on one bounded CI test idea that detects span repetition or redundant
   tool calls. Use a threshold such as two repeated calls for the same
   tool/query; do not require a loop to exhaust the request budget.
5. Write one short, evidence-based bug report or improvement proposal:
   - Case ID
   - Title
   - Expected behavior
   - Actual behavior
   - UI and trace evidence
   - Classification
   - Recommended guardrail or fix

## Team Evidence Table

| Case ID | Analyst | Expected trajectory | Actual trajectory | UI/MLflow evidence | Classification |
|---|---|---|---|---|---|
| case1 |  |  |  |  |  |
| case2 |  |  |  |  |  |
| case3 |  |  |  |  |  |
| case4 |  |  |  |  |  |
| case5 |  |  |  |  |  |

## Optional Team Controls

After completing the assigned single-agent cases, toggle **Crew Mode ON** and
rerun one assigned prompt once as a preview of Exercise 6. You may also run
`simulate react loop for trajectory hacking` as a separate failure control; the
explicit loop trigger is designed for the single-agent path.
Record one difference in the team discussion.

## Team debrief questions
1. Which evidence best distinguished useful tool use from redundant tool use?
2. What max-iteration, retry cap, or stop rule should be enforced?
3. Which trajectory metric should be added to CI as a gate: span repetitions, redundant tool calls, or token-bloat?

