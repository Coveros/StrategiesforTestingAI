# Exercise 7: Stress Test the Assistant (NFRs)

## Prerequisites
1. App running locally (`python run.py`).
2. Team of up to 5 people.
3. Ability to use Agent mode in the UI.

## Scenario
You are testing reliability, not just correctness. The goal is to find the weakest non-functional area under stress.

## How to run this in the UI
1. Open `http://localhost:5000/?exercise=7`.
2. Switch from **Ask** to **Agent** in the input bar.
3. For NFR stress checks, use instructor controls so you can force trace/crew settings:
	- Open `http://localhost:5000/?exercise=7&instructor=1`
	- Enable **Agent Mode** and **Show Trace**
	- Optional: enable **Crew Mode** to compare single-agent vs multi-agent resilience
4. For each role test, send the exact simulation prompt listed below and capture evidence from response metadata.

## Student tasks
1. Split 5 roles:
	- Rate Limits
	- Timeouts
	- Boundary Inputs
	- Gibberish/Fuzzing
	- Latency Stability
2. Each person runs 1 stress test (Person 5 runs 3 baseline queries).
3. Record Pass/Fail/Mixed with one evidence note per role.
4. Choose the weakest link and propose one fix.

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
For each role, capture:
1. Prompt used
2. Response summary
3. `response_time`
4. `trajectory_metrics.degraded_mode`
5. `trajectory_metrics.circuit_open`
6. `trajectory_metrics.steps` and `trajectory_metrics.tool_calls`

Note: this UI currently surfaces response-time and trajectory metrics, not token-level billing fields.

## Optional automation path
If you prefer scripted simulation evidence, run:
- `python section7_nfr_quickrun.py`
This generates JSON/TXT artifacts in `regression_test_results/`.

## NFR scorecard
| NFR Area | Expected Behavior | Actual Behavior | Pass/Fail/Mixed | Evidence | Recommended Fix |
|---|---|---|---|---|---|
| Rate Limits |  |  |  |  |  |
| Timeouts |  |  |  |  |  |
| Boundary Inputs |  |  |  |  |  |
| Gibberish/Fuzzing |  |  |  |  |  |
| Latency Stability |  |  |  |  |  |

## Team debrief questions
1. Which failure mode is highest production risk?
2. Did the system fail safely or silently?
3. What resilience check should be automated first?

