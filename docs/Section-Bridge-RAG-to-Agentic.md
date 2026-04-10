# Section Bridge: From RAG Testing to Agentic Testing

**Instructor-Delivered Framing Presentation**  
**Estimated Duration:** 5-10 minutes  
**Delivery:** After Exercise 4 debrief, before distributing Exercise 5

---

## Purpose

Students just spent Exercises 1-4 learning to test a RAG chatbot. This bridge reframes everything they learned and shows why it is necessary but not sufficient for agentic systems. It answers the question: *"Why can't I just use the same tests I already wrote?"*

---

## Slide 1 - What You Have Done (1 minute)

**Say:**

> "Let's take stock of what you've built over the last four exercises. You wrote golden-record test cases to evaluate answer quality. You audited those test cases to catch false positives and false negatives. You traced two-layer failures: when the retriever pulled the wrong document, versus when the generator hallucinated despite good retrieval. You can now tell the difference between 'the pipeline is broken' and 'the evaluation is broken.' That is a genuinely professional skill. Most teams can't do it."

**Slide content:**

```
Exercises 1-4: RAG Testing
─────────────────────────────────────────
✓ Golden records with pass/fail thresholds
✓ Evaluation audit (false positives + negatives)
✓ Two-layer decomposition (Retriever vs Generator)
✓ Automated regression with change detection
```

---

## Slide 2 - The Test Target So Far (1 minute)

**Say:**

> "Here's what we have been testing. A user sends a query. The retriever finds relevant documents. The generator reads those documents and produces a text response. That is it. One input, one output. We ask: 'Is this answer good?' Everything we measured - semantic similarity, pass/fail thresholds, regression deltas - is a judgment about the quality of that one output string."

**Slide content (diagram):**

```
User Query
   |
   v
 Retriever -> [relevant documents]
   |
   v
 Generator -> Answer (text)
   |
   v
Question we ask:
"Was the answer good?"
```

---

## Slide 3 - Now Meet an Agentic System (2 minutes)

**Say:**

> "An agentic system does not just produce one answer. It makes decisions. It calls tools. It maintains memory across turns. It may take actions that are hard or impossible to undo - filing a bug ticket, triggering a test suite, sending an alert. Look at this same diagram now."

**Slide content (diagram):**

```
User Request
    |
    v
  Agent -> Decides: Which tool? With what parameters?
    |
    |- search_kb(query)              [read-only]
    |- run_regression_suite(scope)   [expensive operation]
    |- get_test_history(test_id)     [read-only]
    '- create_bug_ticket(...)        [write action, hard to undo]
    |
    v
  Result + Updated State + Next Turn

Questions we now ask:
"Did it pick the RIGHT tool?"
"With the RIGHT parameters?"
"In the RIGHT order?"
"Without overstepping its authority?"
```

**Say:**

> "A fluent, well-written response can still be catastrophic if the agent files a P0 ticket with made-up evidence, or runs a full regression suite when the user just asked a general question. The output quality is no longer the only thing that matters."

---

## Slide 4 - The Critical Shift (1 minute)

**Say:**

> "Here is the single most important thing I want you to carry from this section into the next one."

**Slide content:**

```
RAG Testing                     Agentic Testing
────────────────────────────────────────────────
Output quality                  Decision correctness
"Was the answer good?"          "Was the choice right?"

Semantic similarity             Tool routing accuracy
BLEU / cosine scores            Hallucinated parameter detection

Deterministic pipeline          Multi-step, stateful behavior
One input -> one output          Sequences of decisions + actions

Bad answer = user misinformed   Bad action = data corrupted,
(recoverable)                   ticket misfiled, audit triggered
                                (potentially not recoverable)
```

---

## Slide 5 - What the Next Exercises Test (1 minute)

**Say:**

> "In Exercises 5 through 9 you will test each of these failure modes systematically. Exercise 5 is tool routing and state. Exercise 6 is multi-agent handoffs. Exercise 7 is non-functional behavior - timeouts, rate limits, weird inputs. Exercise 8 is security: prompt injection, guardrail evasion, least privilege. Exercise 9 ties it all together as a CI gate: can you automate a pass/fail decision before you deploy a new version? The skills transfer. You still write test cases. You still compare expected to actual. What changes is *what* you are comparing."

**Slide content:**

```
Exercise 5  ──  Tool routing + state integrity
Exercise 6  ──  Multi-agent handoffs + trajectory validation
Exercise 7  ──  NFR: timeouts, rate limits, robustness
Exercise 8  ──  Security: prompt injection + guardrails
Exercise 9  ──  CI gate: automated deploy/no-deploy decision
```

---

## Facilitation Notes

**If students ask "can't I just test the final output?":**

> "You can. But an agent that routes to the wrong tool and still produces a readable sentence is passing your output test and failing in production. You need to test the decision layer, not just the response layer."

**If students seem anxious about the complexity shift:**

> "The test case structure is almost identical - you still write inputs, expected behaviors, and observations. The vocabulary changes. 'Expected tool' replaces 'expected answer.' Take five minutes to read the opening of Exercise 5 before we start, and it will click."

**If time is short (under 5 minutes available):**

Skip Slides 2 and 3. Deliver Slides 1, 4, and 5 only. The table on Slide 4 is the minimum viable transition.

---

## Bridge to Exercise 5

Hand out Exercise 5 immediately after this framing. Do not take questions until students have had 2 minutes to read the "Why This Exercise Exists" section at the top - it reinforces what you just said in their own reading pace.
