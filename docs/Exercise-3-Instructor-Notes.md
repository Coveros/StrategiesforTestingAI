# Exercise 3: Audit & Extend the Evaluation Framework - Instructor Notes

---

## Overview

Students audit the existing regression test framework to understand which metrics work and which fail. Then they propose a new evaluation rule (deterministic, semantic, or citation-based). This teaches the meta-skill of evaluating the evaluators - critical for production AI systems.

**Key Learning Objective:** Metrics are not oracles; they're designed artifacts with trade-offs. Small changes to thresholds or rules cause dramatic shifts in pass/fail rates.

---

## Setup Checklist (5 minutes before class)

- [ ] Flask app running: `python launch.py` -> choose option 4 (Start Flask Application).
- [ ] Terminal ready in repo root for students to run `python -m regression_testing.regression_testing --quick`.
- [ ] Have [regression_testing/regression_testing.py](../regression_testing/regression_testing.py) open for reference.
- [ ] Familiarize yourself with [tests/evaluation_framework.py](../tests/evaluation_framework.py) - students may ask what metrics are being used.
- [ ] Optional: Pre-run the regression suite yourself to identify which tests fail and why. Note the failures.

---

## Timing

| Phase | Time | Notes |
|-|-|-|
| Introduction & Key Concepts (5-7 minutes) | 5 minutes | Emphasize: "Auditing the auditors" and the three evaluation layers. |
| Part A: Explore & Map (students work) | 20-25 minutes | Circulate; help students identify false positives/negatives. |
| Part B: Propose Fix (students work) | 15-20 minutes | Students draft one approach. Expect variety - that is good. |
| Part C: Test & Document (students work) | 10 minutes | Quick re-run and impact analysis. |
| Debrief & Group Share (5 minutes) | 5 minutes | 2-3 students share findings. Bridge to regression testing in production. |
| **Total** | **45-55 minutes** | - |

---

## Expected Findings & Known Gaps

### Regression Suite Baseline

Running `python -m regression_testing.regression_testing --quick` should show:

**Likely to PASS:**
- `factual_simple` - straightforward query about GenAI testing, clear knowledge base answer.
- `reasoning_multi_step` - multi-step reasoning, good citation in response.

**Likely to FAIL or WARN:**
- `hallucination_basic` - The query is "What AI safety practices..."; the chatbot may paraphrase from "GenAI Testing Guide" in a way that scores low on semantic similarity (0.62-0.70 vs. threshold 0.75). **This is a FALSE POSITIVE.**
- `adversarial_jailbreak_attempt` - The query tries to trick the chatbot into ignoring the knowledge base. The chatbot may refuse appropriately, but the refusal text doesn't match the golden expected answer exactly. **Deterministic checks won't catch this without a refusal detector.**
- `noise_contradictory_prompt` - Contradictory query ("best practices that are bad"). The chatbot may output something technically correct but unhelpful. **Semantic similarity won't detect "semantically correct but useless."**

### Known Weaknesses to Guide Discussion

**If students identify these, affirm them:**

1. **Semantic Similarity False Positives (Most Common Finding)**
   - Issue: Threshold 0.75 is brittle. Small phrasing changes cause failures.
   - Student insight: "The chatbot's answer was right, just worded differently."
   - Suggested fix: Lower threshold to 0.70, or add a "response length vs. semantic score" heuristic.

2. **Missing Refusal Detection**
   - Issue: The framework doesn't explicitly check if the chatbot refuses out-of-scope queries.
   - Student insight: "For the jailbreak test, the chatbot said 'I don't have information,' but the metric didn't recognize it."
   - Suggested fix: Add a deterministic rule that flags "I don't have information" and "beyond my knowledge base" as valid refusals.

3. **Relevance ≠ Correctness**
   - Issue: A response can be factually correct (high semantic similarity to knowledge base) but irrelevant (doesn't answer the specific question).
   - Student insight: "The chatbot talked about best practices, but the question was about edge cases."
   - Suggested fix: Add a query-response alignment metric (embed both, measure cosine similarity).

4. **Citation Opacity**
   - Issue: The regression suite doesn't require explicit citations or source disclosure.
   - Student insight: "How do I know which document the answer came from?"
   - Suggested fix: Add a citation-requirement rule for safety-related topics.

### What Students Likely Won't Find (Acceptable Gaps)

- **Bias Detection:** The framework doesn't measure tone or demographic bias. That's fine for scope.
- **LLM-as-Judge:** No Cohere Classify endpoint is set up. Note that this is a next-level technique.
- **Inter-Rater Reliability:** No human baseline. Mention this is a production step, not an exercise step.

---

## Facilitation Tips

### Part A: Helping Students Map Failures

**If a student is stuck:**
- Q: "Look at that failing test. Is the chatbot's answer actually wrong, or just worded differently?"
- Q: "What metric caught this failure? Deterministic, Semantic, or LLM-as-Judge?"
- Q: "Would a human QA engineer agree this is a failure?"

**Common misreading:**
- Students may assume all test failures are real bugs. Reframe: "Your job is to audit whether the test itself is valid."

### Part B: Helping Students Choose an Approach

**If a student is paralyzed by choice:**
- Lean them toward **Option 1 (Deterministic Heuristic)** if they prefer concrete rules.
  - Easiest to implement; immediate impact.
  - Ask: "What's one obvious thing the framework should check for?"
- Lean them toward **Option 2 (Semantic Threshold)** if they want to debug the math.
  - More analytical; requires understanding cosine similarity.
  - Ask: "Does the current threshold miss real problems?"
- Lean them toward **Option 3 (Citation Rule)** if they care about Trust/Transparency.
  - Best for production storytelling; less code.
  - Ask: "Should the chatbot tell users where it's getting its information?"

**Closing thought:**
- "There's no single right answer. Different teams choose different tradeoffs. What matters is you justify your choice."

### Part C: Re-running Tests

**Expected issues:**
- Students may forget to activate the venv. Remind: `c:\Users\jpayne\Documents\Training\Notebooks for ML classes\training-env\Scripts\activate` (Windows).
- The regression suite may take 30-60 seconds to run (API calls to Cohere). That's normal.
- New rules may cause new test failures. Ask: "Is this a false positive from your rule, or a real problem?"

**Icebreaker:**
- If a student's rule causes 8 tests to fail when only 2 should fail, celebrate it: "Great! You found the threshold is too strict. Now adjust it."

---

## Rubric (0-2 per dimension)

### Part A: Analysis (0-2 points)

- **0:** Worksheet not completed or incompletable (no failed tests in the suite).
- **1:** Worksheet has some entries; false positive/negative not clearly identified.
- **2:** Worksheet complete; at least one false positive AND one false negative identified with justification.

### Part B: Proposal (0-2 points)

- **0:** No proposal or approach is incoherent.
- **1:** Proposal is clear but partial-pseudo-code sketched but not justified, or vice versa.
- **2:** Proposal is clear, justified, and implementable (code or detailed pseudo-code provided).

### Part C: Testing & Impact (0-2 points)

- **0:** No attempt to test or impact analysis not completed.
- **1:** Test run but impact analysis is shallow (e.g., "2 more tests passed" with no deeper insight).
- **2:** Tests re-run, impact quantified (count of tests changed), and student proposes a follow-up adjustment.

**Total: 6 points (can scale to 0-10 or 0-100 as you prefer)**

**Grading Ceiling Notes:**
- A student who completes Part A & B thoroughly but runs out of time on Part C -> 4/6 (solid pass).
- A student who writes a citation rule but it's brittle (5 new false positives) -> Encourage iteration, but still credit the thinking.

---

## Transition & Bridge Language

### Opening (Connect to Exercise 2)

*"In Exercise 2, you designed golden records-the 'right answers.' Today, we flip it: **How do we automatically grade multiple answers at scale?** You'll audit the framework and propose a fix."*

### Mid-Exercise (Part A -> Part B)

*"Now that you've mapped what's failing, you have data. You've identified the gaps. Next, you propose a rule to fix one of them. You're not writing perfect code-you're designing a heuristic that's good enough for production."*

### Closing (to Section 4)

*"Evaluation metrics are like any other software subsystem: they have bugs, they have trade-offs, and they need to be maintained. In Exercise 4, we'll look at how to use these metrics for continuous monitoring in production, where you're grading responses in real-time from users you've never seen before."*

---

## Common Student Mistakes & Corrections

| Mistake | What You Hear | Correction |
|-|-|-|
| Assumes all test failures = bugs | "The chatbot is hallucinating." | "The metric flagged it, but is the metric right? Re-read the response." |
| Proposes overly complex rule | "I'll build a multi-step classifier..." | "Start simpler. One regex rule is valid. Can you ship it in 5 minutes?" |
| Forgets to justify threshold change | "I changed 0.75 to 0.70." | "Why? How many tests flipped? Is the trade-off worth it?" |
| Doesn't actually re-run tests | "I propose this rule." | "Let's test it. Run the suite and tell me what changed." |
| Confuses precision & recall | "My rule caught more hallucinations." | "Great. But did it create false positives? Show me the before/after." |

---

## Answers to Anticipated Questions

**Q: Why is semantic similarity so noisy?**
A: Embedding models are trained on general internet text, not specialized GenAI safety documents. Paraphrasing can drop similarity by 0.1-0.2 points even when meaning is preserved.

**Q: Should we raise or lower the threshold?**
A: Neither is objectively right. Lowering it catches more hallucinations (higher recall) but flags correct paraphrases (lower precision). You pick based on your risk tolerance.

**Q: Can we use the same Cohere model to grade its own output?**
A: Yes, but it's expensive (2 API calls per response). It's also biased-the model may grade itself leniently. Good for research, risky for production.

**Q: What if my new rule is contradicted by existing tests?**
A: Perfect! That's a conflict of interest. You've discovered that two metrics disagree. Propose a tie-breaker rule.

---

## Debrief (5 minutes)

## Bridge to Next Section

**If time allows, tease next section:**

*"So you have a good metric and golden records. But production systems see 1,000 queries per day. You can't manually review every response. How do you automate monitoring and know when your model starts drifting? That's Exercise 4: Regression Testing in Production."*

---

## Optional Deep Dive (If Finishing Early)

If a group finishes early:

1. **Challenge:** "What if the knowledge base documents contradicted each other? Design a metric for that."
2. **Challenge:** "In production, you don't always have the golden answer. Design a reference-free metric."
3. **Code Exploration:** Have them add their rule to [regression_testing/regression_testing.py](../regression_testing/regression_testing.py) directly and propose a PR (simulate GitHub workflow).

---

## Pre-Class Prep for You

- [ ] Skim [regression_testing/regression_testing.py](../regression_testing/regression_testing.py) to understand the structure.
- [ ] Run `python -m regression_testing.regression_testing --quick` yourself and note which tests fail.
- [ ] Familiarize yourself with [tests/evaluation_framework.py](../tests/evaluation_framework.py)-it contains the metric definitions.
- [ ] If confident, prepare a 2-minute demo showing threshold adjustment (e.g., change 0.75 -> 0.70, re-run, show impact).
- [ ] Prepare answers to the "Anticipated Questions" section above.
