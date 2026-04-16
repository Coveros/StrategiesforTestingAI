# Exercise 6: Lab - Testing Multi-Agent Systems - Instructor Notes

---

## Overview

Students move from testing single-agent behavior to testing **multi-agent workflows**. The core question in this lab is not just whether the assistant produced a good answer. The question is whether the **Crew** moved through the task efficiently, handed work off correctly, and avoided wasteful loops.

**Key Learning Objective:** Students should learn to audit multi-agent systems through three lenses:

1. Trajectory efficiency
2. Handoff quality
3. Orchestrator control quality

This is a table-based distributed auditing lab. Each student becomes responsible for two trajectories, then the table combines evidence to identify the single worst inefficiency in the crew.

---

## Setup Checklist (10 minutes before class)

- [ ] Confirm students can access Crew or multi-agent mode
- [ ] Confirm Trace logs are visible and include steps, calls, and agent transitions
- [ ] Explain the crew roles clearly before students begin
- [ ] Ensure each table can capture **5 total trajectories**, ideally one per person
- [ ] Remind students that each person's query must be **unique and complex**
- [ ] Have the student-facing lab open: [docs/Exercise-6.md](Exercise-6.md)

---

## Timing

| Phase | Time | Notes |
|---|---|---|
| Intro and crew framing | 5 minutes | Explain Researcher, Summary Agent, and Orchestrator roles |
| Scoring example | 5 minutes | Walk through one annotated trajectory before students start |
| Part 1: Distributed auditing | 20-25 minutes | 5 total trajectories captured across the table |
| Part 2: Efficiency review | 10-15 minutes | Compare runs and identify the worst loop |
| Debrief | 5 minutes | Discuss how to improve orchestrator behavior |
| **Total** | **45-55 minutes** | Intentional deep-dive lab |

---

## Time-box Guidance

- Require one trajectory per person in the timed version.
- Use the annotated example to reduce argument about how to count steps.
- If discussion runs long, force the table to pick one worst loop and move on.

---

## Expected Findings

### Trajectory Efficiency

Common failure patterns:

- The orchestrator delegates twice when one handoff would have been enough
- The same agent repeats a step with no new information gained
- The system re-queries evidence already available in the trace

What strong student evidence looks like:

- Clear comparison between Actual Steps and Optimal Steps
- Explanation of which steps were unnecessary

### Handoff Quality

Common failure patterns:

- Researcher finds useful evidence but Summary Agent omits it
- Summary Agent receives a vague or incomplete handoff
- The orchestrator re-asks an agent for work that was already completed

What strong student evidence looks like:

- Students can point to where context or intent was dropped between agents
- Students can explain why the handoff caused extra work or weaker output

### Orchestrator Quality

Common failure patterns:

- Over-delegation: too many agent turns for a simple task
- Under-delegation: wrong agent chosen or no specialization used when needed
- Weak stop behavior: the crew continues after sufficient evidence has already been gathered

What strong student evidence looks like:

- Students identify the exact loop trigger
- Students propose a prompt improvement that changes orchestrator behavior, not just agent wording

---

## Facilitation Tips

### While Students Capture Trajectories

Push them to be concrete:

- "What made this step necessary?"
- "Which step added no new value?"
- "Where did the orchestrator make the workflow longer than needed?"

### While Students Compute Efficiency Scores

Use prompts like:

- "What is the minimum path this crew should have taken?"
- "Did the extra step improve quality, or just add overhead?"
- "If this ran 10,000 times a day, where would cost explode first?"

### During the Efficiency Review

Keep the group focused on one worst loop:

- Ask each person to nominate one inefficient trajectory
- Require the table to choose **one** worst loop, not several
- Push for a prompt-level orchestrator fix, not a vague "make it smarter" statement

---

## Rubric (0-2 per dimension)

### Trajectory Audit Quality (0-2)

- **0:** Incomplete or unclear trajectory records
- **1:** Most fields captured, but step logic or notes are weak
- **2:** Clear trajectory capture with step count, handoff evidence, and efficiency reasoning

### Efficiency Analysis Quality (0-2)

- **0:** No clear Optimal vs. Actual comparison
- **1:** Efficiency scores calculated but weakly interpreted
- **2:** Efficiency scores used well to identify specific waste or loops

### Group Efficiency Review Quality (0-2)

- **0:** No clear worst loop selected
- **1:** Loop identified but explanation is vague or unsupported
- **2:** Single worst loop identified with strong evidence and group consensus

### Improvement Proposal Quality (0-2)

- **0:** Generic recommendation only
- **1:** Somewhat relevant improvement but not tied to the loop cause
- **2:** Specific orchestrator prompt improvement directly linked to the observed inefficiency

**Total: 8 points**

---

## Strong Mitigations to Reward

If students propose these, reward strongly:

1. Add stop rules to the orchestrator once enough evidence is gathered
2. Add delegation constraints so the same task is not reassigned redundantly
3. Add handoff templates or structured payload requirements between agents
4. Add repeated-call detection to suppress loops
5. Add step budgets or trajectory budgets for complex tasks

---

## Transition and Bridge Language

### Opening (Connect to Exercise 5)

"In Exercise 5, you tested whether one agent could choose and act correctly. In this lab, we raise the bar: when several agents collaborate, does the workflow stay efficient and coherent?"

### Mid-Lab Framing

"A crew can look intelligent while still being wasteful. Your job is to inspect the trace and ask: did every step create value, or did the orchestrator create motion without progress?"

### Closing (to next stage)

"You just audited multi-agent trajectories manually. The next step is to turn efficiency, handoff quality, and loop detection into regression metrics that can run automatically."

---

## Common Student Mistakes and Corrections

| Mistake | What You Hear | Correction |
|---|---|---|
| Focuses only on final answer quality | "The result was fine" | "Fine results can still hide inefficient or fragile workflows." |
| Treats all extra steps as acceptable | "It only took one extra call" | "One extra call matters if it repeats thousands of times a day." |
| Confuses redundancy with collaboration | "Both agents were helping" | "Were both steps necessary, or did they duplicate work?" |
| Blames the worker agent only | "The Summary Agent looped" | "What orchestrator instruction caused that repeated delegation?" |
| Suggests vague fixes | "Improve the prompt" | "What exact orchestrator instruction would reduce this loop?" |

---

## Answers to Anticipated Questions

**Q: What if a trajectory is inefficient but still correct?**  
A: That still counts as a defect. In multi-agent systems, wasted steps are cost, latency, and reliability problems.

**Q: Do all 5 trajectories need to use the same query type?**  
A: No. Variety is useful as long as the queries are complex enough to exercise handoffs and delegation.

**Q: What if two students find different loops?**  
A: That is expected. The table must compare them and select the single worst one based on evidence and efficiency impact.

**Q: Should students edit prompts or code during this lab?**  
A: Not required. The core deliverable is diagnosis plus one proposed orchestrator prompt improvement.

---

## Debrief (5-10 minutes)

Ask the room:

1. What was the worst loop you found today?
2. Which handoff was most fragile?
3. What one orchestrator rule would you add first?

Map answers back to controls:

- repeated delegation -> delegation limits or repeated-call suppression
- fragile handoffs -> structured handoff contracts
- weak stopping behavior -> explicit stop rules and trajectory budgets

---

## Optional Deep Dive

If a group finishes early:

1. Ask them to define a "golden trajectory" for one of their queries
2. Ask them to create a loop-detection heuristic for the orchestrator
3. Ask them to rank inefficiency sources by production cost impact

