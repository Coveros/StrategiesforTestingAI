# Exercise 6: Multi-Agent Handoff and Trajectory Analysis

## Overview

**Team Exercise (30 minutes max)**
- Focus: Diagnose a bounded handoff and understand state mutation impact on multi-agent systems

## Prerequisites
1. Completion of Exercise 5
2. Crew mode turned on in the demo chatbot
3. The MLflow tracking server is running at [http://localhost:5001](http://localhost:5001).

## Team Exercise - Handoff Corruption Diagnosis (30 minutes)

### Goal
As a team, continue the same case assignments from Exercises 4 and 5, now in
Crew mode. Compare how each assigned prompt changes when a Triage Agent routes
it to a RAG Specialist, then diagnose how corrupted state between agents breaks
retrieval quality.

### Role Assignments (Divide these among 3-5 team members)
- **MLflow Navigator**: Opens MLflow and filters traces
- **Trajectory Analyst**: Examines span sequences and tool calls
- **Evidence Scribe**: Records findings in the results table
- **Debugger** (optional): Proposes fixes based on findings

### Activities (30 minutes total)

#### Activity 1: Assigned Prompt Comparison (10 minutes)
1. In the demo chatbot, select **Agent** mode and turn **Crew Mode ON**.
2. Run the same prompt assigned to you in Exercises 4 and 5.
3. Capture the UI response, steps taken, tools called, and final answer.
4. In MLflow, inspect the **Triage Agent → RAG Specialist handoff** and
   compare the Crew trace with your Ask and single-Agent traces for the same
   prompt.
5. Fill your assigned row in the table below.

#### Activity 2: Corrupted Handoff Detection (15 minutes)
1. After everyone has completed their assigned prompt, run this shared control
   query with Crew mode ON:
   ```
   simulate handoff corruption for retrieval query about 2024 regression failures
   ```
2. **Capture corrupted evidence:**
   - In UI response, note: Did retrieval fail? Was the query modified?
   - In MLflow, inspect the same **Triage Agent → RAG Specialist handoff**
   - Compare original query vs. what RAG Specialist received
3. **Analyze side-by-side:**
   - Did the query text change between agents?
   - Did the routed query preserve the year and other retrieval-relevant detail?
   - Did the retrieved response remain relevant after the mutation?
   - Inspect `handoff.original_query`, `handoff.routed_query`, `handoff.mutated`, and `handoff.integrity_status` on the specialist span.
   - Compare `trajectory_metrics.handoffs`, `trajectory_metrics.tool_calls`, and `trajectory_metrics.poisoned_retrieval`.
4. **Fill the corruption-control row in the table** (see below)

### Results Table

| Run Type | Query Summary | Actual Steps | Handoff Query Intact? | Retrieval Success? | Root Cause |
|---|---|---:|---|---|---|
| case1 | Exercise 4 case 1 prompt | | Yes / No | Yes / No | — |
| case2 | Exercise 4 case 2 prompt | | Yes / No | Yes / No | — |
| case3 | Exercise 4 case 3 prompt | | Yes / No | Yes / No | — |
| case4 | Exercise 4 case 4 prompt | | Yes / No | Yes / No | — |
| case5 | Exercise 4 case 5 prompt | | Yes / No | Yes / No | — |
| corruption control | Regression failures | | Yes / No | Yes / No | [Find in MLflow] |

### Team Debrief (5 minutes)

1. **"What exactly was corrupted in the handoff?"** (Original query vs. mutated)
2. **"What did the corrupted routing change in the retrieved response?"** (Compare query detail and relevance)
3. **"If you were designing this orchestrator, what guardrail would you add?"** (e.g., schema validation, checksums, explicit state contracts)

### Runtime boundary

Crew mode is intentionally bounded: the default configuration allows four crew
iterations and a 25-second execution budget. This exercise inspects one
specialist handoff and its contract; it does not require an unbounded retry
loop. If the live provider is unavailable, use
`artifacts/precomputed/trace_samples/exercise6_trajectory_cases_20260416_190513.json`
as a fallback, but prioritize the live trace for the current handoff fields.

### Optional: Control Test (Extra)
If time permits, run the same corrupted query with **crew mode OFF** (single-agent).
- Expected: No handoff, no corruption
- Observation: Does it perform better or worse?
- Insight: Is corruption a handoff problem or an LLM problem?

## Evidence to capture

For both runs, record:

- the UI response, trajectory steps, and tools called
- the `Triage Agent` root span and the `RAG Specialist` span
- `handoff.original_query` and `handoff.routed_query`
- `handoff.mutated` and `handoff.integrity_status`
- retrieved output and final response relevance
- `trajectory_metrics.handoffs`, `trajectory_metrics.tool_calls`, and
   `trajectory_metrics.poisoned_retrieval`

