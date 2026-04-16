# Exercise 9: Lab - Automating the Test Run / MLOps - Instructor Notes

---

## Overview

Students conclude the course by simulating the **final Go/No-Go Release Meeting**. This lab is about evidence-based release management: compare a baseline and candidate version, debate the trade-offs, cast a release vote, and define a shift-right monitoring plan.

**Key Learning Objective:** Students should learn to combine three kinds of evidence into one release decision:

1. CI test results
2. Performance trade-offs
3. Production monitoring and rollback readiness

This is both an automation lab and a release-governance lab.

---

## Setup Checklist (10 minutes before class)

- [ ] Confirm students can run the CI suite in their own Codespace
- [ ] Confirm the suite produces baseline and candidate results that students can compare
- [ ] Ensure students can see or record Pass Rate and Latency on their own machine
- [ ] Explain the release-meeting scenario before execution begins
- [ ] Remind students that the table will act as the **Release Advisory Board**
- [ ] Have the student-facing lab open: [docs/Exercise-9.md](Exercise-9.md)

---

## Timing

| Phase | Time | Notes |
|---|---|---|
| Intro and release framing | 5 minutes | Explain baseline vs candidate comparison |
| Part 1: Individual analysis | 10-12 minutes | Everyone reviews provided CI output and records Pass Rate and Latency |
| Part 2: Release Advisory Board | 10-12 minutes | Table debates Ship vs No-Ship |
| Part 3: Shift-right plan | 8-10 minutes | Define monitoring and rollback rules |
| Debrief | 5 minutes | Discuss release rationale and evidence quality |
| **Total** | **35-45 minutes** | - |

---

## Time-box Guidance

- Pre-run the CI suite before class and distribute the baseline-versus-candidate results.
- Keep the board debate to one evidence-based reason per person.
- Use the monitoring template as a selection exercise, not an open-ended design exercise, if time is tight.

---

## Expected Findings

### Individual CI Analysis

Common findings:

- Small machine-to-machine variation in latency
- Possible minor variance in observed pass results depending on environment or timing
- Clear trade-off framing once students compare speed vs quality

What strong evidence looks like:

- Student records both Baseline and Candidate results explicitly
- Student can explain whether observed differences look stable or noisy

### Release Advisory Board Discussion

Expected tension:

- Some students will argue **Ship** because the 30% speed gain is operationally valuable
- Some students will argue **No-Ship** because any measurable accuracy decline is risky
- The best discussions ground the decision in business risk and monitoring readiness, not opinion alone

What strong evidence looks like:

- Every student contributes one concrete reason for Ship or No-Ship
- The board gives a rationale tied to both latency and accuracy trade-offs

### Shift-Right Monitoring

Strong student plans usually include:

- accuracy drift monitoring
- latency or TTFT alerting
- safety or complaint monitoring
- a rollback condition tied to real thresholds

---

## Facilitation Tips

### While Students Run the CI Suite

Push them to compare, not just run:

- "What changed from v1.0 to v2.0?"
- "Would you trust this difference if only one person observed it?"
- "Is the latency gain large enough to matter operationally?"

### During the Board Debate

Keep the conversation disciplined:

- Require every person to state Ship or No-Ship explicitly
- Require one evidence-based reason per person
- Do not let the table end with "it depends" without a vote

### While Designing Shift-Right Monitoring

Use prompts like:

- "What signal would tell you the candidate is hurting users after launch?"
- "When would you rollback automatically vs manually?"
- "What do you want to see in the first 24 hours after release?"

---

## Rubric (0-2 per dimension)

### Individual Analysis Quality (0-2)

- **0:** Missing or incomplete baseline/candidate comparison
- **1:** Results captured but weakly interpreted
- **2:** Clear comparison of Pass Rate and Latency with sound interpretation

### Board Deliberation Quality (0-2)

- **0:** No clear discussion or vote
- **1:** Debate occurred but rationale was shallow
- **2:** Every person contributed a reason and the final vote was evidence-based

### Release Decision Quality (0-2)

- **0:** Ship/No-Ship decision unsupported
- **1:** Some justification present but weak trade-off reasoning
- **2:** Decision clearly justified using performance, quality, and risk evidence

### Shift-Right Monitoring Quality (0-2)

- **0:** Generic monitoring ideas only
- **1:** Some metrics named, but thresholds/actions are weak
- **2:** Concrete metrics, thresholds, rollback logic, and monitoring window defined

**Total: 8 points**

---

## Strong Mitigations to Reward

If students propose these, reward strongly:

1. Canary release or partial rollout before full production release
2. Accuracy and latency dashboards with alert thresholds
3. Automatic rollback when quality drops beyond a defined threshold
4. User feedback or thumbs-down complaints feeding back into CI tests
5. Daily or weekly drift checks after release

---

## Transition and Bridge Language

### Opening (Connect to Exercise 8)

"In Exercise 8, you attacked the assistant to expose trust and safety weaknesses. In this final lab, you move into release governance: given all the evidence you've learned to collect, would you actually ship the new version?"

### Mid-Lab Framing

"Release decisions are rarely perfect choices. They are trade-off decisions. Your job is to make the trade-off explicit and justify it."

### Closing (Course Closeout)

"You started by evaluating single outputs. You now have the full lifecycle: diagnose, automate, stress, red-team, gate, ship, and monitor. That is modern AI testing."

---

## Common Student Mistakes and Corrections

| Mistake | What You Hear | Correction |
|---|---|---|
| Focuses only on speed | "It's 30% faster, so ship it" | "Speed matters only if the quality loss is acceptable and monitored." |
| Focuses only on accuracy | "Any drop means no-ship" | "Sometimes a small drop is acceptable if the gain is meaningful and well-monitored." |
| Treats one machine's result as final truth | "My latency looked fine" | "Compare across the table. Release decisions need broader evidence." |
| Votes without rationale | "I vote ship" | "Why? What evidence makes that the better release decision?" |
| Ignores post-release risk | "The CI passed enough" | "What would you watch after launch, and when would you rollback?" |

---

## Answers to Anticipated Questions

**Q: What if different people see slightly different latency numbers?**  
A: That is expected. Students should discuss whether the difference is noise or a meaningful trend.

**Q: Is a 2% accuracy drop always unacceptable?**  
A: No. The point of the lab is to debate whether that trade-off is justified by the 30% speed gain and production monitoring readiness.

**Q: What if the board splits evenly?**  
A: Require a final tie-break rationale from the table, such as choosing the more conservative position or deferring release pending canary rollout.

**Q: Should students implement monitoring during this lab?**  
A: Not required. The main deliverable is the plan, thresholds, and rollback logic.

---

## Debrief (5-10 minutes)

Ask the room:

1. Would your table ship v2.0 or not?
2. What was the strongest argument on the opposite side?
3. What is the first production signal you would watch after launch?

Map answers back to controls:

- speed vs quality trade-off -> explicit release gate policy
- uncertainty across machines -> canary rollout and monitoring
- production risk -> rollback thresholds and shift-right alerts

---

## Optional Deep Dive

If a group finishes early:

1. Ask them to design a formal Release Advisory Board checklist
2. Ask them to define separate Ship, Ship-with-Warnings, and No-Ship criteria
3. Ask them to draft a 24-hour post-release monitoring dashboard

