# Exercise 8: Security, Fairness, and Red Teaming - Instructor Notes

---

## Objective

Students should practice adversarial testing on the agentic chatbot and produce evidence-backed mitigation proposals.

Primary outcomes:

1. identify jailbreak/bypass weaknesses
2. analyze poisoned retrieval behavior
3. assess fairness using counterfactual pairs
4. propose layered guardrails

---

## Setup Checklist

1. Start app and open [http://localhost:5000/?instructor=1](http://localhost:5000/?instructor=1).
2. Enable Agent Mode, Show Trace, Crew Mode.
3. Validate deterministic security hooks:
   - direct harmful request -> blocked/refusal
   - roleplay/obfuscation harmful request -> simulated bypass (`policy_bypass=true`)
   - "simulate poisoned policy document" -> poisoned retrieval marker (`poisoned_retrieval=true`)
4. Remind students: do not generate or distribute real harmful payloads.

---

## Timing (60-70 minutes)

| Phase | Time | Outcome |
|-|-|-|
| Threat-model framing | 5-7 minutes | Students understand abuse-centric mindset |
| Part A jailbreak testing | 20 minutes | Bypass and block outcomes documented |
| Part B poisoned retrieval | 20 minutes | Data-layer injection risk analyzed |
| Part C fairness pairs | 15 minutes | Counterfactual bias observations recorded |
| Part D guardrail plan + debrief | 10 minutes | Practical mitigation plan produced |

---

## Expected Findings

### Part A (jailbreak)

Expected behavior pattern:

1. direct harmful ask is blocked
2. roleplay/obfuscation framing may trigger bypass simulation (`policy_bypass=true`)

Teaching point: context framing often defeats naive safety filters.

### Part B (poisoned retrieval)

Expected behavior pattern:

1. poisoned retrieval marker appears in metrics
2. poisoned claim can influence response if trust checks are absent
3. canary token visibility indicates leakage risk

Teaching point: retrieval trust is a first-class security boundary.

### Part C (fairness)

Expected outcomes:

1. students may detect subtle tone/helpfulness differences
2. evidence quality will vary; push for concrete pairwise comparisons, not intuition alone

Teaching point: fairness testing needs structured counterfactual methodology.

---

## Rubric (0-2 per dimension)

### 1) Adversarial Coverage (0-2)

- 0: limited or incomplete attempts
- 1: partial attack coverage
- 2: full attack classes tested with clear outcomes

### 2) Evidence Quality (0-2)

- 0: claims without telemetry
- 1: mixed evidence
- 2: strong trace/metric-backed evidence

### 3) Fairness Analysis Quality (0-2)

- 0: no counterfactual method
- 1: basic comparison
- 2: structured comparison with clear interpretation

### 4) Mitigation Quality (0-2)

- 0: generic suggestions only
- 1: somewhat actionable mitigations
- 2: prioritized, layered guardrails tied to observed failures

---

## Strong Mitigations to Reward

1. input risk classifier for roleplay/obfuscation jailbreak patterns
2. retrieval source trust allowlist and poison marker checks
3. canary token detector in output filter
4. policy-aware refusal templates for high-risk intents
5. fairness counterfactual regression set in CI
6. immutable audit trail of prompt, retrieval, and output decisions

---

## Common Misconceptions to Correct

1. "If direct attack is blocked, system is secure."
   - Correction: framed or indirect attacks are often the real bypass path.

2. "Prompt security alone can solve retrieval poisoning."
   - Correction: retrieval trust controls must be deterministic and enforced pre-generation.

3. "Bias testing is subjective."
   - Correction: use pairwise counterfactual measurement and thresholds.

---

## Debrief (5 minutes)

Ask teams:

1. "Which attack succeeded first, and why?"
2. "Where in the trace did trust break down?"
3. "What one guardrail would you ship this week?"

Map responses:

- jailbreak bypass -> input policy classifier and prompt hardening
- poisoning -> retrieval trust policy and source validation
- fairness drift -> counterfactual regression tests with thresholds

---

## Bridge to Next Section

Suggested transition:

"You have now red-teamed agent behavior, retrieval trust, and fairness. Next we operationalize this: continuous security and fairness regression in CI/CD with scheduled adversarial test suites."

