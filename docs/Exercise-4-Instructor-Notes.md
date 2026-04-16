# Exercise 4: Lab - Diagnosing RAG Failures with Root Cause Analysis - Instructor Notes

---

## Overview

Students investigate three production bugs and use the Trace UI to isolate root cause across the RAG pipeline. The central teaching goal is disciplined triage: identify whether each issue belongs to Retriever behavior (Data Engineering), Generator behavior (Prompt Engineering), or shared ownership.

**Learning Objective:** Train students to produce evidence-based bug diagnosis with clear ownership and verification criteria, rather than generic "the bot failed" reports.

---

## Setup Checklist (10 minutes before class)

- [ ] Start app: `python launch.py` -> option 4
- [ ] Verify chatbot is reachable at [http://localhost:5000](http://localhost:5000)
- [ ] Open Trace UI and confirm students can see retrieved sources and responses
- [ ] Run the three lab queries yourself before class:
  - `What are the key differences between black-box and white-box testing for GenAI?`
  - `According to the production best practices, what is the recommended batch size for processing GenAI evaluations?`
  - `Explain the concept of hallucination in the context of GenAI testing.`
- [ ] Keep these references open:
  - [app/rag_pipeline.py](../app/rag_pipeline.py)
  - [data/documents/](../data/documents/)

---

## Timing

| Phase | Time | Notes |
|---|---|---|
| Intro and triage framing | 5 minutes | Explain ownership model: Data Eng vs Prompt Eng vs Shared |
| Part A: Trigger and inspect | 10-15 minutes | Prefer pre-captured Trace evidence; reserve live reruns for spot checks |
| Part B: Case A diagnosis | 10-12 minutes | Context Precision (Bad Librarian) |
| Part C: Case B diagnosis | 10-12 minutes | Groundedness (The Liar) |
| Part D: Case C diagnosis | 10-12 minutes | Context Recall (Lazy Bot) |
| Part E: Bug report writing | 5-8 minutes | Actionable ticket-style reports |
| Debrief | 5-10 minutes | Compare triage choices and verification plans |
| **Total** | **45-60 minutes** | Intentional deep-dive lab |

---

## Time-box Guidance

- Pre-capture one example Trace for each case and distribute it before Part A starts.
- Do not require every student to regenerate every trace live.
- If the room is running long, shorten Part E to bullet-style bug reports only.

---

## Facilitation Tips - By Case

### Case A (Bad Librarian): Context Precision Failure

**Watch for:** low-relevance top sources, weak similarity patterns, source-topic mismatch.

**Socratic prompts:**
- "Are the top retrieved documents actually about the query intent?"
- "Which source should have ranked first, and why?"
- "If similarity is moderate, does that automatically mean relevance?"

**Instructor move:**
- Reinforce: this is a retrieval quality problem first.
- Route ownership: **Data Engineering** (unless evidence shows mixed failure).

### Case B (The Liar): Groundedness Failure

**Watch for:** retrieved docs are relevant but response includes unsupported specifics.

**Socratic prompts:**
- "Point to the exact sentence in context that supports this response claim."
- "Did the model add details not present in source text?"
- "If retrieval was good, what control failed next?"

**Instructor move:**
- Reinforce: this is a grounding/prompt control problem.
- Route ownership: **Prompt Engineering**.

### Case C (Lazy Bot): Context Recall / Lost-in-the-Middle

**Watch for:** answer exists in retrieved context but output is incomplete, vague, or refusal-like.

**Socratic prompts:**
- "Is evidence present but not used?"
- "Could context ordering or overload be hiding key facts?"
- "Would this be fixed by ranking/filtering, prompt changes, or both?"

**Instructor move:**
- Reinforce ambiguity: this often needs **shared ownership**.
- Ask for first experiment students would run to disambiguate.

---

## Rubric (0-2 per dimension)

### Case Diagnosis Quality (0-2 each, 3 cases = 6 points)

- **0:** Root cause not identified or unsupported.
- **1:** Root cause named but weak evidence or unclear ownership.
- **2:** Root cause clearly supported by Trace evidence with correct ownership.

### Bug Report Quality (0-2 points)

- **0:** Incomplete or vague report.
- **1:** Structured report with partial actionability.
- **2:** Complete, actionable report with clear acceptance criteria.

**Total: 8 points** (scale as needed).

---

## Common Student Mistakes and Corrections

| Mistake | Typical student statement | Instructor correction |
|---|---|---|
| Blames LLM first | "The model hallucinated" | "Show retrieval evidence first. Was context correct?" |
| Confuses similarity with relevance | "72% means wrong" | "Similarity is a signal, not proof of usefulness." |
| Skips Trace details | "I think it's broken" | "Point to specific source/response mismatch in Trace." |
| Proposes broad fixes without measurement | "Lower threshold a lot" | "What metric or before/after check validates improvement?" |
| Ignores context limits | "Just add more docs" | "More context can reduce recall if ordering/noise worsens." |

---

## Transition and Bridge Language

### Opening (Connect to Exercise 3)

"In Exercise 3, you upgraded how we evaluate responses. In this lab, we shift from score quality to failure diagnosis: when production breaks, where exactly in the RAG pipeline did it fail?"

### Mid-Exercise (Case A to Case B)

"You just diagnosed retriever quality. Now assume retrieval is good and test the next hypothesis: did generation stay grounded, or did it invent unsupported details?"

### Closing (to Exercise 5)

"You manually triaged three failures with evidence. The next step is operational scale: build automated checks for Context Precision, Groundedness, and Context Recall so failures are detected and routed continuously."

---

## Answers to Anticipated Questions

**Q: What if a case looks like both retriever and generator failed?**  
A: Mark it as shared ownership, then propose the first isolating experiment (for example: improve ranking first, rerun, and verify whether groundedness still fails).

**Q: Should students fix code during this lab?**  
A: Not required. The primary objective is diagnosis quality and ownership clarity. Optional code-level remediation can be treated as stretch work.

**Q: Can similarity score alone determine correctness?**  
A: No. Similarity is a signal, not a verdict. Students must pair similarity with source relevance and claim-level grounding checks.

**Q: How strict should grading be on ownership?**  
A: Reward evidence quality first. If ownership is debatable but well-justified from Trace evidence, score strongly.

---

## Debrief Prompts (5 minutes)

- Which case was hardest to assign ownership, and why?
- What was your strongest piece of Trace evidence in any case?
- What fix would you deploy first, and how would you verify it worked?

Tie-off message:

"You just performed manual root-cause triage. Next, we automate this process so failures are detected and routed continuously."

---

## Pre-Class Prep for Instructors

- [ ] Capture one example Trace for each failure mode
- [ ] Prepare one model bug report to show quality expectations
- [ ] Validate that students can access Trace UI before starting the lab
- [ ] Review [app/rag_pipeline.py](../app/rag_pipeline.py) so you can answer ownership questions

---

## Optional Stretch Activities

1. Ask students to design a fourth failure query and diagnose it.
2. Have students propose one pipeline change in [app/rag_pipeline.py](../app/rag_pipeline.py) to reduce one failure mode.
3. Ask students to define one measurable acceptance metric per case (e.g., groundedness pass rate).
