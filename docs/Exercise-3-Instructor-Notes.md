# Exercise 3: Lab - Audit & Extend the Evaluation Framework - Instructor Notes

---

## Overview

Students inherit an automated evaluation framework and audit it to find bugs: **false positives** (test fails when bot answer is correct) and **false negatives** (test passes when bot answer is poor). They then use **GitHub Copilot** to rapidly generate and integrate a new evaluation metric to catch the gaps they identified.

**Key Learning Objective:** 
1. Evaluation metrics are imperfect and must be audited continuously.
2. Modern AI tools (Copilot) allow QA testers to rapidly prototype sophisticated metrics without deep coding skills.
3. The real skill is **test strategy design**, not code-writing—pick the right metric for your constraints (speed, cost, accuracy).

**Copilot Focus:**
- Students learn that they don't need to be senior engineers to add semantic checks, structure validators, or LLM-based judges.
- Different students' Copilot prompts may generate different code—compare and discuss trade-offs.

---

## Setup Checklist (10 minutes before class)

- [ ] Flask app running: `python launch.py` -> choose option 4 (Start Flask Application).
- [ ] Terminal ready in repo root for optional verification of one targeted case.
- [ ] Have [regression_testing/regression_testing.py](../regression_testing/regression_testing.py) open for reference.
- [ ] Have [tests/evaluation_framework.py](../tests/evaluation_framework.py) open—students will add code here.
- [ ] GitHub Copilot enabled in each student's Codespace (confirm before class).
- [ ] Pre-run the regression suite yourself to identify which tests fail and why. Share the output snapshot with students.
- [ ] Familiarize yourself with the four Copilot prompt options in Part B (JSON Validator, PII Detector, Professionalism, Citation Checker).

---

## Timing

| Phase | Time | Notes |
|-|-|-|
| Introduction & Scenario (5 minutes) | 5 minutes | "You inherited broken tests—audit them and fix one." Emphasize false positive/negative definitions. |
| Part A: Audit the Auditors (students work) | 12-15 minutes | Prefer instructor-provided regression output snapshot to avoid setup drag. |
| Part B: Copilot Metric Generation (students work + share) | 18-20 minutes | Each student picks one metric, integrates a small change, and runs one targeted check. |
| Part C: Document & Wrap-Up (students work) | 5-7 minutes | Submit findings and one trade-off. |
| **Total** | **40-45 minutes** | Timed version prioritizes audit quality over full-suite implementation. |

## Time-box guidance

1. Pre-run the regression suite before class and distribute the output snapshot.
2. Require one false positive and one false negative only.
3. Steer most students to the simpler deterministic metrics first.
4. Skip full-suite reruns during class unless a student finishes early.

---

## Expected Findings & Known Gaps

### Regression Suite Baseline

Running `python -m regression_testing.regression_testing --quick` should show:

**Likely to PASS:**
- `factual_simple` - straightforward query about GenAI testing, clear knowledge base answer.
- `reasoning_multi_step` - multi-step reasoning, good citation in response.

**Likely to FAIL or WARN (False Positives):**
- `hallucination_basic` - The query is "What AI safety practices..."; the chatbot may paraphrase from "GenAI Testing Guide" in a way that scores low on semantic similarity (0.62-0.70 vs. threshold 0.75). **This is a FALSE POSITIVE—the answer is correct, just different wording.**
- `adversarial_jailbreak_attempt` - The query tries to trick the chatbot into ignoring the knowledge base. The chatbot correctly refuses, but the refusal text doesn't match the golden expected answer exactly. **Current framework misses "refusal detection."**

**Likely to PASS but be Poor (False Negatives):**
- `noise_contradictory_prompt` - Contradictory query ("best practices that are bad"). The chatbot may output something technically correct but unhelpful. **Semantic similarity won't detect "semantically correct but useless."**

### Why Copilot Metrics Help

The current framework (deterministic checks: regex, length limits, keyword matching) has blind spots:

| Gap | Copilot Metric Solution | Why It Works |
|-----|------------------------|----|
| Can't validate structured output (JSON) | JSON Validator (Option A) | Catches malformed data that passes semantic checks. |
| No security gate for PII leaks | PII Detector (Option B) | Fails gracefully; prevents accidents. |
| Can't grade tone/professionalism | Professionalism Grader (Option C, LLM-as-Judge) | Sophisticated judgment without manual review. |
| Claims not attributed to sources | Citation Checker (Option D) | Deterministic but requires some linguistic sophistication. |

**Students will realize:** "I didn't write these functions from scratch; Copilot did. My value is picking the right metric for my constraints (speed, cost, accuracy) and verifying it works."

---

## Facilitation Tips

### Part A: Helping Students Audit

**If a student is stuck:**
- Q: "Look at that failing test. Is the chatbot's answer actually wrong, or just worded differently?"
- Q: "What metric caught this failure? A regex? Semantic similarity? Which one?"
- Q: "Would a human QA engineer agree this is a failure, or would they say the bot succeeded?"

**Framing:**
- "You're not debugging the bot. You're debugging the test itself."
- "Auditing the auditors is harder than auditing the software. Good news: you're learning a production superpower."

**Common misreading:**
- Students may assume all test failures are real bugs. Reframe: "Your job is to audit whether the test itself is valid. Is the metric right, or is the metric wrong?"

---

### Part B: Copilot Metric Generation - Facilitation

**This is the key differentiator from old Exercise 3. Students are not writing code; they're strategically using AI.**

**Step 1: Choosing a Metric**

Help students pick based on their audit findings:

- **If they found false positives from exact string matching:** → Citation Checker or PII Detector (add deterministic checks that complement semantic similarity).
- **If they found vague answers passing:** → Professionalism Grader or JSON Validator (add structure or tone checks).
- **If they found no obvious gaps:** → Suggest Citation Checker (universally useful for safety/transparency).

**Step 2: Using Copilot Chat**

**If students are unfamiliar with Copilot Chat:**
- Walk through: Ctrl+Shift+I (open Copilot Chat), type the prompt, copy the code.
- Emphasize: "The prompt is your job. Copilot's job is to write code. Your job is to pick good prompts."

**Troubleshooting:**
- If Copilot generates code that doesn't run: "Good. Now debug it. Change the import, fix the function call. You're learning."
- If Copilot generates overly complex code: "Simpler is better. Ask Copilot to simplify it."
- If different students get different code for the same prompt: "Exactly! Copilot is probabilistic. Pick the one you like best."

**Example Guidance:**

"Your audit found that the framework doesn't catch refusals. Here's a prompt: 
> 'Write a regex function that detects if the response contains common refusal phrases like I don't have information, beyond my knowledge base, or I cannot help with that. Return True if the response is a refusal, False otherwise.'

Now open Copilot Chat and paste that."

**Step 3: Integration**

Students need to:
1. Copy the function into [tests/evaluation_framework.py](../tests/evaluation_framework.py)
2. Wire it into a test (show the example in Part B of the exercise)
3. Run one targeted check before attempting a full rerun

**If integration breaks:**
- Q: "What's the error? Does it look like a syntax error or a logic error?"
- Q: "Did you import the function into your test file?"
- Tip: "Add a print statement to debug what the function is returning."

**Step 4: Show & Tell**

Turn laptops to face neighbors. Each pair shows:
1. The metric they added (Option A/B/C/D)
2. The Copilot prompt they used
3. Any tweaks they made to Copilot's code
4. Whether it caught the bugs they identified in Part A

**Group Discussion Question:**
- "Did Copilot's code work perfectly, or did you have to fix it? What does that tell you about AI-generated code?"
- "Did different metrics catch different bugs?"
- "For production use, which metric would you pick, and why?"

### Part C: Re-running Tests & Wrap-Up

**Expected outcomes:**
- Most students should complete the audit and produce one working or near-working metric prototype.
- Some students will still hit syntax or integration errors; that is acceptable in the timed version.
- Students who finish early can attempt a full rerun or a second metric.

**Validation Questions:**
- "Did your metric behave the way you expected on the targeted case?"
- "Did your new metric create any false positives? How do you know?"
- "Would you keep this metric in production? Why or why not?"

---

## Rubric (0-3 per section, total 0-9)

### Part A: Audit (0-3 points)

- **0:** Worksheet not completed or no tests run.
- **1:** Worksheet has entries but false positive/negative not clearly identified.
- **2:** At least one false positive AND one false negative identified with examples.
- **3:** Comprehensive audit with multiple findings and clear categorization (e.g., "Metric A causes false positives; Metric B misses edge cases").

### Part B: Copilot Metric & Integration (0-3 points)

- **0:** No metric generated or integration not attempted.
- **1:** Metric generated by Copilot but has syntax errors or doesn't integrate.
- **2:** Metric works; integrated into test suite; student can explain what it does.
- **3:** Metric works; integration clean; student can explain why this metric was chosen and how it addresses audit findings.

### Part C: Testing & Reflection (0-3 points)

- **0:** No re-run or reflection.
- **1:** Tests re-run; minimal reflection (e.g., "2 tests now pass").
- **2:** Tests re-run; before/after impact documented; student proposes one improvement.
- **3:** Tests re-run; clear before/after; student reflects on Copilot code quality and proposes production next steps.

**Total: 9 points (scale to 0-10 by granting 1pt for completion)**

**Grading Notes:**
- A student who completes a solid audit (Part A) + generates a working metric (Part B) but doesn't finish Part C -> 5-6/9 (solid pass).
- A student whose Copilot metric introduces more false positives than it fixes -> "Great debugging exercise! Now adjust the metric." Still credit the thinking.
- A student who asks clarifying questions and refines Copilot's code -> Bonus engagement point.

---

## Transition & Bridge Language

### Opening (Connect to Exercise 2)

*"In Exercise 2, you designed golden records—the 'right answers.' Today, we flip it: How do we **automatically grade multiple answers at scale?** And critically: How do we know our test automation itself is correct? You'll audit the framework, find bugs in the metrics themselves, and use Copilot to add a sophisticated new check."*

### Mid-Exercise (Part A -> Part B)

*"Now that you've mapped what's failing, you have data. You know which metrics are weak. Next, you propose a fix. Here's the modern way: You don't hand-code the solution. You use Copilot to generate a strong candidate, verify it works, and ship it. This is how production teams move fast."*

### Closing (to next section)

*"Evaluation metrics are like any other software subsystem: they have bugs, they evolve, and they need to be maintained. But notice: You didn't need a PhD in machine learning to add semantic checks or professionalism graders. Copilot let you focus on **test strategy**, not plumbing. In Exercise 4, we'll scale this: How do you monitor these metrics in production when users are sending queries you've never seen?"*

---

## Common Student Mistakes & Corrections

| Mistake | What You Hear | Correction |
|-|-|-|
| Confuses test failure with bot failure | "The bot is hallucinating." | "The metric flagged it. But is the metric right? Re-read the response. Metric bug or bot bug?" |
| Assumes Copilot code is perfect | "Copilot generated this, so it must work." | "Great start! Now test it. Fix any syntax errors. You're not accepting generated code; you're validating it." |
| Picks a metric they don't understand | "I chose JSON Validator because... umm..." | "Can you explain what it does? Why does it solve one of your audit findings? Pick based on strategy, not randomness." |
| Doesn't actually re-run tests | "I think my metric will work." | "Let's test it. Run the suite and show me the results. Data > intuition." |
| Misinterprets Copilot output | Code that's overly complex or wrong | "That's okay. Copilot is probabilistic. Simplify the prompt or try again. Or debug the code yourself." |
| Adds a metric that breaks production | New metric causes 20 tests to fail | "Excellent discovery! Your metric is too strict. Adjust it—is the threshold right? Does it need tuning?" |

---

## Answers to Anticipated Questions

**Q: Why would I use Copilot instead of writing the code myself?**
A: Speed. You focus on **what to check**, not **how to check it**. In production, you iterate on metrics weekly. Copilot shaves hours off that cycle.

**Q: Can I trust Copilot's code for production?**
A: Verify and validate. Copilot's code is a starting point. You test it, debug it, and own the result. That's true for any external code.

**Q: What if Copilot generates overly complex code?**
A: Refine your prompt. Say: "Write a simple regex-based function..." or "Simplify this code." Or debug the code yourself—that's good engineering practice.

**Q: Why do different students get different Copilot outputs for the same prompt?**
A: Copilot uses a language model with temperature/randomness. Slight variations are normal. Pick the best output and iterate.

**Q: Can I use Copilot in production?**
A: For **code generation**, yes (with review). For **runtime decision-making**, only if you're comfortable with non-determinism and third-party dependence.

---

## Debrief (5-10 minutes)

### Share-Out Structure

1. **Ask 2-3 volunteers:** "What metric did you add, and did it catch the bugs you found in Part A?"
2. **Highlight:**
   - "Notice: No two people generated identical code, but they all solved the problem."
   - "Notice: Choosing the *right* metric matters more than perfect code."
3. **Bridge:** "You've now audited and improved an evaluation framework. This is a real production skill. Teams do this every sprint."

---

## Optional Deep Dive (If Finishing Early)

If a group finishes early:

1. **Challenge:** "Add a second metric that contradicts your first one. How would you resolve the conflict?"
2. **Challenge:** "Design a metric that detects when the chatbot is too verbose (>500 tokens). How would you implement it with Copilot?"
3. **Code Exploration:** Have them add their rule to [regression_testing/regression_testing.py](../regression_testing/regression_testing.py) directly and discuss how this would integrate into CI/CD.
4. **Copilot Deep Dive:** "Try a different prompt for the same metric. Did Copilot generate different code? Which is better?"

---

## Pre-Class Prep for You

- [ ] Skim [regression_testing/regression_testing.py](../regression_testing/regression_testing.py) to understand the structure.
- [ ] Run `python -m regression_testing.regression_testing --quick` yourself and note which tests fail.
- [ ] Familiarize yourself with [tests/evaluation_framework.py](../tests/evaluation_framework.py)—understand how functions are defined and called.
- [ ] **Test Copilot Chat in a Codespace.** Try one of the four prompts yourself (Option A, B, C, or D) and verify you can copy the output into the framework. Note any tweaks needed.
- [ ] Prepare a 2-minute demo: Open Copilot Chat, ask for a metric, integrate it, re-run tests, show the impact. This gives students confidence.
- [ ] Prepare answers to "Anticipated Questions" above.
- [ ] Have [Exercise-3.md](Exercise-3.md) open to guide students through prompts.
