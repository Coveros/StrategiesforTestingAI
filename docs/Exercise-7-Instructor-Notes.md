# Exercise 7: Testing Non-Functional Requirements in the Agentic Chatbot - Instructor Notes

---

## Objective

Students should validate system-level resilience in the agentic chatbot under adverse conditions.

Focus areas:

1. Dependency failure handling
2. Circuit breaker behavior
3. Timeout and rate-limit resilience
4. Boundary input robustness
5. Latency and cost-risk proxies

---

## Setup Checklist

1. Launch app and verify [http://localhost:5000](http://localhost:5000) is reachable.
2. Open [http://localhost:5000/?instructor=1](http://localhost:5000/?instructor=1).
3. Enable Agent Mode, Show Trace, Crew Mode.
4. Confirm special NFR prompts work:
   - "run quick regression simulate dependency outage"
   - "run quick regression simulate tool timeout"
   - "run quick regression simulate rate limit"
   - "reset circuit breaker"
5. Optional standardized submission path: `python section7_nfr_quickrun.py` (generates JSON + TXT artifacts in `regression_test_results`).

---

## Timing (50-60 minutes)

| Phase | Time | Outcome |
|-|-|-|
| Intro to NFR framing | 5 minutes | Students align on resilience vs correctness |
| Part A dependency + breaker | 15 minutes | Outage and breaker behavior observed |
| Part B timeout + rate limit | 10-12 minutes | Unhappy path handling assessed |
| Part C boundary cases | 12-15 minutes | Robustness under weird inputs validated |
| Part D latency/loop-tax | 10 minutes | Simple cost-risk proxy calculated |
| Debrief | 5 minutes | Hardening priorities discussed |

---

## Expected Findings

### Dependency and circuit behavior

Students should observe:

1. Graceful degraded responses for simulated outages.
2. Circuit breaker opens after repeated failures.
3. Dependency calls blocked while breaker is open.
4. "reset circuit breaker" restores normal behavior.

### Timeout and 429 handling

Students should observe:

1. Timeout path returns fallback response (no crash).
2. 429 path reports backpressure behavior.
3. User communication remains explicit and understandable.

### Boundary robustness

Students should observe:

1. Empty and gibberish inputs do not crash the app.
2. Very long inputs may be slower but should remain stable.
3. Unexpected/unsafe tool execution should not occur on noise input.

### Latency and cost-risk proxy

Students should observe:

1. Response-time spread across scenarios.
2. Higher trajectory complexity can increase perceived cost risk.
3. Redundant tool calls act as a practical loop-tax indicator.

---

## Rubric (0-2 per dimension)

### 1) Failure-Path Validation (0-2)

- 0: Incomplete tests; little evidence
- 1: Partial tests; some evidence
- 2: Complete failure-path checks with clear outcomes

### 2) Circuit Breaker Reasoning (0-2)

- 0: No clear breaker analysis
- 1: Breaker behavior observed but weak interpretation
- 2: Correct interpretation of open/block/reset cycle

### 3) Boundary and Stability Analysis (0-2)

- 0: Minimal boundary testing
- 1: Boundary tests run with shallow analysis
- 2: Boundary cases analyzed with meaningful pass/fail criteria

### 4) Hardening Recommendations (0-2)

- 0: Generic recommendations
- 1: Some actionable ideas
- 2: Prioritized, concrete mitigations tied to evidence

---

## Strong Mitigations to Reward

1. Retry policy with capped exponential backoff
2. Circuit breaker cooldown telemetry and alerting
3. Per-tool timeout contracts and fallback paths
4. Input guardrails and early validation gates
5. Queue/backpressure strategy for 429 bursts
6. NFR regression checks in CI with scenario sampling

---

## Common Misconceptions to Correct

1. "If answer text is okay, reliability is okay."
   - Correction: Resilience is independent of answer fluency.

2. "Circuit breakers are optional in AI apps."
   - Correction: Dependency-heavy agent workflows need blast-radius control.

3. "Average latency is enough."
   - Correction: Tail latency and failure spikes drive user experience.

---

## Debrief (5 minutes)

Ask each team:

1. "What failed first under stress?"
2. "Did the system degrade gracefully or silently?"
3. "What one reliability control should be added before production?"

Map answers to controls:

- dependency instability -> retries + breaker policy
- noisy inputs -> validation and refusal defaults
- latency spikes -> timeout and queue controls
- loop-cost risk -> trajectory caps and redundancy suppression

---

## Submission Standardization (Recommended)

If students are on isolated VMs, request these two artifacts from each student/team:

1. `section7_quickrun_*.json`
2. `section7_quickrun_summary_*.txt`

These provide consistent evidence for pass/fail and reduce grading variability across environments.

---

## Bridge to Next Section

Suggested transition:

"You can now test agentic reliability manually. Next, we automate this into non-functional regression suites so resilience regressions are caught before release."

