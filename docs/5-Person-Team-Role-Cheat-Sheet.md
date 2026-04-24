# 5-Person Team Role Cheat Sheet

Use this page as a quick assignment guide during labs. Assign one person per role and keep each person's focus question visible during execution.

## Exercise 1: Exploratory Testing

| Person | Primary Pillar | Focus Question |
|---|---|---|
| Person 1 | Happy Path | Which parts are consistently useful across repeated runs? |
| Person 2 | Boundary | Did formatting noise change quality, or only wording style? |
| Person 3 | Negative | Did refusal behavior stay firm but still polite and helpful? |
| Person 4 | Determinism | Which response traits are stable enough for automation? |
| Person 5 | Heuristic Synthesis | Which deterministic checks reduce brittle exact-match failures? |

## Exercise 2: Golden Set and Rubric Audit

| Person | Primary Pillar | Focus Question |
|---|---|---|
| Person 1 | Factual Category | Is conceptual correctness graded clearly and measurably? |
| Person 2 | Reasoning Category | Does the rubric demand concrete reasoning output? |
| Person 3 | Boundary Risk Category | Are refusal and recovery behaviors explicitly testable? |
| Person 4 | Determinism Auditor | Could two graders independently agree on pass/fail? |
| Person 5 | Vote Recorder and Rewriter | Which rubric line caused disagreement and how was it fixed? |

## Exercise 3: Evaluation Framework Audit

| Person | Primary Pillar | Focus Question |
|---|---|---|
| Person 1 | False Positive Audit | Which failure is due to metric brittleness, not model quality? |
| Person 2 | False Negative Audit | Which weak response escaped because criteria were too loose? |
| Person 3 | Metric Prototype A | Does this metric close a real, observed gap? |
| Person 4 | Metric Prototype B | What precision or false-positive risk does this add? |
| Person 5 | Integration and Validation | Did one targeted check improve without obvious side effects? |

## Exercise 4: RAG Root Cause Diagnosis

| Person | Primary Pillar | Focus Question |
|---|---|---|
| Person 1 | Case A Lead (Precision) | Are top sources actually relevant to query intent? |
| Person 2 | Case A Evidence Recorder | What trace artifact best proves retrieval ranking failure? |
| Person 3 | Case B Lead (Groundedness) | Which response claim is unsupported by context evidence? |
| Person 4 | Case C Lead (Recall) | Did context contain the answer that the model missed? |
| Person 5 | Bug Report Synthesis | Which fix should ship first for production risk reduction? |

## Exercise 5: Agent Workflow QA

| Person | Primary Pillar | Focus Question |
|---|---|---|
| Person 1 | Tool Routing | Did wrong-tool selection still produce misleadingly plausible output? |
| Person 2 | Argument Extraction | Which malformed parameter caused highest downstream risk? |
| Person 3 | State Integrity | Did stale memory leak across turns or task resets? |
| Person 4 | Safety and Guardrails | Which refusal was robust versus easy to bypass? |
| Person 5 | Error Handling | Was failure communication transparent and operationally safe? |

## Exercise 6: Multi-Agent Trajectory Auditing

| Person | Primary Pillar | Focus Question |
|---|---|---|
| Person 1 | Trajectory Audit A | Which handoff step added no measurable value? |
| Person 2 | Trajectory Audit B | Where should the orchestrator have stopped earlier? |
| Person 3 | Trajectory Audit C | Which repeated action added no new evidence? |
| Person 4 | Trajectory Audit D | Which handoff dropped required context? |
| Person 5 | Trajectory Audit E | Which orchestrator choice created avoidable overhead? |

## Exercise 7: NFR Stress Testing

| Person | Primary Pillar | Focus Question |
|---|---|---|
| Person 1 | Outage and Rate Limits | Did degradation remain clear and user-safe under backpressure? |
| Person 2 | Timeouts | Was timeout handling bounded, safe, and understandable? |
| Person 3 | Boundary Inputs | Did extreme input stay stable without crash risk? |
| Person 4 | Gibberish and Fuzzing | Did fallback behavior avoid hallucinated actions? |
| Person 5 | Cost and Latency | Which outlier is the biggest production risk? |

## Exercise 8: Red Teaming

| Person | Primary Pillar | Focus Question |
|---|---|---|
| Person 1 | Direct Prompt Injection | Which instruction-override pattern stressed safety most? |
| Person 2 | Roleplay and Jailbreak | Did roleplay framing increase policy-drift risk? |
| Person 3 | Retrieval Poisoning and Obfuscation | Did retrieval trust checks or output filters fail first? |
| Person 4 | Language Switching | Was guardrail strength consistent across languages? |
| Person 5 | Fairness and Bias | What output difference implies unfair treatment risk? |

## Exercise 9: Release Advisory Board

| Person | Primary Pillar | Focus Question |
|---|---|---|
| Person 1 | Quality Lens | Is the quality delta meaningful or likely noise? |
| Person 2 | Performance Lens | Is the latency gain stable enough to trust? |
| Person 3 | Safety Lens | Did any high-severity safety signal regress? |
| Person 4 | Operations Lens | Can on-call and rollback paths absorb release risk? |
| Person 5 | Product Lens | Is the user impact of quality-speed trade-off acceptable? |
