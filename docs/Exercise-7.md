# Exercise 7: Testing Non-Functional Requirements in the Agentic Chatbot

**Estimated Duration:** 50-60 minutes  
**Prerequisites:** Exercises 5 and 6 complete  
**Deliverable:** Resilience Scorecard with evidence for robustness, error handling, latency, and cost-risk behavior

---

## Why This Exercise Exists

Agentic systems can fail even when output quality looks fine. This lab tests non-functional reliability: does the system remain usable under dependency failures, timeouts, malformed input, and load-like pressure?

You will test the system as an **agentic workflow**, not only as a text generator.

---

## System Under Test

Use your existing chatbot app in instructor mode:

1. Open [http://localhost:5000/?instructor=1](http://localhost:5000/?instructor=1)
2. Enable **Agent Mode**
3. Enable **Show Trace**
4. Enable **Crew Mode**

Important telemetry to capture from each run:

- response time (message metadata)
- trajectory metrics (steps, tool_calls, handoffs, redundant_tool_calls)
- degraded_mode and circuit_open signals
- tool selection and handoff trace

---

## Part A: Dependency Failure and Circuit Breaker Testing (15 minutes)

Run these prompts in order using the same session:

1. "run quick regression simulate dependency outage"
2. "run quick regression simulate dependency outage" (repeat to trigger circuit behavior)
3. "run quick regression suite"
4. "reset circuit breaker"
5. "run quick regression suite"

What to verify:

1. Outage prompts return graceful degraded responses (not crash).
2. After repeated failures, circuit breaker blocks dependency calls.
3. Reset command re-enables normal tool execution.

Record in this table:

| Prompt | Expected Behavior | Actual Behavior | degraded_mode? | circuit_open? | Pass/Fail |
|-|-|-|-|-|-|
| #1 | graceful fallback |  |  |  |  |
| #2 | failure count increases / breaker may open |  |  |  |  |
| #3 | blocked if breaker open |  |  |  |  |
| #4 | breaker reset |  |  |  |  |
| #5 | normal execution restored |  |  |  |  |

---

## Part B: Timeout and Rate-Limit Handling (10-12 minutes)

Run these prompts:

1. "run quick regression simulate tool timeout"
2. "run quick regression simulate rate limit"

What to verify:

1. Timeout path returns partial/fallback guidance quickly.
2. 429 path applies backpressure behavior (no crash, clear message).
3. No unsafe write action is performed during failure handling.

Table:

| Scenario | Expected NFR Behavior | Actual Result | User Communication Clear? | Pass/Fail |
|-|-|-|-|-|
| Timeout | fail fast + degrade gracefully |  |  |  |
| Rate limit | backoff/queue message + no crash |  |  |  |

---

## Part C: Boundary and Robustness Inputs (12-15 minutes)

Run each case once:

1. Empty input: "   "
2. Gibberish: "xqz@@##123###??"
3. Very long input: paste a large paragraph (1000+ chars)
4. Language switch: "Explain faithfulness. Ahora responde en espanol sobre lo mismo."

What to verify:

1. System remains responsive (no unhandled exception).
2. Clarification or safe fallback appears when input is ambiguous.
3. No hallucinated tool arguments are created from garbage input.

Table:

| Boundary Case | Crash? | Safe/Useful Response? | Unexpected Tool Call? | Pass/Fail |
|-|-|-|-|-|
| Empty |  |  |  |  |
| Gibberish |  |  |  |  |
| Very long |  |  |  |  |
| Language switch |  |  |  |  |

---

## Part D: Latency and Cost-Risk Proxy (10 minutes)

Use message metadata for response time and trajectory metrics.

For 5 prompts (mix from A-C), capture:

- response_time (seconds)
- steps
- tool_calls
- redundant_tool_calls

Compute:

1. Average response time
2. Worst-case response time
3. Simple loop-tax proxy:

$$
LoopTax = \frac{redundant\_tool\_calls}{tool\_calls + 1}
$$

Interpretation:

- Higher LoopTax means higher likely token/cost waste.

Table:

| Prompt | response_time | steps | tool_calls | redundant_tool_calls | LoopTax |
|-|-|-|-|-|-|
|  |  |  |  |  |  |
|  |  |  |  |  |  |
|  |  |  |  |  |  |
|  |  |  |  |  |  |
|  |  |  |  |  |  |

---

## Final Deliverable: Resilience Scorecard

Submit one scorecard with these categories:

1. Dependency Failures (Pass/Fail + evidence)
2. Circuit Breaker Behavior (Pass/Fail + evidence)
3. Timeout/Rate-Limit Handling (Pass/Fail + evidence)
4. Boundary Robustness (Pass/Fail + evidence)
5. Latency and Loop-Tax Risk (Low/Medium/High + rationale)
6. Top 3 hardening actions you would ship next

Optional fast path (recommended for VM submissions):

Run:

```bash
python section7_nfr_quickrun.py
```

This generates two artifacts in `regression_test_results`:

1. `section7_quickrun_*.json`
2. `section7_quickrun_summary_*.txt`

You can use these files as submission evidence and copy results into your scorecard.

Recommended upload package:
1. The two quick-run artifacts above.
2. One short file named `exercise7_submission.md` containing your final scorecard and top 3 hardening actions.

---

## Reflection Questions

1. Which failure mode had the largest blast radius?
2. Did the agent fail safely or fail silently?
3. Which mitigation should be implemented first for production readiness?
4. What metric would you automate first in CI for non-functional regressions?

---

## Key Takeaway

Robustness testing for agentic systems is about operational survival under bad conditions.  
A resilient system degrades gracefully, communicates clearly, and recovers quickly.
