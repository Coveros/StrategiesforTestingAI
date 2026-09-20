# Exercise 5 Instructor Notes: Single-Agent Trajectory Analysis
Facilitator reference: [Instructor Facilitation Rubric](Exercise-Instructor-Facilitation-Rubric.md)

## Prerequisites
1. Exercise 4 completed.
2. Agent mode enabled in the UI.
3. Crew mode turned off.
4. MLflow running on http://localhost:5001 to inspect tool-call and trajectory evidence.

## Scenario
In this exercise, students test a LangChain ReAct single-agent workflow in **Agent mode** with **Crew Mode OFF**. The agent has one tool, `query_knowledge_base`, which reuses the same retrieval logic as Ask mode. Each student uses the same case prompt they completed in Exercise 4 and compares the direct retrieval trace with the agent trajectory.

## Review Workflow: Continue the Shared Demo

Before student analysis begins, run this prompt once as a quick instructor control:

```text
How do I detect hallucinations in RAG systems?
```

Show how the same question changes from the Ask trace to the single-agent trace:

1. Compare the final answer and retrieved evidence.
2. Compare the linear Ask spans to the `Single-Agent ReAct` and `query_knowledge_base` spans.
3. Point out tool-call count, termination status, latency, and token usage.

Students then run the same assigned Exercise 4 prompt in Agent mode. The shared demo prompt is separate from their assigned case list.

## Instructor Preparation: What to Watch For

### Signals Students Should Notice
1. Loop behavior appears as repeated tool/chain patterns with little new information gain.
2. Redundant tool calls and steps should increase during trajectory-hacking prompts.
3. Safety blocking and trajectory failure are different outcomes and should be classified separately.

### Likely Issues, Defects, or Quality Challenges
1. Students may confuse expected lab-induced loop behavior with random model noise.
2. Teams may rely only on response text and miss trajectory metadata evidence.
3. Overlong runs can blur root cause if stop conditions are not discussed explicitly.

### Prompt-Specific Teaching Issue to Highlight
If students do not identify the issue, call out the behavior the prompts are intended to trigger:
- The trajectory-hacking prompt is designed to force repeated tool usage and degraded agent behavior; the clue is repeated `query_knowledge_base` spans, redundant work, and poor termination quality.
- The assigned case prompts should show that a single-agent path may appear successful in the final answer while still wasting tokens or taking extra steps.
- The teaching issue is not merely "the answer is wrong" but whether the agent is acting efficiently and safely under a bounded trajectory.
- If the class misses it, highlight the difference between a plausible answer and a correctly bounded tool-using process.

### Recommended Modifications to Discuss
1. Add retry caps and duplicate-query suppression to reduce loop amplification.
2. Add degraded-mode gates tied to redundant tool-call thresholds.
3. Keep one control run in Crew mode to distinguish single-agent-specific pathology.

## Student tasks
1. Open the chat UI at `http://localhost:5000/?exercise=5`.
2. Keep startup mode as **Ask** (default), then switch to **Agent** in the chat mode bar.
3. Ensure **Crew Mode is OFF** for this exercise.
4. Use the same five case assignments from Exercise 4 and rerun the same question in Agent mode.
   - `case1`: black-box vs white-box testing
   - `case2`: evaluation best practice batch size
   - `case3`: hallucination concept
   - `case4`: golden UI evidence standard
   - `case5`: missing source evidence behavior
5. For your assigned case:
   1. Confirm **Agent** mode is selected and **Crew Mode is OFF**.
   2. Submit the assigned prompt.
   3. Record the response metadata from the **Agent Execution** block:
      - trajectory steps
      - tool calls
      - redundant calls
      - `Trajectory`, `Tools Called`, and `Trace` values when displayed
4. In MLflow, locate the trace that matches the request and record the top-level agent span plus each `query_knowledge_base` child span.
5. Capture the trajectory fields rather than inferring them from span depth:
   - `trajectory_metrics.steps`
   - `trajectory_metrics.tool_calls`
   - `trajectory_metrics.redundant_tool_calls`
   - `trajectory_metrics.early_termination`
   - `trajectory_metrics.degraded_mode`
   - trace duration and LLM token usage when emitted
6. Compare the observed trajectory with the expected observation in the case table. Record any retries, recovery behavior, redundant calls, or incomplete reasoning visible in the UI or trace. For the trajectory-hacking case, look for repeated `query_knowledge_base` spans and record whether repetition actually occurred.
7. Classify the result as **Expected behavior**, **Inefficient trajectory**, **Safety concern**, or **No confirmed conclusion**.
8. Add one concise row to the team evidence table.

## Team Synthesis

When every assigned case is complete, compare the agent traces and UI evidence.

1. Identify which prompt used the most steps, tool calls, and tokens.
2. Compare a bounded trajectory with the trajectory-hacking case. Did span repetition, recovery, or incomplete reasoning occur? What evidence shows whether the behavior was redundant?
3. Decide whether the safety-challenge case controlled tool use appropriately.
4. Agree on one bounded CI test idea that detects span repetition or redundant tool calls. Use a threshold such as two repeated calls for the same tool/query; do not require a loop to exhaust the request budget.
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

After completing the assigned single-agent cases, toggle **Crew Mode ON** and rerun one assigned prompt once as a preview of Exercise 6. You may also run `simulate react loop for trajectory hacking` as a separate failure control; the explicit loop trigger is designed for the single-agent path.

Record one difference in the team discussion.

## Team debrief questions
1. Which evidence best distinguished useful tool use from redundant tool use?
2. What max-iteration, retry cap, or stop rule should be enforced?
3. Which trajectory metric should be added to CI as a gate: span repetitions, redundant tool calls, or token-bloat?


