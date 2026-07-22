# Exercise 6 Instructor Notes: Multi-Agent Handoff and Trajectory Analysis
Facilitator reference: [Instructor Facilitation Rubric](Exercise-Instructor-Facilitation-Rubric.md)

## Prerequisites
1. Exercise 5 completed.
2. Agent mode enabled in the UI.
3. Crew Mode enabled in the UI.
4. Ability to capture trace/trajectory evidence.

## Scenario
You are auditing a real multi-agent flow in LangChain with core roles **Triage Agent** and **RAG Specialist** (and an optional **Validator Agent** when enabled). The orchestrator routes work between specialist capabilities instead of forcing retrieval every time. Your goal is to study the hand-off graph in Phoenix and diagnose how corrupted state can break retrieval.

# Exercise 6 Instructor Notes: Multi-Agent Handoff and Trajectory Analysis
Facilitator reference: [Instructor Facilitation Rubric](Exercise-Instructor-Facilitation-Rubric.md)

## Two-Part Structure

This exercise has two components:
1. **Part 1 (30 min)**: Classroom demo using `generate_classroom_traces.py`
2. **Part 2 (45-55 min)**: Individual student exercise on handoff corruption

---

## Part 1: Classroom Demo Preparation and Facilitation

### What You'll Do
1. Run `python generate_classroom_traces.py` in front of the class
2. Walk through the resulting 12 traces in Phoenix
3. Lead discussion on multi-agent behavior across 3 scenarios

### Before Class
- Ensure Flask is running: `python run.py`
- Ensure Phoenix is running: `phoenix serve --host 0.0.0.0 --port 6006`
- Ensure Ollama is running and model is warm
- Test the script once: `python generate_classroom_traces.py`
- Make note of the output file: `classroom_traces_results.json`

### During Class
1. **Announce** (2 min): "We're going to generate 12 example traces together and walk through them"
2. **Run script** (6 min): Execute the script, let students watch progress
3. **Open Phoenix** (2 min): Show http://localhost:6006 → Traces tab
4. **Activity 1 - Consistency** (5 min):
   - Show traces labeled "same_prompt"
   - Expand two runs side-by-side
   - Point out differences in tool calls, steps, latency
   - Ask: "Why did the agent decide differently?"
5. **Activity 2 - Robustness** (10 min):
   - Filter "variation" traces
   - Show how wording changes agent behavior
   - Highlight where hallucinations appear
   - Ask: "How would you make the agent more robust?"
6. **Activity 3 - Diversity** (10 min):
   - Show "different_prompt" traces
   - Point out edge cases or failures
   - Discuss efficiency differences
   - Ask: "What guardrails would you add?"
7. **Debrief** (5 min):
   - Summarize key observations
   - Bridge to Part 2 exercise
   - Explain: "Next, you'll do this analysis yourselves with corruption scenarios"

### Tips for Smooth Facilitation
- Have script output projected so students can see progress
- Keep Phoenix UI visible in another window for quick switching
- Use this language: "Notice in the trace... What do you see in the span attributes?"
- Pause at interesting traces to let students examine them
- If a trace fails, acknowledge it: "This is a real failure case you'd debug in production"

---

## Part 2: Individual Exercise - Handoff Corruption (Existing Content)

### Prerequisites

### Likely Issues, Defects, or Quality Challenges
1. Students may treat shallow crew traces as failure instead of checking handoff fields.
2. Handoff quality may degrade without obvious user-facing text changes.
3. Over-delegation or unnecessary handoffs can increase overhead without quality gains.

### Recommended Modifications to Discuss
1. Enforce handoff schema checks (required fields and immutable original query reference).
2. Add integrity assertions comparing original and routed query for high-risk cases.
3. Add a handoff-efficiency guardrail (max handoffs or min utility per handoff).

### What to Watch For in Student Traces
   - Compare two test strategies for a GenAI support bot and recommend one.
   - Create a release test plan with risks, gates, and rollback criteria.
   - Summarize noisy bug reports into top root causes and priorities.
   - Design fairness tests for a multilingual assistant.
   - Write a production readiness memo using retrieval, groundedness, and latency findings.
   - simulate handoff corruption for retrieval query about 2024 regression failures.
5. Run one non-corruption query first and capture baseline evidence from metadata.
   - In the response's **Agent Execution** block, capture: `Trajectory` (steps/tools/handoffs/redundant), `Tools Called`, and `Trace` (if shown).
   - Record this as your baseline row for that query.
6. In Phoenix, inspect the baseline run as an agent graph and confirm you can see the flow between **Triage Agent** and **RAG Specialist**. If Validator is enabled in your environment, include it in the observed flow.
7. Run the handoff-corruption scenario: `simulate handoff corruption for retrieval query about 2024 regression failures`.
8. Capture corrupted-run evidence from UI metadata and Phoenix traces.
9. Compare baseline vs corrupted run for handoff count, retrieval quality, and redundant tool calls.
10. Record results in this table for both runs:

| Run Type | Query | Actual Steps | Optimal Steps | Efficiency Score | Handoff Quality Note | Evidence |
|---|---|---:|---:|---:|---|---|
| Baseline |  |  |  |  |  |  |
| Corrupted |  |  |  |  |  |  |

11. In Phoenix, click into the hand-off between **Triage Agent** and **RAG Specialist** and compare the original query with the routed query.
12. Calculate Efficiency Score = Optimal Steps / Actual Steps.
13. As a team, propose one fix for handoff integrity and one guardrail for loop control.
14. As a control, run the same corruption prompt once with **Crew Mode OFF** and note that the handoff mutation should not appear in the single-agent path.

## Team debrief questions
1. What caused the worst inefficiency: loop, bad handoff, or over-delegation?
2. Where exactly was input corrupted in the handoff chain?
3. What orchestrator rule or schema check would prevent this next time?


