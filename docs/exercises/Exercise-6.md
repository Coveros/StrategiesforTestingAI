# Exercise 6: Multi-Agent Handoff and Trajectory Analysis

## Overview

**Team Exercise (30 minutes max)**
- Pre-generated traces available in Phoenix
- Focus: Diagnose handoff corruption and understand state mutation impact on multi-agent systems

## Prerequisites
1. Flask app running: `python run.py`
2. Phoenix running on http://localhost:6006
3. Pre-generated traces from `python generate_classroom_traces.py` (run by instructor offline)

## Team Exercise - Handoff Corruption Diagnosis (30 minutes)

### Goal
As a team, diagnose how corrupted state between agents breaks retrieval quality. Understand where handoffs introduce mutation and efficiency loss.

### Role Assignments (Divide these among 3-5 team members)
- **Phoenix Navigator**: Opens Phoenix and filters traces
- **Trajectory Analyst**: Examines span sequences and tool calls
- **Evidence Scribe**: Records findings in the results table
- **Debugger** (optional): Proposes fixes based on findings

### Activities (30 minutes total)

#### Activity 1: Baseline Clean Handoff (10 minutes)
1. **Run this query in the UI (ask or agent mode):**
   ```
   Compare two test strategies for a GenAI support bot and recommend one.
   ```
2. **Capture baseline evidence:**
   - In the UI response, record: Steps taken, tools called, final recommendation
   - In Phoenix, find this trace and click into the **Triage Agent → RAG Specialist handoff**
   - Compare: Is the original query intact when passed to RAG Specialist?
3. **Fill baseline row in table** (see below)

#### Activity 2: Corrupted Handoff Detection (15 minutes)
1. **Run this query with crew mode ON:**
   ```
   simulate handoff corruption for retrieval query about 2024 regression failures
   ```
2. **Capture corrupted evidence:**
   - In UI response, note: Did retrieval fail? Was the query modified?
   - In Phoenix, inspect the same **Triage Agent → RAG Specialist handoff**
   - Compare original query vs. what RAG Specialist received
3. **Analyze side-by-side:**
   - Did the query text change between agents?
   - How many extra steps resulted from the mutation?
   - Where did the system loop or retry?
4. **Fill corrupted row in table** (see below)

### Results Table

| Run Type | Query Summary | Actual Steps | Handoff Query Intact? | Retrieval Success? | Root Cause |
|---|---|---:|---|---|---|
| Baseline | Compare test strategies | | Yes / No | Yes / No | — |
| Corrupted | Regression failures | | Yes / No | Yes / No | [Find in Phoenix] |

### Team Debrief (5 minutes)

1. **"What exactly was corrupted in the handoff?"** (Original query vs. mutated)
2. **"What was the efficiency cost?"** (Extra steps due to retry loops)
3. **"If you were designing this orchestrator, what guardrail would you add?"** (e.g., schema validation, checksums, explicit state contracts)

### Optional: Control Test (Extra)
If time permits, run the same corrupted query with **crew mode OFF** (single-agent).
- Expected: No handoff, no corruption
- Observation: Does it perform better or worse?
- Insight: Is corruption a handoff problem or an LLM problem?

## Evidence to capture

