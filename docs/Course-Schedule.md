# Course Schedule and Timing Guide

---

## Purpose

This document gives instructors a practical pacing model for delivering Exercises 1-9 inside a **13-14 hour course** without cutting the core learning goals.

The key principle is simple:

- keep most exercises in the **30-45 minute** range
- allow a small number of deeper labs to run longer when evidence review is the point
- use pre-staged artifacts instead of live setup when setup friction teaches less than the analysis step

---

## Target Exercise Durations

| Exercise | Topic | Target Duration | Notes |
|---|---|---|---|
| Exercise 1 | Exploratory testing for GenAI | 35-45 minutes | Reduced prompt count and shorter determinism comparison |
| Exercise 2 | Golden test set + rubric audit | 35-45 minutes | Fewer active categories and only 2 cases reviewed live |
| Exercise 3 | Audit and extend evaluation framework | 40-45 minutes | Audit stays live; implementation becomes a targeted prototype |
| Exercise 4 | RAG root-cause analysis | 45-60 minutes | Intentional deep dive using pre-captured traces |
| Exercise 5 | Testing an agent | 45-50 minutes | One representative case per pillar |
| Exercise 6 | Testing multi-agent systems | 45-55 minutes | Intentional deep dive with one trajectory per person |
| Exercise 7 | Stress testing / NFRs | 40-50 minutes | One stress case per pillar and 3 baseline latency queries |
| Exercise 8 | Red teaming | 40-50 minutes | One primary attack per person |
| Exercise 9 | MLOps / release decision | 35-45 minutes | Review precomputed CI results instead of running the full suite live |

**Exercise-only total:** about **6.0 to 7.4 hours**

---

## Recommended Full-Course Agenda

This agenda assumes direct instruction, demos, debriefs, and short transitions in addition to the labs.

| Block | Activity | Time |
|---|---|---|
| Course kickoff | Setup, environment check, and framing | 30 minutes |
| Foundations | Intro to GenAI testing concepts | 25 minutes |
| Foundations | Exercise 1 | 40 minutes |
| Foundations | Debrief 1 | 10 minutes |
| Foundations | Golden records lecture/demo | 20 minutes |
| Foundations | Exercise 2 | 40 minutes |
| Foundations | Debrief 2 | 10 minutes |
| Foundations | Evaluation framework lecture/demo | 20 minutes |
| Foundations | Exercise 3 | 45 minutes |
| Foundations | Debrief 3 | 10 minutes |
| RAG diagnostics | RAG failure analysis lecture/demo | 20 minutes |
| RAG diagnostics | Exercise 4 | 50 minutes |
| RAG diagnostics | Debrief 4 | 10 minutes |
| Section transition | Bridge from RAG to agentic testing | 10 minutes |
| Agentic systems | Agent workflow testing lecture/demo | 20 minutes |
| Agentic systems | Exercise 5 | 50 minutes |
| Agentic systems | Debrief 5 | 10 minutes |
| Agentic systems | Multi-agent orchestration lecture/demo | 20 minutes |
| Agentic systems | Exercise 6 | 50 minutes |
| Agentic systems | Debrief 6 | 10 minutes |
| Operations | Reliability and NFR lecture/demo | 20 minutes |
| Operations | Exercise 7 | 45 minutes |
| Operations | Debrief 7 | 10 minutes |
| Operations | Trust, safety, and red teaming lecture/demo | 20 minutes |
| Operations | Exercise 8 | 45 minutes |
| Operations | Debrief 8 | 10 minutes |
| Operations | Release gating and MLOps lecture/demo | 20 minutes |
| Operations | Exercise 9 | 40 minutes |
| Operations | Course closeout and final synthesis | 20 minutes |
| Breaks | Three 20-minute breaks | 60 minutes |

**Recommended course total:** about **13.2 hours**

This leaves a small amount of flex time inside a 13-14 hour window for room questions or local setup delays.

---

## Where to Keep Labs Short

Use these compression rules consistently across the course:

1. Cut repeated attempts before cutting the core discussion.
2. Precompute traces or CI output when the setup step is not the learning goal.
3. Keep only one structured group synthesis moment per exercise.
4. Move stretch activities outside the required class window.
5. If time is slipping, shorten written formatting before shortening evidence review.

---

## Labs Allowed to Run Long

These are the two labs most worth protecting as deeper exercises:

1. **Exercise 4:** Students need enough time to inspect evidence and assign ownership correctly.
2. **Exercise 6:** Students need enough time to reason about trajectory waste, handoffs, and orchestrator behavior.

Exercise 5 can also run slightly long if you want to preserve all five testing pillars with meaningful discussion.

---

## Instructor Notes

If the class is running behind, do not cut the main reasoning task first. Use this order:

1. Skip optional stretch work
2. Use pre-staged artifacts instead of live reruns
3. Reduce writing polish or reporting detail
4. Reduce repeated examples or extra attempts
5. Only then cut core analysis scope