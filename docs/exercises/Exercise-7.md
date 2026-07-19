# Exercise 7: Reliability and Overhead (Ask vs Agent + Crew Handoff Focus)

## Prerequisites
1. Exercise 6 completed.
2. Use live traces from Phoenix during this exercise.
3. Ability to use Ask mode, Agent mode, and Crew Mode in the UI.
4. Optional automation runner available in your Codespace: `python section7_nfr_quickrun.py`.

## Scenario
You are testing non-functional behavior across the runtime patterns now used in this repo:

1. **Ask mode**: deterministic RAG pipeline.
2. **Single-agent mode**: one ReAct agent with the `query_knowledge_base` tool.
3. **Crew mode**: multi-agent orchestration primarily used here for handoff resilience checks.

The goal is to compare reliability, latency, and trajectory overhead primarily across Ask vs single-agent mode, then run a focused Crew handoff-resilience check.

## Student tasks
1. Open `http://localhost:5000/?exercise=7&instructor=1`.
2. In instructor controls, enable **Show Trace**.
3. Run the baseline factual query in Ask mode and Agent mode (Crew OFF):
   - Ask mode: `What are the key challenges in testing GenAI applications?`
   - Agent mode with **Crew Mode OFF**: same prompt
4. Run a Crew baseline once (**Crew Mode ON**) as supplemental context, not the primary comparison.
5. Split 5 roles:
   - Latency Overhead
   - Long-Input Stability
   - Malformed Input Handling
   - Single-Agent Loop Containment
   - Multi-Agent Handoff Resilience
6. For your assigned role, run the exact prompts below and capture evidence from response metadata and Phoenix.
7. Record Pass/Fail/Mixed with one evidence note per required mode.
8. As a team, identify the weakest NFR area and propose one fix with the smallest blast radius.

## Role prompts

### Latency Overhead
1. Run this prompt in Ask mode and Agent mode (Crew OFF):
   - `What are the key challenges in testing GenAI applications?`
2. Compare `response_time`, steps, and tool calls.
3. Optional Crew add-on: run once with **Crew ON** and note handoffs overhead separately.

### Long-Input Stability
1. Paste a long but valid prompt under the UI limit, for example a repeated paragraph asking for a 5-bullet summary of GenAI testing risks.
2. Run it in Ask mode and single-agent mode.
3. Optional Crew add-on: run once with Crew ON if time permits.
4. Verify the system stays bounded and returns a usable answer.

### Malformed Input Handling
1. Use this malformed prompt in Ask mode and single-agent mode:
   - `xqz@@##123###?? en espanol ??? ###`
2. Optional Crew add-on: run once with Crew ON.
3. Verify the system does not crash and still returns a bounded response.

### Single-Agent Loop Containment
1. In Agent mode with **Crew Mode OFF**, run:
   - `simulate react loop for trajectory hacking`
2. In Agent mode with **Crew Mode ON**, rerun the same prompt as a control.
3. Compare whether the loop pathology is isolated to the single-agent path.

### Multi-Agent Handoff Resilience
1. In Agent mode with **Crew Mode ON**, run:
   - `simulate handoff corruption for retrieval query about 2024 regression failures`
2. In Agent mode with **Crew Mode OFF**, rerun the same prompt as a control.
3. Compare whether handoff mutation is visible only in the multi-agent path.

## What to capture as evidence
For each run, capture:
1. Prompt used
2. Mode used (`ask`, `agent`, or `crew`)
3. Response summary
4. `response_time`
5. `trajectory_metrics.steps`
6. `trajectory_metrics.tool_calls`
7. `trajectory_metrics.redundant_tool_calls`
8. `trajectory_metrics.degraded_mode`
9. `trajectory_metrics.poisoned_retrieval`
10. `handoffs` count (if present)
11. One Phoenix observation from live traces (trace shape, span depth, or handoff graph)

## NFR scorecard
| NFR Area | Mode | Expected Behavior | Actual Behavior | Pass/Fail/Mixed | Evidence | Recommended Fix |
|---|---|---|---|---|---|---|
| Latency Overhead | Ask |  |  |  |  |  |
| Latency Overhead | Single-agent |  |  |  |  |  |
| Long-Input Stability | Ask |  |  |  |  |  |
| Long-Input Stability | Single-agent |  |  |  |  |  |
| Malformed Input Handling | Ask |  |  |  |  |  |
| Malformed Input Handling | Single-agent |  |  |  |  |  |
| Loop Containment | Single-agent |  |  |  |  |  |
| Loop Containment | Crew control |  |  |  |  |  |
| Handoff Resilience | Single-agent control |  |  |  |  |  |
| Handoff Resilience | Crew |  |  |  |  |  |
| Crew Overhead (Optional) | Crew baseline |  |  |  |  |  |

## Optional automation
Run:

```bash
python section7_nfr_quickrun.py
```

This generates JSON and TXT artifacts in `regression_test_results/` using the current supported prompts and mode comparisons.

## Team debrief questions
1. Which mode introduced the most overhead relative to the value it added?
2. Did the system fail safely, fail noisily, or silently degrade?
3. What one NFR check should be automated first in CI or smoke testing?

