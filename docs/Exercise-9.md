# Exercise 9: Lab - Automating the Test Run / MLOps

**Estimated Duration:** 35-45 minutes  
**Prerequisites:** Exercises 5-8 completed; access to the CI-style test suite and release artifacts in Codespaces  
**Deliverable:** An individual baseline-vs-candidate analysis plus a group Go/No-Go release decision and shift-right monitoring plan

---

## Overview

This final lab simulates the **Go/No-Go Release Meeting** for the assistant. Your job is to treat the assistant like a production system under release review: compare versions, analyze performance and quality trade-offs, and decide whether the candidate build should ship.

This is not just a test run. It is a release decision exercise.

---

## Scenario: The Release Advisory Board

The assistant has two versions available for evaluation:

1. **v1.0 (Baseline)**
2. **v2.0 (Candidate)**

Everyone on the table will review the provided CI results for these two versions and compare them.

You will capture:

- **Pass Rate**
- **Latency**

The goal is to see whether results are consistent across the group and whether the candidate is ready for release.

---

## Group Setup

- **Individual Analysis:** Everyone reviews the provided baseline-versus-candidate results on their own machine.
- **Release Advisory Board:** The table regroups and acts as the decision-making board.
- **Final Vote:** Every person must argue either **Ship** or **No-Ship**, then cast a vote.

Precomputed Section 9 release-gate artifacts are available at:

- `artifacts/precomputed/section9/section9_agentic_ci_*.json`
- `artifacts/precomputed/section9/section9_agentic_ci_*.txt`

Regenerate snapshots with:

```bash
python prepare_exercise_artifacts.py
```

---

## Key Concepts

### Why Compare Baseline vs Candidate?

A release decision should be based on evidence, not intuition.

The baseline gives you a known reference point. The candidate tells you what changed.

You are looking for trade-offs such as:

- faster but less accurate
- more accurate but slower
- safer but more expensive
- higher pass rate with worse operational latency

### CI Is Only the First Gate

Automated tests help decide whether a release is acceptable **before shipping**.

But even a shipped candidate still needs **Shift-Right monitoring** after release.

### Release Decisions Are Trade-Off Decisions

In this lab, the table must reason through a realistic conflict:

- **v2.0 is 30% faster**
- **v2.0 has a 2% lower Accuracy score**

The team must decide whether that trade-off is acceptable.

---

## Part 1: Individual Analysis

Each person reviews the CI output snapshot in their own Codespace and compares **v1.0 (Baseline)** vs **v2.0 (Candidate)**.

Record the following from the provided output:

- Pass Rate for v1.0
- Pass Rate for v2.0
- Latency for v1.0
- Latency for v2.0

### Individual Analysis Table

| Person | Baseline Pass Rate | Candidate Pass Rate | Baseline Latency | Candidate Latency | Notes |
|---|---|---|---|---|---|
| Person 1 |  |  |  |  |  |
| Person 2 |  |  |  |  |  |
| Person 3 |  |  |  |  |  |
| Person 4 |  |  |  |  |  |
| Person 5 |  |  |  |  |  |

### Questions to Answer Individually

1. Are your results consistent with other people at the table?
2. Is the latency improvement real and repeatable?
3. Is the accuracy drop small enough to tolerate?
4. Would you personally recommend Ship or No-Ship based on your own machine?

---

## Part 2: The Release Advisory Board (Group Decision)

Now regroup as the **Release Advisory Board**.

### The Conflict

Assume the group sees this result:

- **v2.0 is 30% faster**
- **v2.0 has a 2% lower Accuracy score**

### The Discussion

You have **5 minutes** to debate.

Every person must provide **one reason** to either:

- **Ship**
- **No-Ship**

### Board Deliberation Table

| Person | Position (Ship / No-Ship) | Reason |
|---|---|---|
| Person 1 |  |  |
| Person 2 |  |  |
| Person 3 |  |  |
| Person 4 |  |  |
| Person 5 |  |  |

### Final Vote

After the discussion, cast a final table vote.

| Final Outcome | Vote Count | Rationale |
|---|---|---|
| Ship |  |  |
| No-Ship |  |  |

Document the final decision and why the board chose it.

---

## Part 3: Shift-Right Monitoring Plan

Whether you choose Ship or No-Ship, define a production monitoring plan.

Your plan must include:

1. What to monitor after release
2. What thresholds would trigger concern
3. What you would do if v2.0 underperforms in production

### Shift-Right Monitoring Template

| Metric | Why It Matters | Threshold / Alert Rule | Action if Triggered |
|---|---|---|---|
| Accuracy trend |  |  |  |
| Latency / TTFT |  |  |  |
| User complaints / thumbs down |  |  |  |
| Safety failures |  |  |  |

Also define:

- **Rollback Rule:** When would you rollback v2.0?
- **Observation Window:** How long will you monitor closely after launch?

---

## Deliverables

Submit one file named `exercise9_submission.md` containing:

1. Your individual baseline vs candidate results
2. The board deliberation table
3. The final Ship / No-Ship vote and rationale
4. Your Shift-Right monitoring plan
5. Your rollback rule

---

## Reflection Questions

1. How much accuracy loss is acceptable in exchange for latency improvement?
2. What kinds of failures should always block release, even if performance is better?
3. Did group members see consistent CI results, or was there meaningful variance across machines?
4. What is the most important shift-right signal after launch?

---

## Optional Stretch

If your table finishes early:

1. Define a formal release gate policy for future versions.
2. Propose one automated canary-release metric.
3. Design a release dashboard for the Release Advisory Board.

---

## Key Takeaway

MLOps is not just about running tests automatically.

It is about turning evidence from CI, performance, and production monitoring into disciplined release decisions.
