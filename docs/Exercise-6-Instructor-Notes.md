# Exercise 6: Trajectory Analysis and Multi-Agent Handoff Testing - Instructor Notes

---

## Objective

Students should move from single-agent assertions to workflow-level diagnostics.

They must identify issues in:

1. Trajectory efficiency
2. Multi-agent handoff integrity
3. Loop/livelock risks
4. Safety and privilege boundaries under orchestration

---

## Setup Checklist

1. Start the app and verify [http://localhost:5000](http://localhost:5000) loads.
2. Open [http://localhost:5000/?instructor=1](http://localhost:5000/?instructor=1).
3. Enable Agent Mode, Show Trace, and Crew Mode.
4. Run one warm-up prompt to confirm telemetry appears:
   - Tools Called
   - Handoffs
   - Trajectory metrics
5. Remind students to preserve the same session during Part A and reset only when instructed.
6. For a guaranteed loop/thrash case during Part B, use prompt: "simulate bad trajectory" (Crew Mode only).

---

## Timing (55-65 minutes)

| Phase | Time | Outcome |
|-|-|-|
| Intro + architecture framing | 5 minutes | Students understand Coordinator/Specialist handoff model |
| Part A baseline trajectories | 15-20 minutes | 6 clean traces captured |
| Part B stress trajectories | 15 minutes | Loop/safety/drift defects identified |
| Part C handoff audit | 10-15 minutes | Context preservation assessed |
| Part D efficiency scoring | 10 minutes | Golden trajectory drafted |
| Debrief | 5 minutes | Improvement priorities shared |

---

## Expected Findings

### Baseline behavior (Part A)

Students should observe:

1. One main tool call for direct requests.
2. Two handoffs per routed request:
   - Coordinator -> Specialist
   - Specialist -> Coordinator
3. State persistence for tracked failure IDs until reset.
4. Early termination after reset command.

### Stress behavior (Part B)

Students should observe:

1. Prompt-injection style requests blocked or constrained.
2. Clarification requests when required write-action fields are missing.
3. Potential inefficiency on compound requests if decomposition is weak.
4. Deterministic loop/thrash telemetry when using "simulate bad trajectory".

### Handoff risks (Part C)

Typical student-identified weak points:

1. Missing payload detail between handoffs.
2. Coordinator summary omits specialist context.
3. Tracked state not used when it should be.

---

## Rubric (0-2 per dimension)

### 1) Trajectory Capture Quality (0-2)

- 0: Incomplete captures; telemetry missing for most prompts
- 1: Partial capture; some prompts have sufficient evidence
- 2: Complete captures with tools, handoffs, and metrics for all required prompts

### 2) Failure Diagnosis Quality (0-2)

- 0: Vague statements without trace evidence
- 1: Some valid diagnoses; weak evidence linkage
- 2: Clear diagnosis of loop/safety/drift with trace-backed proof

### 3) Handoff Analysis Quality (0-2)

- 0: No handoff analysis
- 1: Basic handoff checks; misses context-loss details
- 2: Strong handoff audit with payload expectations and observed losses

### 4) Improvement and Golden Path Quality (0-2)

- 0: Generic suggestions only
- 1: Some actionable ideas but no prioritization
- 2: Concrete, prioritized fixes plus a realistic golden trajectory

---

## Facilitation Prompts

Use these to coach analysis depth:

1. "Which step added no value to goal progress?"
2. "Where did information get transformed, and did meaning change?"
3. "Could this workflow terminate earlier with the same quality?"
4. "Which handoff contract is implicit here and should be explicit?"
5. "If this ran 10,000 times/day, where would cost or risk spike first?"

---

## Common Misconceptions to Correct

1. "If final response is acceptable, trajectory quality is irrelevant."
   - Correction: Inefficient trajectories are reliability and cost bugs.

2. "Any handoff counts as good collaboration."
   - Correction: Handoff must preserve required state and intent, not just pass text.

3. "Livelock requires obvious infinite loops."
   - Correction: Repeated partial progress with no completion is also livelock risk.

---

## Strong Mitigations to Reward

1. Handoff schema contracts (required keys, validation)
2. Turn and tool-call circuit breakers
3. Redundant-call suppression rules
4. Goal-progress scoring with early-stop policy
5. Explicit memory reset checkpoints between workflows

---

## Debrief (5 minutes)

Ask three quick questions:

1. "What was your highest-impact inefficiency?"
2. "What was your most fragile handoff?"
3. "What one guardrail would you implement tomorrow?"

Then map answers to engineering controls:

- inefficiency -> trajectory budget and stop criteria
- fragile handoff -> typed contract and validation
- safety leakage -> privilege boundaries and approval gates

---

## Bridge to Next Section

Suggested transition:

"You can now audit multi-agent trajectories manually. Next we automate this with trajectory regression tests, so every build checks loop risk, handoff quality, and efficiency drift before release."

