# Exercise 7: Lab - Stress Testing / NFRs

**Estimated Duration:** 40-50 minutes  
**Prerequisites:** Exercises 5 and 6 completed; access to the assistant with traces, latency, and operational metadata visible  
**Deliverable:** A table-wide Resilience Scorecard identifying the weakest non-functional requirement

---

## Overview

This lab shifts from workflow correctness to **non-functional reliability**. Your job is to validate how well the assistant behaves under failure, overload, malformed inputs, and operational cost pressure.

You are not asking only, "Did it answer correctly?" You are asking:

- Does it degrade gracefully?
- Does it stay stable under stress?
- Does it avoid blowing up latency or token cost?
- Which non-functional requirement is the weakest link?

---

## Scenario: Reliability and Operational Cost

You are the QA team validating the assistant's **reliability under failure** and its **operational cost profile**.

In this lab, each person stress tests one specific **Non-Functional Requirement (NFR)**. After individual testing, the table combines results into one shared **Resilience Scorecard**.

---

## Group Setup

- **Table Exercise:** Each person owns one NFR pillar.
- **Chaos Engineering Assignments:** Each person runs the stress cases for their assigned area.
- **Resilience Scorecard:** The table combines findings and decides which NFR is the weakest link.

Precomputed Section 7 artifacts for this lab are available at:

- `artifacts/precomputed/section7/section7_quickrun_*.json`
- `artifacts/precomputed/section7/section7_quickrun_*.txt`

Regenerate snapshots with:

```bash
python prepare_exercise_artifacts.py
```

---

## Key Concepts

### What Is an NFR in This Lab?

You are testing system qualities that matter in production, even when the assistant is logically correct:

1. Reliability under dependency failure
2. Timeout tolerance and recovery behavior
3. Stability under extreme or malformed input
4. Robustness under fuzzed or nonsensical data
5. Latency and token-cost efficiency

### Failure Under Stress Is a Product Problem

A system may still be unsafe or production-unready if it:

- crashes on large inputs
- hangs on slow tools
- misbehaves during rate limits
- becomes unstable on garbage input
- consumes excessive latency or tokens for ordinary requests

### Resilience Scorecard

At the end of the lab, the table creates one shared scorecard summarizing:

- what failed
- how severe the weakness is
- what should be fixed first

---

## Part 1: Chaos Engineering Assignments

Each person at the table takes one specific NFR pillar to stress test. In the timed version, run one deliberate stress case per pillar.

### Person 1: Outage / Rate Limits

**Goal:** Simulate API 429 errors and check for graceful degradation.

Look for:

- clear rate-limit communication
- retry/backoff behavior
- no crash or broken state after the failure

### Person 2: Timeouts

**Goal:** Simulate slow tool responses and check for circuit breaker or timeout behavior.

Look for:

- fail-fast behavior or safe fallback
- no endless waiting loop
- clear user communication about timeout or degraded mode

### Person 3: Boundary Inputs

**Goal:** Input massive text blocks and check for context window crashes or instability.

Look for:

- truncation or safe handling of very large input
- no app crash or broken rendering
- reasonable response instead of uncontrolled failure

### Person 4: Gibberish / Fuzzing

**Goal:** Input nonsensical or non-English data and check for stability.

Look for:

- no hallucinated tool usage
- no system crash
- safe clarification or controlled fallback behavior

### Person 5: Cost / Latency

**Goal:** Run **3 baseline queries** and calculate the average **TTFT** and **Token Cost**.

Look for:

- whether baseline latency is acceptable
- whether token use is stable across similar queries
- whether any run looks unusually expensive

### Individual NFR Test Table

| Person | NFR Pillar | Stress Case / Query | Expected Behavior | Actual Behavior | Evidence | Pass/Fail |
|---|---|---|---|---|---|---|
| Person 1 | Outage/Rate Limits |  |  |  |  |  |
| Person 2 | Timeouts |  |  |  |  |  |
| Person 3 | Boundary Inputs |  |  |  |  |  |
| Person 4 | Gibberish/Fuzzing |  |  |  |  |  |
| Person 5 | Cost/Latency | Query 1 |  |  |  |  |
| Person 5 | Cost/Latency | Query 2 |  |  |  |  |
| Person 5 | Cost/Latency | Query 3 |  |  |  |  |

For Person 5, compute:

- **Average TTFT**
- **Average Token Cost**
- **Highest TTFT observed**
- **Highest Token Cost observed**

---

## Part 2: The Resilience Scorecard

Combine your findings into one table-wide **Resilience Scorecard**.

For each NFR, discuss:

1. Did the system remain usable?
2. Did it degrade gracefully?
3. Was the user informed clearly?
4. How severe would this weakness be in production?

### Resilience Scorecard Template

| NFR Area | Owner | Pass / Fail / Mixed | Severity | Evidence Summary | Recommended Fix |
|---|---|---|---|---|---|
| Outage / Rate Limits | Person 1 |  |  |  |  |
| Timeouts | Person 2 |  |  |  |  |
| Boundary Inputs | Person 3 |  |  |  |  |
| Gibberish / Fuzzing | Person 4 |  |  |  |  |
| Cost / Latency | Person 5 |  |  |  |  |

### Final Group Question

Which NFR is the **weakest link** right now, and why?

Your group must choose one.

---

## Deliverables

Submit one file named `exercise7_submission.md` containing:

1. Individual NFR findings for all five pillars
2. Person 5's TTFT and Token Cost calculations from 3 baseline queries
3. The completed Resilience Scorecard
4. The table's chosen weakest-link NFR
5. One recommended fix for each NFR area

---

## Reflection Questions

1. Which NFR produced the highest production risk?
2. Did the assistant fail safely, fail noisily, or fail silently?
3. Was the weakest link caused more by poor recovery behavior or poor operational limits?
4. If you could automate one resilience check first, which would you choose and why?

---

## Optional Stretch

If your table finishes early:

1. Design one extra adversarial stress case for each NFR pillar.
2. Define a target threshold for acceptable TTFT.
3. Draft one automated resilience regression check you would add to CI.

---

## Key Takeaway

Stress testing is about operational trust, not just answer quality.

A resilient assistant must degrade gracefully, remain stable under bad inputs and failures, and keep latency and cost within acceptable bounds.
