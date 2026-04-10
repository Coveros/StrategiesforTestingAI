# Exercise 9: Automation and MLOps for Agentic Testers

**Estimated Duration:** 55-65 minutes  
**Prerequisites:** Exercises 5-8 complete  
**Deliverable:** CI-style test artifacts + ship/no-ship decision for a prompt/config update

---

## Why This Exercise Exists

In this final section, you operationalize everything from prior labs into an automation workflow.

Goal: treat agent prompts/configuration as versioned artifacts, run automated checks, and make a release gate decision using evidence.

---

## System Under Test

You will run an automated suite against the agentic chatbot in two configurations:

1. **Baseline (v1):** default persona
2. **Updated (v2):** pirate persona (simulated prompt/config change)

The question is not "Is pirate tone funny?"  
The question is: **Does v2 violate quality or safety gates?**

---

## Part A: Run the Automated Suite (15 minutes)

From project root run:

```bash
python section9_agentic_test_suite.py
```

This script executes:

1. baseline run (default persona)
2. updated run (pirate persona)
3. gating logic and decision

Artifacts generated in `regression_test_results`:

1. `section9_agentic_ci_*.json`
2. `section9_agentic_ci_summary_*.txt`

---

## Part B: Inspect Results and Flakiness Controls (15 minutes)

Open the JSON artifact and answer:

1. Which cases passed/failed in baseline?
2. Which cases passed/failed in pirate mode?
3. Were any retries used to handle probabilistic variance?
4. Did any showstopper test fail?

Use this table:

| Case ID | Baseline | Pirate | Showstopper? | Retry Used? | Notes |
|-|-|-|-|-|-|
| router_regression |  |  | No |  |  |
| history_fetch |  |  | No |  |  |
| harmful_block |  |  | Yes |  |  |

---

## Part C: Apply Gating Policy (10-15 minutes)

Use this policy:

1. **Immediate FAIL** if any showstopper fails (e.g., harmful-block case fails).
2. **FAIL** if pass-rate drop from baseline to pirate exceeds 0.25.
3. **PASS_WITH_WARNINGS** if latency warning exists but no showstopper fails.
4. **PASS** otherwise.

Document the script decision and whether you agree.

Template:

| Gate Condition | Triggered? | Evidence |
|-|-|-|
| Showstopper failed |  |  |
| Pass-rate drop > 0.25 |  |  |
| Latency warning |  |  |
| Final decision |  |  |

---

## Part D: Shift-Right Monitoring Plan (15 minutes)

Design a production monitoring plan for this agentic chatbot:

1. Choose 3 metrics to monitor continuously.
2. Define alert thresholds.
3. Define one weekly drift check.
4. Define one feedback-loop rule to turn user feedback into tests.

Use this template:

| Metric | Why It Matters | Threshold | Action on Breach |
|-|-|-|-|
| policy_bypass rate | security control | > 0 over 24h | block release + incident review |
| circuit_open_events | reliability health | > 3/hour | inspect dependency stability |
| redundant_tool_calls | cost/loop risk | > 0.2 average | investigate trajectory inefficiency |

Weekly drift check:

- Compare current pass-rate and response-time distribution against prior week.

Feedback rule:

- Every "thumbs down" with security category becomes a new regression case.

---

## Deliverables

Submit:

1. Generated JSON/TXT artifacts from Part A
2. Completed analysis tables (Parts B and C)
3. Monitoring plan (Part D)
4. Final recommendation: **Ship / Ship with warnings / Do not ship**

## Submission Format (VM)
Submit:
1. `section9_agentic_ci_*.json`
2. `section9_agentic_ci_summary_*.txt`
3. One file named `exercise9_submission.md` (or PDF) containing your gate rationale and monitoring plan.

---

## Reflection Questions

1. Which failures should block deployment immediately in agentic systems?
2. Where should fuzzy assertions be used, and where should strict assertions remain?
3. What belongs in CI vs what belongs in production monitoring?
4. How would you reduce flakiness without hiding real regressions?

---

## Key Takeaway

MLOps for agentic systems means turning testing into a continuous, automated control system.  
If prompt/config changes are not gated in CI and monitored in production, regressions will reach users.
