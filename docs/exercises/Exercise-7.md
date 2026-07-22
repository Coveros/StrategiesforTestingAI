# Exercise 7: Reliability and Overhead (Ask vs Agent + Crew Handoff Focus)

## Prerequisites
1. Exercise 6 completed.
2. Use live traces from Phoenix during this exercise.
3. Ability to use Ask mode, Agent mode, and Crew Mode in the UI.
4. Optional automation runner available in your Codespace: `python section7_nfr_quickrun.py`.

## Trace Reuse Optimization: No New Prompts Needed ⏱️

**You do not need to run new prompts for this exercise.** The 12 traces generated in Exercise 6 Part 1 (via `python generate_classroom_traces.py`) already capture Ask, Agent, and Crew modes with varying input characteristics:

- **5 traces (same_prompt)**: Identical input, test consistency and latency variation
- **4 traces (variation)**: Robustness tests with reworded questions
- **3 traces (different_prompt)**: Edge cases and diverse query types

These traces have already captured all NFR metadata: response latency, token counts, error status, tool calls, and handoff behavior.

**To proceed:**
1. Ensure Exercise 6 Part 1 has completed: `python generate_classroom_traces.py` (or verify `classroom_traces_results.json` exists)
2. Open Phoenix: http://localhost:6006 → **Traces tab**
3. Filter or search for traces with tags: `scenario: same_prompt` or `scenario: variation` or `scenario: different_prompt`
4. Proceed to "Student tasks" below

**Why reuse?** Saves ~6 minutes of inference time and focuses the exercise on *analysis* rather than data generation.

# Exercise 7: Reliability and NFR Testing

## Prerequisites
1. Exercise 6 completed (traces available in Phoenix)
2. Flask app running: `python run.py`
3. Phoenix running on http://localhost:6006

## Team Exercise - NFR Metrics Analysis (30 minutes)

### Overview
Using pre-generated traces from Exercise 6, analyze **two key non-functional requirements**:
1. **Latency & Token Overhead**: Does agent mode cost more than ask mode?
2. **Error Resilience**: How does the system handle malformed inputs?

### Role Assignments
- **Phoenix Queries**: Filters traces by mode (ask vs agent) and scenario
- **Metrics Collector**: Extracts latency, token counts, and error info
- **Evidence Scribe**: Records findings in results table
- **Proposer**: Suggests one efficiency improvement

### Activities (30 minutes)

#### Activity 1: Latency & Token Overhead (15 minutes)
1. **In Phoenix Traces tab**, find 2-3 traces from Exercise 6:
   - One "same_prompt" trace run in **Ask mode**
   - One "same_prompt" trace run in **Agent mode** (crew OFF)
   - Compare side-by-side
2. **Extract metrics from each trace:**
   - Response latency (total span duration)
   - Token count (prompt + completion combined)
   - Tool calls made
   - Any retry loops?
3. **Calculate overhead:**
   - Token overhead = (Agent tokens - Ask tokens) / Ask tokens × 100%
   - Latency overhead = (Agent latency - Ask latency) / Ask latency × 100%
4. **Record in table** (see below)

#### Activity 2: Error Resilience (10 minutes)
1. **Run these test prompts in the UI** (agent mode, crew OFF):
   - `What are the key challenges in testing GenAI applications?` (normal)
   - `xqz@@##123###?? en espanol ???` (malformed)
2. **For each, note:**
   - Did the system crash or return bounded response?
   - How many tool calls were attempted?
   - Did error handling kick in?
3. **In Phoenix**, inspect the error trace:
   - Find the error span (red indicator)
   - What was the error type? (malformed input, tool error, timeout?)
4. **Record pass/fail** in table

### Results Table

| Test | Mode | Latency (sec) | Tokens | Tool Calls | Status | Insight |
|---|---|---:|---:|---:|---|---|
| Same Prompt - Ask | Ask | | | | | |
| Same Prompt - Agent | Agent | | | | | |
| **Overhead** | | **+X%** | **+X%** | | | |
| Normal Prompt | Agent | | | | Pass/Fail | |
| Malformed Input | Agent | | | | Pass/Fail | [Error type] |

### Team Debrief (5 minutes)

1. **"Where does the biggest overhead come from?"** (Extra tokens? Tool calls? Handoffs?)
2. **"Does the system degrade gracefully on malformed input?"** (Bounded? Retry logic?)
3. **"If you could optimize one thing, what would it be?"** (Fewer tool calls? Determinism? Caching?)
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

