# Exercise 6: Multi-Agent Handoff and Trajectory Analysis

## Overview

This is a **two-part exercise**:
1. **Part 1 (30 min)**: Classroom demo - Generate and analyze 12 traces together
2. **Part 2 (45-55 min)**: Individual exercise - Diagnose handoff corruption

## Part 1: Classroom Demo - Batch Trace Generation (30 minutes)

### Goal
Generate a portfolio of multi-agent traces with your instructor to understand:
- **Consistency**: How does the agent handle the same prompt multiple times?
- **Robustness**: How does agent behavior change with slight variations?
- **Edge cases**: What happens with different types of questions?

### Prerequisites
1. Flask app running: `python run.py`
2. Phoenix running on http://localhost:6006
3. Ollama running with llama3.2:1b model

### Instructor Setup

**As the instructor, run this command to generate 12 traces:**

```bash
python generate_classroom_traces.py
```

This script will:
- Generate 5 traces with the **same prompt** (runs 1-5)
- Generate 4 traces with **variations** of the question (robustness)
- Generate 3 traces with **completely different prompts** (diversity)

**Total time**: ~5-7 minutes (includes inference time and delays)

### What Students Should Do During This Demo

1. **Watch the script run** — Notice how agent behavior differs across runs
2. **Wait for completion** — Script will print summary of results
3. **Open Phoenix** — Go to http://localhost:6006 → **Traces tab**
4. **Examine the traces** together with the class:

#### Activity 1: Consistency (5 minutes)
- **Filter by scenario**: Look for traces labeled "same_prompt"
- **Compare Run 1 vs Run 2**: Click on each span
  - Did the agent call the same tools?
  - Did it reach the same conclusion?
  - How many steps did each take?
- **Discussion**: "What causes different trajectories for identical prompts?"

#### Activity 2: Robustness (10 minutes)
- **Filter by scenario**: Look for traces labeled "variation"
- **Read the 4 questions**:
  1. Clear: "What testing approaches work best for large language models?"
  2. How-to: "How do I test systems that use large language models?"
  3. Comparison: "Compare different strategies for testing AI systems"
  4. Why: "Why is testing AI-based systems challenging?"
- **Analyze each trace**:
  - Did the agent use different tools?
  - How did grounding/relevance differ?
  - Which phrasing caused hallucinations?
- **Discussion**: "Why does wording matter for multi-agent systems?"

#### Activity 3: Diversity (10 minutes)
- **Filter by scenario**: Look for traces labeled "different_prompt"
- **Examine 3 diverse prompts**:
  1. Definition question
  2. Technical explanation
  3. Evaluation metrics
- **Compare trajectories**:
  - How different were the decision trees?
  - Did any fail or loop?
  - Which was most efficient?
- **Discussion**: "When does a multi-agent system shine vs struggle?"

### Classroom Discussion Questions (5 minutes)

**Ask the class:**
1. "Which scenario had the most variation? Why?"
2. "Did you see any hallucinations in the traces? Where?"
3. "If you were designing this multi-agent system, what would you change?"

---

## Part 2: Individual Exercise - Handoff Corruption Diagnosis (45-55 minutes)

### Goal
Diagnose how corrupted state between agents breaks retrieval quality.

### Prerequisites
1. Part 1 (classroom demo) completed.
2. Understanding of multi-agent handoffs from demo traces.
3. Exercise 5 completed.

### Scenario
You are auditing a real multi-agent flow in LangChain with core roles **Triage Agent** and **RAG Specialist** (and an optional **Validator Agent** when enabled). The orchestrator routes work between specialist capabilities instead of forcing retrieval every time. Your goal is to study the hand-off graph in Phoenix and diagnose how corrupted state can break retrieval.

### Individual Student Tasks
4. Use these queries during this exercise:
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

