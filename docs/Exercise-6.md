# Exercise 6: Lab - Testing Multi-Agent Systems

**Estimated Duration:** 45-55 minutes  
**Prerequisites:** Exercise 5 completed; access to Crew or multi-agent mode with Trace logs enabled  
**Deliverable:** A 5-trajectory audit report with efficiency scores and one orchestrator improvement proposal

---

## Overview

The assistant now uses a **Crew** of cooperating agents, such as a **Researcher** and a **Summary Agent**. In this lab, you are no longer testing a single agent's decisions. You are auditing the **trajectories and handoffs** across a multi-agent workflow.

Your job is to determine whether the crew makes progress efficiently, avoids redundant loops, and hands work between agents without losing intent or context.

---

## Scenario: Auditing a Crew

You are the QA team auditing a multi-agent assistant that uses a small crew to answer complex requests.

For example, the system may behave like this:

- **Researcher Agent:** gathers information, references, or evidence
- **Summary Agent:** synthesizes findings into a final response
- **Orchestrator:** decides who should act next and when the workflow should stop

You must inspect the **Trace logs** to understand:

1. How many steps were taken
2. Whether there were redundant or looping calls
3. Whether handoffs between agents succeeded
4. Whether the orchestrator made the workflow longer than necessary

---

## Group Setup

- **Distributed Auditing:** As a table, you must capture and analyze **5 trajectories total**.
- **Individual Ownership:** Each person runs **1 unique complex query**.
- **Efficiency Review:** After individual runs, the table compares all 5 trajectories and identifies the single worst inefficiency.

Before you start, review one instructor-provided annotated example trajectory so the table has a shared scoring model.

Precomputed trajectory samples are available at:

- `artifacts/precomputed/trace_samples/exercise6_trajectory_cases_*.json`

Use these captures when live crew tracing is unavailable or when you need to accelerate table setup.

---

## Key Concepts

### What Is a Trajectory?

A trajectory is the full path the crew takes from user request to final answer.

That path may include:

1. Orchestrator decisions
2. Agent handoffs
3. Tool calls
4. Intermediate observations
5. Final stop conditions

### Multi-Agent Quality Is About More Than Correctness

A crew can still fail even if the final answer looks acceptable.

Common multi-agent failure modes include:

- repeated unnecessary steps
- loops between agents
- redundant tool calls
- weak handoffs where context is dropped
- over-delegation by the orchestrator

### Efficiency Score

For each run, compute:

$$
Efficiency\ Score = \frac{Optimal\ Steps}{Actual\ Steps}
$$

Interpretation:

- **1.00** = ideal trajectory
- **0.70-0.99** = acceptable overhead
- **Below 0.70** = clear inefficiency bug

---

## Part 1: Distributed Auditing (Table Exercise)

As a group, you must capture and analyze **5 trajectories** total.

Each person runs **1 unique complex query** and uses the Trace logs to track:

- steps taken
- redundant calls
- handoff success

### What to Record for Each Run

- **Query:** the exact user request
- **Agents Involved:** which crew members acted
- **Steps Taken:** total number of trajectory steps
- **Redundant Calls:** repeated agent actions or tool calls that did not add value
- **Handoff Success:** whether intent and context were preserved between agents
- **Actual Steps:** observed step count from the trace
- **Optimal Steps:** your estimate of the minimum necessary path
- **Efficiency Score:** Optimal Steps / Actual Steps

### Trajectory Audit Table

| Trajectory ID | Owner | Query | Agents Involved | Actual Steps | Optimal Steps | Efficiency Score | Redundant Calls? | Handoff Success? | Notes |
|---|---|---|---|---|---|---|---|---|---|
| T-01 | Person 1 |  |  |  |  |  |  |  |  |
| T-02 | Person 2 |  |  |  |  |  |  |  |  |
| T-03 | Person 3 |  |  |  |  |  |  |  |  |
| T-04 | Person 4 |  |  |  |  |  |  |  |  |
| T-05 | Person 5 |  |  |  |  |  |  |  |  |

### What Counts as a Multi-Agent Defect?

- The orchestrator sends work to the wrong agent
- Two agents repeat the same work unnecessarily
- The same tool is called more than needed
- A handoff loses task intent or key evidence
- The workflow continues when it should terminate

---

## Part 2: The Efficiency Review (Table Exercise)

Once all 5 trajectories are collected, compare them as a group.

Your goal is to identify the **single most inefficient loop** found at the table.

### Discussion Questions

1. Which trajectory had the lowest Efficiency Score?
2. What specific loop or redundant pattern caused the inefficiency?
3. Was the problem caused mainly by orchestrator indecision, repeated delegation, bad handoff quality, or unnecessary re-research/re-summarization?
4. How would you improve the **Orchestrator's prompt** to avoid that loop in the future?

### Efficiency Review Summary Table

| Worst Trajectory ID | Loop Observed | Why It Is Inefficient | Proposed Orchestrator Prompt Fix |
|---|---|---|---|
|  |  |  |  |

---

## Deliverables

Submit one file named `exercise6_submission.md` containing:

1. All 5 completed trajectory audits
2. An Efficiency Score for each run
3. The single worst loop identified by the table
4. A group explanation of why that loop happened
5. One proposed improvement to the Orchestrator's prompt

---

## Reflection Questions

1. Which problem was more common: redundant steps, bad handoffs, or orchestrator over-delegation?
2. Did inefficient trajectories still sometimes produce decent answers? What risk does that create?
3. Which signal was most useful for auditing a crew: step count, repeated calls, or handoff quality?
4. If you could automate one trajectory metric first, which would you choose and why?

---

## Optional Stretch

If your table finishes early:

1. Design one adversarial query likely to trigger an agent loop.
2. Propose a stopping rule for the orchestrator.
3. Draft a "golden trajectory" for one query that the crew should follow in an ideal run.

---

## Key Takeaway

Testing multi-agent systems means testing the **workflow between agents**, not just the final response.

Reliable crews depend on efficient trajectories, successful handoffs, and orchestrators that know when to delegate and when to stop.
