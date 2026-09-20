# Exercise 6 Instructor Notes: Multi-Agent Handoff and Trajectory Analysis
Facilitator reference: [Instructor Facilitation Rubric](Exercise-Instructor-Facilitation-Rubric.md)

## Prerequisites
1. Completion of Exercise 5.
2. Crew mode turned on in the demo chatbot.
3. The MLflow tracking server is running at [http://localhost:5001](http://localhost:5001).

## Scenario
This exercise continues the same case assignments from Exercises 4 and 5, but in **Crew mode**. Students compare the Ask trace, the single-agent trace, and the multi-agent handoff trace for the same prompt, then diagnose how a corrupted state or mutated handoff can break retrieval quality.

## Review Workflow: Complete the Shared Demo

Use the same facilitator prompt from Exercises 4 and 5 as a short Crew-mode comparison:

```text
How do I detect hallucinations in RAG systems?
```

Review the three traces together:

1. Ask: `rag.query` -> `rag.retrieve` -> `rag.generate`
2. Agent: `Single-Agent ReAct` -> `query_knowledge_base`
3. Crew: `Triage Agent` -> `rag_agent_tool` -> `RAG Specialist`

Compare the final answers, retrieval evidence, latency, tool calls, and handoff fields. Students then run their own carried-forward prompt assignment in Crew mode before the team performs the separate handoff-corruption control.

## Role Assignments

Divide the team across 3-5 roles:

- **MLflow Navigator**: Opens MLflow and filters traces
- **Trajectory Analyst**: Examines span sequences and tool calls
- **Evidence Scribe**: Records findings in the results table
- **Debugger** (optional): Proposes fixes based on findings

## Team Exercise - Handoff Corruption Diagnosis

### Goal
As a team, continue the same case assignments from Exercises 4 and 5, now in Crew mode. Compare how each assigned prompt changes when a Triage Agent routes it to a RAG Specialist, then diagnose how corrupted state between agents breaks retrieval quality.

### Activity 1: Assigned Prompt Comparison
1. In the demo chatbot, select **Agent** mode and turn **Crew Mode ON**.
2. Run the same prompt assigned to you in Exercises 4 and 5.
3. Capture the UI response, steps taken, tools called, and final answer.
4. In MLflow, inspect the **Triage Agent → RAG Specialist handoff** and compare the Crew trace with your Ask and Agent traces for the same prompt.
5. Fill your assigned row in the table below.

### Activity 2: Corrupted Handoff Detection
1. After everyone has completed their assigned prompt, run this shared control query with Crew mode ON:
   ```
   simulate handoff corruption for retrieval query about 2024 regression failures
   ```
2. Capture corrupted evidence:
   - In UI response, note whether retrieval failed or the query was modified.
   - In MLflow, inspect the same **Triage Agent → RAG Specialist handoff**.
   - Compare the original query with the routed query and the specialist output.
3. Analyze side-by-side:
   - Did the query text change between agents?
   - Did the routed query preserve the year and other retrieval-relevant detail?
   - Did the retrieved response remain relevant after the mutation?
   - Inspect `handoff.original_query`, `handoff.routed_query`, `handoff.mutated`, and `handoff.integrity_status` on the specialist span.
   - Compare `trajectory_metrics.handoffs`, `trajectory_metrics.tool_calls`, and `trajectory_metrics.poisoned_retrieval`.
4. Fill the corruption-control row in the table below.

## Results Table

| Run Type | Query Summary | Actual Steps | Handoff Query Intact? | Retrieval Success? | Root Cause |
|---|---|---:|---|---|---|
| case1 | Exercise 4 case 1 prompt | | Yes / No | Yes / No | — |
| case2 | Exercise 4 case 2 prompt | | Yes / No | Yes / No | — |
| case3 | Exercise 4 case 3 prompt | | Yes / No | Yes / No | — |
| case4 | Exercise 4 case 4 prompt | | Yes / No | Yes / No | — |
| case5 | Exercise 4 case 5 prompt | | Yes / No | Yes / No | — |
| corruption control | Regression failures | | Yes / No | Yes / No | [Find in MLflow] |

## Team Debrief

1. **What exactly was corrupted in the handoff?** (Original query vs. mutated)
2. **What did the corrupted routing change in the retrieved response?** (Compare query detail and relevance)
3. **If you were designing this orchestrator, what guardrail would you add?** (For example: schema validation, checksums, or explicit state contracts)

### Prompt-Specific Teaching Issue to Highlight
If students miss the issue, call attention to the exact trace evidence created by the prompts:
- The assigned prompt comparison is meant to show that the answer looks reasonable even when the query or retrieval context has drifted.
- The corruption control (`simulate handoff corruption for retrieval query about 2024 regression failures`) is designed to reveal whether the query mutates during the Triage-to-RAG handoff.
- The teaching problem is not only a wrong answer; it is a hidden state bug where the retrieval logic is operating on altered input, which breaks grounding without always producing an obviously broken response.
- Students should use `handoff.original_query`, `handoff.routed_query`, and `trajectory_metrics.poisoned_retrieval` as the primary bug signal.

## Runtime boundary

Crew mode is intentionally bounded: the default configuration allows four crew iterations and a 25-second execution budget. This exercise inspects one specialist handoff and its contract; it does not require an unbounded retry loop. If the live provider is unavailable, use `artifacts/precomputed/trace_samples/exercise6_trajectory_cases_20260416_190513.json` as a fallback, but prioritize the live trace for the current handoff fields.

## Evidence to capture

For both runs, record:

- the UI response, trajectory steps, and tools called
- the `Triage Agent` root span and the `RAG Specialist` span
- `handoff.original_query` and `handoff.routed_query`
- `handoff.mutated` and `handoff.integrity_status`
- retrieved output and final response relevance
- `trajectory_metrics.handoffs`, `trajectory_metrics.tool_calls`, and `trajectory_metrics.poisoned_retrieval`

## Optional: Control Test

If time permits, run the same corrupted query with **Crew Mode OFF** (single-agent).

- Expected: no handoff, no corruption.
- Observation: does it perform better or worse?
- Insight: is corruption a handoff problem or an LLM problem?

## Team debrief questions
1. What caused the worst inefficiency: loop, bad handoff, or over-delegation?
2. Where exactly was input corrupted in the handoff chain?
3. What orchestrator rule or schema check would prevent this next time?


