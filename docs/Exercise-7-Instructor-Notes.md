# Exercise 7: Lab - Stress Testing / NFRs - Instructor Notes

---

## Overview

Students validate the assistant's behavior under **non-functional stress**, not just correctness. This lab is about operational reliability: how the system behaves when dependencies fail, tools slow down, inputs get extreme, or latency and cost drift upward.

**Key Learning Objective:** Students should learn to evaluate the assistant across five NFR pillars:

1. Outage / Rate Limits
2. Timeouts
3. Boundary Inputs
4. Gibberish / Fuzzing
5. Cost / Latency

This is a distributed chaos-engineering lab. Each student owns one NFR area, then the table merges results into a shared **Resilience Scorecard**.

---

## Setup Checklist (10 minutes before class)

- [ ] Confirm students can access traces, latency metrics, and token-cost metadata if available
- [ ] Confirm there is a practical way to simulate or approximate 429s, timeouts, and long-input cases
- [ ] Explain the five NFR pillars before the exercise begins
- [ ] Ensure each table can assign one person per pillar if possible
- [ ] Remind students that the goal is not just to break the assistant, but to evaluate whether it fails **gracefully**
- [ ] Have the student-facing lab open: [docs/Exercise-7.md](Exercise-7.md)

---

## Timing

| Phase | Time | Notes |
|---|---|---|
| Intro and NFR framing | 5 minutes | Shift from correctness QA to resilience QA |
| Part 1: Chaos assignments | 18-22 minutes | Each person runs one deliberate stress case for one NFR area |
| Part 2: Resilience scorecard | 12-15 minutes | Table combines findings and picks weakest link |
| Debrief | 5 minutes | Discuss which NFR is riskiest for production |
| **Total** | **40-50 minutes** | - |

---

## Time-box Guidance

- Cap the lab at one strong stress case per pillar.
- Reduce Person 5 to 3 baseline queries instead of 5.
- If discussion drifts, require pass/fail/mixed plus one severity note instead of a long debate for every row.

---

## Expected Findings by NFR Area

### Person 1: Outage / Rate Limits

Common failure patterns:

- Assistant does not communicate 429-style backpressure clearly
- System retries poorly or repeatedly without helping the user
- Partial failure leaves the system in a confusing state

What strong evidence looks like:

- Clear example of graceful degradation or lack of it
- Proof of whether the assistant remained usable after the rate-limit event

### Person 2: Timeouts

Common failure patterns:

- Assistant waits too long with no useful feedback
- No circuit-breaker-like behavior or timeout containment
- User receives a vague or misleading answer after a slow failure

What strong evidence looks like:

- Measured or observed delay behavior
- Clear judgment on whether the timeout path was safe and understandable

### Person 3: Boundary Inputs

Common failure patterns:

- Extremely large text causes crashes or broken formatting
- Context handling fails silently under long input
- Large input causes unstable or confusing assistant behavior

What strong evidence looks like:

- A concrete long-input example and the resulting behavior
- Clear distinction between safe truncation and outright failure

### Person 4: Gibberish / Fuzzing

Common failure patterns:

- Assistant hallucinates structured meaning from nonsense input
- Unexpected tool usage is triggered by noise
- Non-English or malformed input causes instability instead of controlled fallback

What strong evidence looks like:

- Example input and proof of whether the system stayed stable
- Judgment on whether fallback or clarification behavior was appropriate

### Person 5: Cost / Latency

Common failure patterns:

- TTFT varies wildly across normal baseline queries
- Similar requests have disproportionate token cost
- One or two runs reveal clear cost/latency spikes

What strong evidence looks like:

- Five baseline runs with average TTFT and average Token Cost
- Identification of worst-case latency or cost outlier

---

## Facilitation Tips

### While Students Run Stress Cases

Keep them focused on NFR behavior, not just correctness:

- "Did the system fail safely or unsafely?"
- "Was the user told clearly what happened?"
- "Did the system degrade, or did it just behave strangely?"
- "Would this be acceptable if it happened in production every day?"

### While Person 5 Measures Cost / Latency

Push for concrete metrics:

- "What is your average TTFT?"
- "Which run was the worst outlier?"
- "Would you call this stable or noisy? Why?"

### During the Resilience Scorecard Discussion

Keep the table from naming everything as equally bad:

- Require one weakest-link choice
- Ask for severity reasoning, not just pass/fail
- Require one recommended fix per NFR area

---

## Rubric (0-2 per dimension)

### NFR Test Quality (0-2)

- **0:** Stress cases are vague, weak, or incomplete
- **1:** Stress cases are usable but evidence is limited
- **2:** Stress cases are concrete and clearly tied to one NFR pillar

### Evidence and Analysis Quality (0-2)

- **0:** Claims unsupported by evidence
- **1:** Some evidence captured, but interpretation is shallow
- **2:** Strong evidence showing how the system behaved under stress

### Resilience Scorecard Quality (0-2)

- **0:** No clear combined scorecard
- **1:** Scorecard present but weakly justified
- **2:** Scorecard clearly summarizes pass/fail, severity, evidence, and fixes

### Weakest-Link Reasoning (0-2)

- **0:** No clear weakest-link decision
- **1:** Weakest link chosen but poorly justified
- **2:** Weakest link selected with evidence-based production reasoning

**Total: 8 points**

---

## Strong Mitigations to Reward

If students propose these, reward strongly:

1. Rate-limit backoff and user-visible degraded mode messaging
2. Per-tool timeout limits and circuit-breaker style recovery behavior
3. Input-size guardrails and truncation policies
4. Early validation for gibberish, malformed, or unsupported inputs
5. Cost and latency telemetry with alert thresholds
6. Automated resilience regressions for baseline TTFT and failure behavior

---

## Transition and Bridge Language

### Opening (Connect to Exercise 6)

"In Exercise 6, you audited whether a multi-agent crew worked efficiently. In this lab, we ask a different question: when the environment gets hostile or expensive, does the assistant stay reliable?"

### Mid-Lab Framing

"A system can be logically correct and still operationally weak. Your job is to find where reliability breaks first under stress."

### Closing (to next stage)

"You just stress-tested the assistant's non-functional behavior. The next step is to automate these resilience checks so failures in cost, latency, and recovery are caught before release."

---

## Common Student Mistakes and Corrections

| Mistake | What You Hear | Correction |
|---|---|---|
| Focuses only on answer quality | "The response was still correct" | "Correctness is not enough if the system is unstable or too expensive." |
| Treats slowdown as acceptable by default | "It was slow, but it finished" | "Production users care about timeouts, TTFT, and responsiveness." |
| Confuses weird output with graceful degradation | "It kind of worked" | "Did it fail clearly and safely, or just behave unpredictably?" |
| Ignores outliers in Person 5 data | "The average looked okay" | "A single severe latency or cost spike can still be the real risk." |
| Picks weakest link by opinion | "I think fuzzing was worst" | "What evidence makes it worse than the other NFR areas?" |

---

## Answers to Anticipated Questions

**Q: What if we cannot trigger a true 429 or timeout in class?**  
A: Use the closest available simulation or approximation. The key is to observe recovery behavior and user communication under stress.

**Q: Does Person 5 need exactly five baseline queries?**  
A: Yes, if possible. Five runs give enough data for simple averages and outlier discussion without taking too long.

**Q: What if more than one NFR looks bad?**  
A: That is expected. The table must still choose one weakest link based on severity, blast radius, and confidence in the evidence.

**Q: Should students fix the app during this lab?**  
A: Not required. The main goal is diagnosis quality, prioritization, and resilience reasoning.

---

## Debrief (5-10 minutes)

Ask the room:

1. Which NFR was the weakest link today?
2. Did the assistant fail gracefully, noisily, or silently under stress?
3. What one reliability control would you ship before production?

Map answers back to controls:

- rate limits -> backoff, queueing, degraded-mode messaging
- timeouts -> timeout policies, circuit breakers, fallback responses
- boundary inputs -> size limits, truncation, validation
- fuzzing stability -> input guards, fallback clarification behavior
- cost/latency -> telemetry, thresholds, regression alerts

---

## Optional Deep Dive

If a group finishes early:

1. Ask them to define a target SLO for TTFT
2. Ask them to design one automated chaos test for their weakest-link NFR
3. Ask them to rank all five NFRs by production blast radius

