# Exercise 5: Lab - Testing an Agent - Instructor Notes

---

## Overview

Students transition from testing chatbot outputs to testing **agent behavior**. The focus is no longer just whether the final answer looks good. The focus is whether the agent made the right decisions, called the right tools, preserved the right state, refused unsafe actions, and recovered properly when tools failed.

**Key Learning Objective:** Students should learn to separate agent failures into five QA pillars:

1. Tool Routing
2. Argument Extraction
3. State Integrity
4. Safety/Guardrails
5. Error Handling

This lab is intentionally structured as a **distributed QA exercise**: each person owns one pillar and becomes the table's specialist for that part of the system.

---

## Setup Checklist (10 minutes before class)

- [ ] Confirm students can access Agent Mode in Codespaces
- [ ] Confirm students know how to inspect traces, tool calls, or transcript evidence
- [ ] Explain the five testing pillars before work begins
- [ ] Ensure each table has five people if possible; if not, combine or redistribute pillars
- [ ] Remind students they must execute **5 total test cases**, one per person
- [ ] Have the student-facing lab open: [docs/Exercise-5.md](Exercise-5.md)

---

## Timing

| Phase | Time | Notes |
|---|---|---|
| Intro and framing | 5 minutes | Shift from output QA to workflow QA |
| Part 1: Divide the strategy | 8-10 minutes | Assign 1 case per person across 5 pillars |
| Part 2: Independent execution | 15-20 minutes | Students run one representative test each |
| Part 3: QA standup | 10-12 minutes | Each pillar owner reports pass/fail and top defect |
| Debrief | 5 minutes | Compare failure patterns and production risk |
| **Total** | **45-50 minutes** | - |

---

## Time-box Guidance

- Require one concrete case per pillar, not two.
- Provide prompt starters if students are spending too long inventing tests.
- Keep standup reporting to one defect and one fix per pillar.

---

## Expected Findings by Pillar

### Person 1: Tool Routing

Common failure patterns:

- Agent chooses a tool that is plausible but wrong
- Agent overuses tools for questions that only need explanation
- Agent invokes a write action too early

What good evidence looks like:

- Prompt clearly implies one tool, but the agent picks another
- Student can explain why the wrong tool increases risk or cost

### Person 2: Argument Extraction

Common failure patterns:

- Agent invents IDs, paths, or issue numbers
- Agent drops one required parameter from a tool call
- Agent guesses instead of asking a clarification question

What good evidence looks like:

- Side-by-side comparison of user-provided value vs. actual argument passed
- Identification of exactly which field was hallucinated or malformed

### Person 3: State Integrity

Common failure patterns:

- Agent forgets an earlier entity too soon
- Agent keeps stale memory after a reset/new-task instruction
- Agent mixes context from unrelated turns

What good evidence looks like:

- Multi-turn transcript with the expected remembered value
- Clear demonstration of whether the agent retained or forgot state correctly

### Person 4: Safety/Guardrails

Common failure patterns:

- Agent complies with out-of-scope or destructive requests
- Agent performs high-impact actions without enough confirmation
- Agent ignores a policy boundary because the user asked forcefully

What good evidence looks like:

- A prompt that should trigger refusal or caution
- Proof that the agent either refused correctly or failed unsafely

### Person 5: Error Handling

Common failure patterns:

- Agent hides a 404 or timeout and continues as if successful
- Agent retries blindly without telling the user
- Agent reports a fabricated success after tool failure

What good evidence looks like:

- Trace or transcript showing the tool error
- Clear judgment on whether the user would understand what happened next

---

## Facilitation Tips

### While Tables Assign Test Cases

If students are vague, push them to make tests concrete:

- "What exact prompt will you use?"
- "What exact tool should that trigger?"
- "What would failure look like in one sentence?"

### While Students Execute Independently

Use these prompts:

- "Did the agent choose wrong, or execute wrong after choosing right?"
- "Did it invent any value the user did not provide?"
- "What should the agent still remember at this turn?"
- "Should a production agent be allowed to do this without confirmation?"
- "Did the agent explain the tool failure honestly, or bluff?"

### During QA Standup

Keep the standup operational, not vague:

- Ask each person to declare **Pass, Fail, or Mixed** for their pillar
- Require one concrete defect and one concrete fix recommendation
- If a student says "it sort of failed," ask them to pick the dominant failure mode

---

## Rubric (0-2 per dimension)

### Test Case Quality (0-2)

- **0:** Cases are incomplete, vague, or not executable
- **1:** Cases are usable but expected behavior is weakly defined
- **2:** Cases are concrete, targeted, and clearly tied to one pillar

### Evidence Quality (0-2)

- **0:** No evidence or unsupported claims
- **1:** Some screenshots/transcripts but unclear interpretation
- **2:** Clear evidence showing why the case passed or failed

### QA Standup Analysis (0-2)

- **0:** No clear pass/fail reporting by pillar
- **1:** Partial reporting with generic observations
- **2:** Each pillar reported with a concrete defect and a justified judgment

### Mitigation Quality (0-2)

- **0:** No practical recommendations
- **1:** Generic fixes without linkage to evidence
- **2:** Specific mitigations mapped directly to discovered failures

**Total: 8 points**

---

## Good Mitigations to Reward

If students propose these, reward strongly:

1. Add deterministic routing rules before model fallback for high-risk actions
2. Add schema validation for tool arguments
3. Add missing-field clarification gates before write operations
4. Add explicit session reset behavior and memory isolation
5. Add approval/confirmation steps for high-impact actions
6. Add structured error surfacing for 404s, timeouts, and retries

---

## Transition and Bridge Language

### Opening (Connect to Exercise 4)

"In Exercise 4, you diagnosed where a RAG pipeline failed. In this lab, you go one layer higher: when an agent reasons, chooses tools, and takes actions, where does that workflow fail?"

### Mid-Lab Framing

"Each person is testing one pillar, but production incidents rarely stay in one pillar. Wrong routing can create bad arguments; bad state can trigger safety issues. Use your pillar to find the first break in the chain."

### Closing (to next stage)

"You just tested agent behavior manually across routing, arguments, memory, safety, and recovery. The next step is to turn these checks into repeatable agent regression suites."

---

## Common Student Mistakes and Corrections

| Mistake | What You Hear | Correction |
|---|---|---|
| Focuses only on final wording | "The answer sounded fine" | "Fine wording is not enough. Did the agent choose and act correctly?" |
| Treats missing arguments as minor | "It mostly got the ticket ID right" | "Near-correct IDs can be production-critical failures." |
| Confuses memory with hallucination | "It hallucinated the issue number" | "Check whether it guessed, or reused stale state from earlier turns." |
| Treats safety as refusal-only | "It did not refuse, so safety failed" | "Sometimes safe behavior is clarification, not outright refusal." |
| Ignores tool failure transparency | "The tool timed out, but it kept going" | "That is an error-handling defect. The user must know what failed." |

---

## Answers to Anticipated Questions

**Q: What if a test case fits more than one pillar?**  
A: That is normal. Have the student assign it to the pillar representing the first or most important failure, then mention cross-pillar effects in notes.

**Q: Do students need real Jira or production systems?**  
A: No. Simulated or observed tool behavior is sufficient. The goal is reasoning quality and evidence-backed diagnosis.

**Q: What if a table has fewer than five people?**  
A: Combine pillars. The best merge options are Tool Routing + Argument Extraction, or Safety + Error Handling.

**Q: Should students fix the agent during this lab?**  
A: Not required. The primary deliverable is diagnosis quality, standup reporting, and mitigation design.

---

## Debrief (5-10 minutes)

Ask the room:

1. Which pillar failed most often today?
2. Which single failure would be most expensive in production?
3. What one guardrail would you ship first this week?

Map answers back to controls:

- Routing failures -> policy router + fallback strategy
- Argument failures -> schema validation + clarification gates
- State failures -> session-scoped memory contracts
- Safety failures -> approvals, policy checks, sandboxing
- Error handling failures -> surfaced errors, retry policy, user-visible recovery

---

## Optional Deep Dive

If a group finishes early:

1. Ask them to design a sixth pillar: observability and trace quality
2. Ask them to convert one manual case into a reusable regression test template
3. Ask them to rank the five pillars by production risk and justify the ranking

