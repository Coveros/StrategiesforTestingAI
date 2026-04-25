# Exercise 7: Stress Test the Assistant (NFRs)

## Prerequisites
1. App running locally (`python run.py`).
2. Copilot Chat in Codespaces.
3. Ability to view tool calls or traces using Agent Mode in the UI.
4. Instructor mode enabled to force trace visibility and crew mode when needed.

## Scenario
You are testing reliability, not just correctness. The goal is to find the weakest non-functional area under stress and compare single-agent vs crew resilience under the same prompts.

## Student tasks
1. Open `http://localhost:5000/?exercise=7&instructor=1`.
2. In instructor controls, enable **Agent Mode** and **Show Trace**.
3. For each role prompt, run two passes in the same session:
	- Pass A: **Crew Mode OFF** (single-agent baseline)
	- Pass B: **Crew Mode ON** (multi-agent crew)
4. Split 5 roles:
	- Rate Limits
	- Timeouts
	- Boundary Inputs
	- Gibberish/Fuzzing
	- Latency Stability
5. For each role test, send the exact simulation prompt listed below and capture evidence from response metadata for both passes.
6. Each person runs 1 stress test (Person 5 runs 3 baseline queries), then repeats the same test with Crew Mode ON.
7. Record Pass/Fail/Mixed for single-agent and crew with one evidence note per mode.
8. Choose the weakest link and propose one fix.

## Simulation prompts by role (copy/paste)

### Rate Limits
1. `run quick regression simulate rate limit`
2. Run it twice in the same session and check if degraded mode/circuit behavior appears.

### Timeouts
1. `run quick regression simulate tool timeout`
2. Check whether the response degrades safely instead of failing silently.

### Boundary Inputs
1. Paste a very long prompt (for example, a repeated paragraph 20-30 times) and ask: `Summarize in 5 bullets.`
2. Verify the system still returns a safe, bounded response.

### Gibberish/Fuzzing
1. `xqz@@##123###?? en espanol ??? ###`
2. Verify the assistant handles malformed input gracefully (no crash, no unsafe action).

### Latency Stability
1. Run these 3 baseline prompts in the same session:
	- `run quick regression suite`
	- `run quick regression suite retrieval`
	- `run quick regression suite smoke`
2. Compare response time consistency across the three runs.

## What to capture as evidence
For each role and for each mode (single-agent and crew), capture:
1. Prompt used
2. Response summary
3. `response_time`
4. `trajectory_metrics.degraded_mode`
5. `trajectory_metrics.circuit_open`
6. `trajectory_metrics.steps` and `trajectory_metrics.tool_calls`
7. `handoffs` count (if present) and whether handoffs helped or hurt resilience

Note: this UI currently surfaces response-time and trajectory metrics, not token-level billing fields.

## NFR scorecard
| NFR Area | Mode | Expected Behavior | Actual Behavior | Pass/Fail/Mixed | Evidence | Recommended Fix |
|---|---|---|---|---|---|---|
| Rate Limits | Single-agent |  |  |  |  |  |
| Rate Limits | Crew |  |  |  |  |  |
| Timeouts | Single-agent |  |  |  |  |  |
| Timeouts | Crew |  |  |  |  |  |
| Boundary Inputs | Single-agent |  |  |  |  |  |
| Boundary Inputs | Crew |  |  |  |  |  |
| Gibberish/Fuzzing | Single-agent |  |  |  |  |  |
| Gibberish/Fuzzing | Crew |  |  |  |  |  |
| Latency Stability | Single-agent |  |  |  |  |  |
| Latency Stability | Crew |  |  |  |  |  |

## Team debrief questions
1. Which failure mode is highest production risk?
2. Did the system fail safely or silently?
3. What resilience check should be automated first?

