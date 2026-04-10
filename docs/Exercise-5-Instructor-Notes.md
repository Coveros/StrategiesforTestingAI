# Exercise 5: Testing Agentic Systems - Instructor Notes

---

## Objective

Students transition from chatbot output testing to agent behavior testing.

They should be able to identify and separate failures in:

1. Tool selection (routing)
2. Parameter extraction
3. State and memory integrity
4. Safety controls (least privilege, prompt injection resistance)

---

## Why This Exercise Matters

RAG chatbot tests validate answer quality. Agentic tests validate decision and execution quality.

A fluent response can still be catastrophic if the agent:

- picks the wrong tool,
- sends wrong parameters,
- forgets or leaks session state,
- executes unsafe actions.

This exercise makes those failure modes visible and testable.

---

## Setup Guidance

This lab is designed as a **simulation-first** exercise.

You can run it in one of two ways:

1. Paper simulation (fastest): Students reason through expected vs actual behavior.
2. Lightweight implementation (optional): Students prototype a tool router in Python and evaluate traces.

No production external APIs are required.

---

## Timing (55-65 minutes)

| Phase | Time | Outcome |
|-|-|-|
| Framing and walkthrough | 5 minutes | Students understand Decision vs Execution testing |
| Part A Router | 15 minutes | Router accuracy measured |
| Part B Parameters | 15 minutes | Hallucinated arguments detected |
| Part C State/Memory | 15 minutes | Session integrity validated |
| Part D Safety | 10 minutes | Injection and privilege boundaries tested |
| Debrief | 5 minutes | Failure patterns summarized |

---

## Expected Findings

### Part A: Router

Common failures students should notice:

1. Tool over-calling on chitchat prompts.
2. Wrong read tool chosen when query includes ID references.
3. Premature write action (`create_bug_ticket`) before confirmation.

Target benchmark:

- Strong teams: >= 85% router accuracy
- Developing teams: 60-80% router accuracy

### Part B: Parameters

Common failure modes:

1. Hallucinated IDs (agent fabricates `REG-xxx`).
2. Missing required fields for ticket creation.
3. Incorrect normalization of scope/severity values.
4. Failure to ask clarification when user intent is underspecified.

### Part C: State

Common failure modes:

1. Forgetting tracked entity by turn 3-5.
2. Carrying stale state into a "new session".
3. Mixing state from two unrelated prompts.

### Part D: Safety

Common failure modes:

1. Following prompt-injection instructions.
2. Performing bulk unsafe actions without approval.
3. Ignoring least-privilege constraints for write tools.

---

## Facilitation Prompts

Use these to guide students without giving away answers:

1. "Was the wrong answer caused by bad routing or bad execution?"
2. "Did the agent invent any argument the user never gave?"
3. "What state variable should exist at this step?"
4. "Would this action be acceptable in production without approval?"

---

## Rubric (0-2 per dimension)

### 1) Router Analysis (0-2)

- 0: Incomplete or no router evaluation
- 1: Partial mapping, limited justification
- 2: Complete mapping with clear pass/fail rationale

### 2) Parameter Analysis (0-2)

- 0: No clear parameter validation
- 1: Some validation, misses hallucination/clarification checks
- 2: Clear validation with hallucination and missing-info handling

### 3) State/Safety Analysis (0-2)

- 0: No state/safety reasoning
- 1: Covers either state or safety, not both
- 2: Correct analysis of both, with concrete examples

### 4) Mitigation Quality (0-2)

- 0: No practical mitigation
- 1: Generic mitigation suggestions
- 2: Specific, actionable mitigations mapped to failures

---

## Good Mitigations to Reward

If students propose these, reward strongly:

1. Add deterministic tool routing rules before LLM fallback.
2. Enforce strict JSON schema validation for tool arguments.
3. Add missing-field clarification gates before write actions.
4. Implement explicit per-session memory reset and isolation.
5. Add approval step for high-impact write tools.
6. Add max-iterations and rate limits to prevent loops.

---

## Common Misconceptions to Correct

1. "If the final answer looks fine, the agent worked."
   - Correction: Execution could still be unsafe or incorrect.

2. "Parameter extraction errors are minor."
   - Correction: Wrong parameters can trigger critical business failures.

3. "Prompt injection is just a prompt quality issue."
   - Correction: It is a control-plane safety issue that requires policy and runtime controls.

---

## Debrief (5 minutes)

Use this close:

"What failed most often today: routing, parameters, memory, or safety?  
If this were production, which failure would be most expensive?  
What one guardrail would you ship first this week?"

Collect 2-3 answers and map them to practical controls:

- Routing errors -> policy router + fallback strategy
- Argument errors -> schema and validation gates
- State errors -> session-scoped memory contracts
- Safety errors -> approval workflows and sandboxing

---

## Bridge to Next Section

Suggested transition language:

"You now know how to detect agent decision failures. Next, we scale this from manual testing to repeatable automation: trace-based assertions, synthetic conversations, and safety regression suites for agent workflows."

