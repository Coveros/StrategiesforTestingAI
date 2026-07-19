# Instructor Facilitation Rubric (Exercises 1-9)

## Purpose
Use this one-page rubric to keep facilitation and scoring language consistent across all exercises. The intent is not strict grading precision; it is consistent evidence quality, risk reasoning, and actionable recommendations.

## Performance scale (use for all exercises)
| Level | Label | Meaning |
|---|---|---|
| 4 | Strong | Accurate findings, traceable evidence, clear prioritization, practical next-step fix. |
| 3 | Proficient | Mostly accurate findings, sufficient evidence, reasonable recommendation. |
| 2 | Developing | Partial findings, weak evidence chain, recommendation too generic or not testable. |
| 1 | Needs Support | Misclassified behavior, little evidence, no usable mitigation path. |

## Required evidence standard
A team output is complete only when all of the following are present:
1. Claim: what failed, degraded, drifted, or passed.
2. Evidence: concrete artifact from UI metadata, automation output, or trace observation.
3. Classification: defect type (quality, safety, trajectory, handoff, NFR, release gate).
4. Recommendation: smallest-blast-radius modification and one validation check.

## Scoring dimensions (apply to each team deliverable)
| Dimension | 4 (Strong) | 3 (Proficient) | 2 (Developing) | 1 (Needs Support) |
|---|---|---|---|---|
| Observation quality | Distinguishes signal vs noise and captures key behavior changes. | Captures key behavior, minor over/under interpretation. | Notes behavior but misses key distinctions. | Reports impressions only. |
| Evidence quality | Uses specific fields/artifacts and ties evidence directly to claim. | Evidence mostly supports claim. | Evidence is present but loosely connected. | Minimal or no supporting evidence. |
| Defect reasoning | Correctly identifies likely root cause category and impact. | Root cause category mostly correct. | Category uncertain or mixed incorrectly. | Root cause not identified. |
| Recommendation quality | Specific, low-risk, testable change + validation step. | Actionable change but validation is weak. | Generic suggestion without measurable outcome. | No actionable change. |

## Exercise-specific anchors

### Exercise 1 (Exploratory baseline)
Students should determine:
1. Variability exists and must be separated from correctness/safety risk.
2. At least one prompt reveals a meaningful quality risk.
3. A candidate automated check can be derived from exploratory findings.

Common misses to coach:
1. Treating wording variance alone as a defect.
2. Missing confident-but-wrong responses.

### Exercise 2 (Gold set expansion)
Students should determine:
1. New tests have clear intent, category, and acceptance logic.
2. Gold expectations are concept-based, not exact-string brittle.
3. Case additions improve coverage rather than duplicate existing intent.

Common misses to coach:
1. Overly strict expected text.
2. Weak rationale for why a new case matters.

### Exercise 3 (Metric audit)
Students should determine:
1. One false positive and one false negative with evidence.
2. Which metric/threshold behavior caused the misclassification.
3. A calibrated metric change and a before/after validation approach.

Common misses to coach:
1. Proposing metric changes without showing improved decision quality.
2. Ignoring category-specific threshold needs.

### Exercise 4 (Ask-mode trace and RAG isolation)
Students should determine:
1. Ask mode follows a linear retrieve-then-generate shape.
2. Retrieval vs generation failures are isolated correctly.
3. One improvement target is identified with measurable effect.

Common misses to coach:
1. Blaming generation for retrieval faults (or vice versa).
2. Using answer fluency as sole quality indicator.

### Exercise 5 (Single-agent trajectory and loops)
Students should determine:
1. Loop-like behavior is confirmed with trajectory evidence.
2. Degraded path is distinguished from safety-policy blocks.
3. One containment rule can reduce redundant steps/tool calls.

Common misses to coach:
1. Relying on final text only, ignoring trajectory fields.
2. No control run to compare behavior.

### Exercise 6 (Crew handoff integrity)
Students should determine:
1. Baseline handoff path is coherent.
2. Corrupted handoff state is observable and impacts retrieval quality/efficiency.
3. A specific handoff contract/integrity check is proposed.

Common misses to coach:
1. Interpreting shallow trace depth as the primary defect.
2. Not comparing crew-on vs crew-off control behavior.

### Exercise 7 (NFR reliability and overhead)
Students should determine:
1. Ask vs single-agent mode differences are quantified.
2. Weakest NFR area is identified with evidence.
3. One minimal remediation is prioritized.

Common misses to coach:
1. Drawing conclusions from single-run noise.
2. Conflating latency overhead with correctness failure.

### Exercise 8 (Red team classification)
Students should determine:
1. Failure types are classified correctly (guardrail, trajectory, handoff, drift, none).
2. Single-agent and crew path differences are interpreted correctly.
3. Highest-risk weakness has one targeted mitigation.

Common misses to coach:
1. Calling every issue a security bypass.
2. Skipping control runs and losing causal confidence.

### Exercise 9 (Release board decision)
Students should determine:
1. Gate status and pass-rate drop rules are applied in order.
2. Ship/No-Ship recommendation is evidence-led.
3. Mitigations and rollback triggers are explicit.

Common misses to coach:
1. Overriding FAIL without defensible risk treatment.
2. Treating PASS_WITH_WARNINGS as unconditional ship.

## Fast facilitation script (optional)
1. Ask: "What did you observe?"
2. Ask: "Which evidence proves it?"
3. Ask: "What class of failure is this?"
4. Ask: "What is the smallest safe modification?"
5. Ask: "What one check proves the fix worked?"

## Suggested weighting (if numeric scoring is needed)
| Dimension | Weight |
|---|---:|
| Observation quality | 25% |
| Evidence quality | 30% |
| Defect reasoning | 20% |
| Recommendation quality | 25% |

Use weights only if your cohort needs numeric rollups; otherwise use the 1-4 scale qualitatively.
