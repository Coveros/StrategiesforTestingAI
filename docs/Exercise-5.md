# Exercise 5: Lab - Testing an Agent

**Estimated Duration:** 45-50 minutes  
**Prerequisites:** Exercises 1-4 completed; access to the GenAI Testing Assistant in Agent Mode; Codespaces environment  
**Deliverable:** A 5-case agent test report plus a QA standup summary by testing pillar

---

## Overview

You are testing the GenAI Testing Assistant in **Agent Mode**, where quality depends on more than the final answer. In this lab, you evaluate whether the agent can reason through tasks, select tools appropriately, preserve state, stay safe, and recover cleanly from failures.

Unlike earlier labs, this is a workflow QA exercise. Your job is to inspect the full action chain, not just the response text.

---

## Scenario: Agent Mode QA

You are the QA team evaluating the GenAI Testing Assistant's **Agent Mode**.

In earlier labs, you tested outputs, retrieval quality, and evaluation logic. In this lab, you will test whether the agent's **internal reasoning and tool usage** are sound.

Your team must verify that the agent can:

1. Choose the correct tool for the task
2. Pass the exact right IDs and parameters
3. Maintain correct conversation state across turns
4. Refuse unsafe or out-of-scope actions
5. Handle tool failures gracefully

Assume the agent may interact with systems such as:

- Jira or ticketing tools
- Test script execution tools
- Internal documentation or knowledge lookup tools

---

## Group Setup

- **Table Exercise:** Your table must execute **5 total test cases**.
- **Individual Ownership:** Each person owns **1 representative test case** from one testing pillar.
- **QA Standup:** After testing independently, the table regroups and reports whether each pillar passed or failed.

---

## Key Concepts

### What Changes When You Test an Agent?

In this lab, you evaluate the full action chain:

1. **Decision:** Did the agent choose the correct tool?
2. **Execution:** Did it send the right arguments?
3. **State:** Did it remember only what it should remember?
4. **Safety:** Did it stay within allowed behavior?
5. **Recovery:** Did it handle failures honestly and usefully?

### Agent Failures Are Not Just Wrong Answers

An agent can produce a fluent answer and still fail badly if it:

- uses the wrong tool
- mutates the wrong ticket
- forgets the active context
- performs an unsafe action
- hides a tool error instead of surfacing it

---

## Part 1: Divide the Test Strategy (Table Exercise)

Assign **1 representative test case to each person** from the following categories:

### Person 1: Tool Routing

**Question:** Can the agent distinguish between similar tools?

Examples of what to test:

- Does it open documentation when the user asks for an explanation instead of running a test script?
- Does it choose Jira only when the user clearly intends to create or update a ticket?

### Person 2: Argument Extraction

**Question:** Does it pass the exact right IDs and parameters to the functions?

Examples of what to test:

- Does it pass the correct issue ID, run ID, or test name?
- Does it preserve exact environment names, paths, or identifiers?
- Does it ask for clarification instead of guessing missing parameters?

### Person 3: State Integrity

**Question:** Does the agent maintain memory across a multi-turn conversation?

Examples of what to test:

- Does it remember the ticket or run ID mentioned earlier?
- Does it stop reusing old context after the user resets the task or starts a new thread?

### Person 4: Safety/Guardrails

**Question:** Does it refuse to perform out-of-scope or destructive actions?

Examples of what to test:

- Does it refuse unsafe destructive actions?
- Does it reject unsupported requests outside its tool scope?
- Does it avoid high-impact actions without clear user intent?

### Person 5: Error Handling

**Question:** What happens if a tool returns a 404 or a timeout?

Examples of what to test:

- Does the agent surface the error clearly?
- Does it retry appropriately or ask the user what to do next?
- Does it avoid inventing a success result when the tool failed?

---

## Part 2: Execute Independently in Codespaces (15-20 minutes)

Each person runs their assigned test independently in Codespaces.

For each test case, document:

- **User Prompt:** What you asked the agent
- **Expected Behavior:** What the agent should do
- **Observed Tool Use:** Which tool(s) it actually used
- **Observed Arguments:** What IDs, fields, or parameters it passed
- **Pass/Fail:** Did the agent behave correctly?
- **Evidence:** Trace, screenshots, copied tool calls, or transcript notes

### Test Case Matrix

| Test Case ID | Pillar | User Prompt | Expected Behavior | Actual Behavior | Pass/Fail | Evidence |
|---|---|---|---|---|---|---|
| TC-01 | Tool Routing |  |  |  |  |  |
| TC-02 | Argument Extraction |  |  |  |  |  |
| TC-03 | State Integrity |  |  |  |  |  |
| TC-04 | Safety/Guardrails |  |  |  |  |  |
| TC-05 | Error Handling |  |  |  |  |  |

### What Counts as a Failure?

- Wrong tool selected
- Correct tool selected with wrong arguments
- Agent forgets or misuses prior conversation state
- Unsafe action executed without sufficient confirmation
- Tool failure hidden, misreported, or hallucinated away

---

## Part 3: QA Standup (10-12 minutes)

After independent execution, regroup at your table and hold a short QA standup.

Each person reports:

1. Their test case
2. Whether their pillar **passed or failed overall**
3. The most important defect they found
4. One recommendation for improving the agent

### QA Standup Summary Template

| Pillar | Owner | Overall Result | Top Defect Found | Recommended Fix |
|---|---|---|---|---|
| Tool Routing | Person 1 | Pass / Fail / Mixed |  |  |
| Argument Extraction | Person 2 | Pass / Fail / Mixed |  |  |
| State Integrity | Person 3 | Pass / Fail / Mixed |  |  |
| Safety/Guardrails | Person 4 | Pass / Fail / Mixed |  |  |
| Error Handling | Person 5 | Pass / Fail / Mixed |  |  |

At the end, your table should decide:

- Which pillar is strongest right now?
- Which pillar is riskiest for production?
- What should the team fix first?

---

## Deliverables

Submit one file named `exercise5_submission.md` containing:

1. All 5 completed test cases
2. A pass/fail judgment for each QA pillar
3. The QA standup summary table
4. The top 3 defects discovered across the team
5. One mitigation recommendation per top defect

---

## Reflection Questions

1. Which pillar failed most often: routing, arguments, state, safety, or error handling?
2. Which failure type would be most expensive in production?
3. Did the agent fail more often by guessing, forgetting, or overreaching?
4. If you could automate one of the five pillars first, which would you choose and why?

---

## Optional Stretch

If your table finishes early:

1. Create one additional adversarial test for each pillar.
2. Re-run one failed case with a rewritten prompt and compare results.
3. Propose a lightweight regression suite for Agent Mode based on the defects you found.

---

## Key Takeaway

Testing an agent means testing more than outputs.

You must verify that the agent can **choose, act, remember, refuse, and recover** correctly. High-quality agent behavior depends on the full workflow, not just the final wording of the response.
