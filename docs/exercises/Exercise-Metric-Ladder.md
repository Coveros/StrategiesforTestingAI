# Exercise Metric Ladder: Retrieval + Generation Quality

## Why this exists

Use this page to progressively introduce quality evaluation across Exercises 1-9.

- Phoenix shows runtime behavior: latency, spans, tool loops, handoffs.
- Evaluation scoring shows output quality: retrieval relevance, grounding, answer quality, safety.
- Release decisions should combine both.

## Scoring model used in class

Track two lanes in each exercise run:

1. System lane (Phoenix)
- Trace shape correctness
- Tool call count and retries
- Latency (avg and p95)
- Handoff integrity (agentic exercises)

2. Quality lane (evaluation harness)
- Retrieval quality (Hit@k, Precision@k, Recall@k)
- Generation quality (Faithfulness, Relevance, Completeness)
- Risk quality (Hallucination rate, Safety refusal behavior)

## Exercise-by-exercise metric ladder

| Exercise | Primary teaching goal | Introduce these metrics | Suggested threshold for pass | Evidence to capture |
|---|---|---|---|---|
| 1 | Exploratory mindset on probabilistic systems | Manual rubric only: relevance, clarity, obvious hallucination | No hard gate yet; discussion-based pass | Prompt log + 1-2 examples of variable outputs |
| 2 | Goldens and expected behavior | Relevance score, Completeness score, Basic hallucination flag | Average relevance >= 0.70, completeness >= 0.65 | Golden test outputs and rubric notes |
| 3 | Formal evaluation and threshold tuning | Weighted quality score, false positive/false negative review, robustness pass rate | Weighted score >= 0.72 and robustness pass >= 0.80 | Evaluation report and tuned threshold rationale |
| 4 | Ask-mode observability + retrieval verification | Hit@3, Precision@3, avg similarity, faithfulness spot-check | Hit@3 >= 0.85, Precision@3 >= 0.70 | Phoenix linear trace (Chains -> Retriever -> LLM) + retrieval scorecard |
| 5 | Single-agent trajectory diagnostics | Tool-loop count, retry depth, answer faithfulness after loop attempts | No infinite loops; faithfulness >= 0.75 | Phoenix trajectory + post-run answer quality checks |
| 6 | Multi-agent handoff integrity | Handoff success rate, retrieval success by specialist, faithfulness per handoff | Handoff success >= 0.85, faithfulness >= 0.78 | Phoenix graph + specialist output rubric |
| 7 | Reliability and NFR under load | p95 latency, throughput, error rate, quality-on-load drift | p95 latency within target and quality drop <= 10% | Load run logs + Phoenix timing + quality deltas |
| 8 | Security and containment under adversarial prompts | Prompt injection resistance, refusal correctness, harmful output rate | Attack containment >= 0.90, harmful output rate <= 0.05 | Red-team prompts, outcomes, and trace evidence |
| 9 | Ship/no-ship governance | Combined gate: quality + reliability + security + trace evidence | All critical thresholds met; no critical regressions | Decision memo with explicit pass/fail per gate |

## Minimal metric definitions used in this course

- Hit@k: fraction of queries where at least one relevant chunk appears in top-k retrieval.
- Precision@k: relevant chunks in top-k divided by k.
- Recall@k: relevant chunks in top-k divided by all relevant chunks.
- Faithfulness: fraction of response claims supported by retrieved context.
- Relevance: how directly the response answers the user intent.
- Completeness: how many expected key points are covered.
- Hallucination rate: fraction of responses with unsupported factual claims.

## Recommended implementation in this repository

- Use the existing evaluator foundation in tests/evaluation_framework.py.
- Continue using regression gating in regression_testing/regression_testing.py.
- Keep Phoenix for diagnostics and root-cause analysis, not as the only quality signal.

## Instructor facilitation pattern (repeat each exercise)

1. Run prompt set for the exercise.
2. Score quality metrics (retrieval and/or generation).
3. Inspect Phoenix traces for causal diagnosis.
4. Apply remediation.
5. Re-run and compare before vs after.

## Suggested gate progression by course phase

- Early phase (Exercises 1-2): rubric-first, low-stakes thresholds.
- Mid phase (Exercises 3-6): introduce hard thresholds and failure analysis.
- Late phase (Exercises 7-9): enforce release-style gates across quality, reliability, and security.
