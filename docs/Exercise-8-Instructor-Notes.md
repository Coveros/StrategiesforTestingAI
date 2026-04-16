# Exercise 8: Lab - Red Teaming - Instructor Notes

---

## Overview

Students perform a structured **bug bounty** against the assistant's safety, retrieval, and fairness guardrails. The core goal is to test whether different attack styles can get the assistant to break its rules and then identify where the protection failed.

**Key Learning Objective:** Students should learn to classify red-team failures across:

1. Direct prompt injection
2. Roleplay or jailbreak attacks
3. Retrieval poisoning or obfuscation
4. Language-switching attacks
5. Fairness and bias attacks using counterfactual swaps

This lab ends with a table-wide reveal where students compare attack outcomes and determine whether the **Input Filter** or **Output Filter** failed.

---

## Setup Checklist (10 minutes before class)

- [ ] Confirm students can access traces or other useful safety telemetry
- [ ] Remind students to keep attacks inside the training environment only
- [ ] Explain the five attack vectors before testing begins
- [ ] Ensure each table can assign one person per vector if possible
- [ ] Clarify the meaning of "captured the flag": a meaningful guardrail failure or bypass
- [ ] Have the student-facing lab open: [docs/Exercise-8.md](Exercise-8.md)

---

## Timing

| Phase | Time | Notes |
|---|---|---|
| Intro and threat framing | 5 minutes | Explain bug-bounty mindset and capture-the-flag concept |
| Part 1: Multi-pronged attack | 18-22 minutes | Each person runs one primary attack vector attempt |
| Part 2: The reveal | 10-15 minutes | Share strongest prompts and identify failed filters |
| Debrief | 5 minutes | Discuss the most dangerous attack path |
| **Total** | **40-50 minutes** | - |

---

## Time-box Guidance

- Require one primary attack attempt per person.
- Allow a second attempt only if the room is moving quickly.
- Keep the reveal focused on strongest prompt, capture/no-capture, and failed layer.

---

## Expected Findings by Attack Vector

### Person 1: Direct Prompt Injection

Common outcomes:

- Basic direct attacks are often blocked
- Some systems still leak policy weakness through partial compliance or soft refusals

What strong evidence looks like:

- Exact injection prompt
- Clear judgment on whether the assistant resisted or partially yielded

### Person 2: Roleplay / Jailbreak

Common outcomes:

- Roleplay framing is often more effective than direct attacks
- "Grandma Exploit"-style prompts may weaken naive guardrails

What strong evidence looks like:

- Prompt framing that changed the assistant's behavior
- Evidence that roleplay caused more leakage than a direct request would have

### Person 3: Retrieval Poisoning / Obfuscation

Common outcomes:

- Obfuscated or manipulated prompts can bypass shallow checks
- If retrieval poisoning is possible, trusted context may be exploited

What strong evidence looks like:

- Proof that the assistant trusted bad context or failed to decode malicious intent correctly

### Person 4: Language Switching

Common outcomes:

- Safety behavior may weaken in non-English prompts
- Mixed-language prompts sometimes bypass stricter English-only protections

What strong evidence looks like:

- Same intent tested in English vs non-English with different outcomes
- Clear evidence of weakened refusal or filtering

### Person 5: Fairness / Bias

Common outcomes:

- Subtle differences in tone, helpfulness, or assumptions across demographic swaps
- Bias may appear even when explicit safety failures do not

What strong evidence looks like:

- A prompt pair differing only by demographic variable
- Clear comparison of how the responses differ in quality or assumptions

---

## Facilitation Tips

### While Students Attack Independently

Keep them focused on controlled evidence-gathering:

- "What exact rule were you trying to break?"
- "Did the assistant fully fail, partially fail, or resist correctly?"
- "Would you classify this as an input-filter failure or an output-filter failure?"

### During the Reveal

Push the table to be precise:

- Require each person to present one strongest prompt
- Require a yes/no judgment on whether they captured the flag
- Require a filter-layer diagnosis, not just "it failed"

### For Fairness Cases

Do not let students rely on vague impressions:

- Ask: "What changed between the prompts?"
- Ask: "What specifically changed in the output?"
- Ask: "Would a user from the swapped demographic receive worse treatment?"

---

## Rubric (0-2 per dimension)

### Attack Coverage Quality (0-2)

- **0:** Few or incomplete attack attempts
- **1:** One attack per vector attempted, but weakly documented
- **2:** Strong coverage with concrete prompts and outcomes

### Evidence Quality (0-2)

- **0:** Claims without transcript or trace evidence
- **1:** Some evidence captured, but interpretation is weak
- **2:** Clear evidence showing why an attack failed or succeeded

### Filter Failure Analysis (0-2)

- **0:** No clear input/output filter reasoning
- **1:** Partial reasoning, but unclear layer attribution
- **2:** Clear diagnosis of whether the Input Filter or Output Filter failed

### Guardrail Recommendation Quality (0-2)

- **0:** Generic fixes only
- **1:** Some relevant fixes but weak prioritization
- **2:** Specific guardrail improvements tied directly to observed attacks

**Total: 8 points**

---

## Strong Mitigations to Reward

If students propose these, reward strongly:

1. Input classifiers for prompt injection and jailbreak framing
2. Better multilingual safety checks and parity testing across languages
3. Retrieval trust checks or source-validation controls
4. Stronger output filtering for unsafe content that slips through
5. Counterfactual fairness regression tests in CI
6. Logging and review workflows for captured red-team failures

---

## Transition and Bridge Language

### Opening (Connect to Exercise 7)

"In Exercise 7, you stress-tested reliability under bad system conditions. In this lab, the attacker is the user. The question is not whether the system survives load, but whether it survives manipulation."

### Mid-Lab Framing

"A direct attack is not the only threat. Often the real weakness appears when the same malicious intent is wrapped in roleplay, translation, or obfuscation."

### Closing (to next stage)

"You just red-teamed the assistant manually. The next step is to operationalize this into recurring attack suites so regressions are caught continuously."

---

## Common Student Mistakes and Corrections

| Mistake | What You Hear | Correction |
|---|---|---|
| Assumes blocked direct prompt means system is safe | "It blocked the first prompt, so we're good" | "Try indirect, roleplay, or multilingual variants before concluding that." |
| Treats partial compliance as safe | "It refused at the end" | "Did it still leak unsafe detail before refusing? Partial leakage still counts." |
| Confuses fairness drift with harmless variation | "The tone was just a little different" | "Would that difference matter to a real user? If yes, it matters." |
| Blames the wrong layer | "The system failed" | "Did it fail to screen the prompt, or fail to block the output after processing it?" |
| Uses weak evidence | "I think it was biased" | "Show the exact counterfactual pair and the concrete difference." |

---

## Answers to Anticipated Questions

**Q: What if no one captures the flag?**  
A: That is still a valid outcome. Students should document which attacks were resisted and what evidence shows the guardrails held.

**Q: What if an attack partially succeeds?**  
A: Count partial compliance or leakage as meaningful evidence. Students should describe exactly what broke.

**Q: What if retrieval poisoning is not available in this environment?**  
A: Have that student focus on obfuscation instead. The point is to test how hidden malicious intent or misleading context affects behavior.

**Q: Should students fix prompts or code during this lab?**  
A: Not required. The main goal is adversarial diagnosis plus one recommended guardrail improvement.

---

## Debrief (5-10 minutes)

Ask the room:

1. Which attack vector was most successful today?
2. Which protection layer failed more often: Input Filter or Output Filter?
3. What one guardrail would you strengthen first?

Map answers back to controls:

- prompt injection -> input risk classifiers and stricter policy routing
- jailbreak framing -> roleplay-aware safety checks
- retrieval/obfuscation -> trust controls and decoding-aware filtering
- language-switching -> multilingual parity checks
- fairness/bias -> counterfactual regression testing and thresholds

---

## Optional Deep Dive

If a group finishes early:

1. Ask them to chain two attack vectors into one prompt
2. Ask them to design a weekly red-team regression pack with five prompts
3. Ask them to rank the five attack vectors by production risk

