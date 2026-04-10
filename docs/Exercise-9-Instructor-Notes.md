# Exercise 9: Automation and MLOps for Agentic Testers - Instructor Notes

---

## Objective

Students should demonstrate they can operationalize agentic testing with CI-style automation, thresholds, and deployment gates.

Key outcomes:

1. run automated baseline vs update comparisons
2. interpret flaky/probabilistic test behavior with retries
3. apply gating policy correctly
4. propose practical shift-right monitoring

---

## Setup Checklist

1. Verify script exists: `section9_agentic_test_suite.py`.
2. Confirm app imports correctly in each student VM environment.
3. Run once yourself:

```bash
python section9_agentic_test_suite.py
```

4. Confirm artifacts appear in `regression_test_results`:
   - `section9_agentic_ci_*.json`
   - `section9_agentic_ci_summary_*.txt`

---

## Timing (55-65 minutes)

| Phase | Time | Outcome |
|-|-|-|
| CI/CD framing | 5-7 minutes | Students understand prompt/config-as-code gate concept |
| Part A execution | 15 minutes | Artifacts generated |
| Part B analysis | 15 minutes | Baseline vs update differences identified |
| Part C gating | 10-15 minutes | Correct ship/no-ship decision justified |
| Part D shift-right plan | 15 minutes | Monitoring strategy drafted |
| Debrief | 5 minutes | Lessons consolidated |

---

## Expected Findings

1. Pirate persona update often causes style/tone regressions.
2. Showstopper safety checks should remain strict and non-negotiable.
3. Soft quality degradations can be handled as warnings depending on threshold.
4. Retry-on-fail can reduce flaky false alarms for non-showstopper checks.

---

## Rubric (0-2 per dimension)

### 1) Automation Execution (0-2)

- 0: no successful run
- 1: partial run/artifacts
- 2: complete run with both artifacts and clear evidence

### 2) Result Interpretation (0-2)

- 0: weak or incorrect interpretation
- 1: partial interpretation
- 2: accurate baseline vs update analysis with clear evidence

### 3) Gating Decision Quality (0-2)

- 0: decision unsupported or incorrect
- 1: somewhat justified decision
- 2: policy-aligned decision with explicit threshold reasoning

### 4) Monitoring Plan Quality (0-2)

- 0: generic monitoring ideas
- 1: partially actionable plan
- 2: clear metrics, thresholds, and response actions

---

## Strong Mitigations to Reward

1. Distinct showstopper vs warning channels
2. Quarantine policy for unstable tests (>5% failure rate without code changes)
3. Weekly drift dashboard (pass-rate, latency, bypass metrics)
4. Auto-conversion of validated user complaints into regression tests
5. Build artifact retention for historical comparisons

---

## Common Misconceptions

1. "All failures should block release."
   - Correction: only showstoppers should hard-block; degradations need policy-based handling.

2. "Retry logic hides bugs."
   - Correction: retries are useful for probabilistic variance when coupled with stability tracking.

3. "CI is enough."
   - Correction: shift-right monitoring is essential for unseen production edge cases.

---

## Debrief (5 minutes)

Ask teams:

1. "Would you ship pirate v2? Why?"
2. "Which metric would you put on an executive dashboard?"
3. "What one automation improvement should be implemented next sprint?"

Map to controls:

- safety confidence -> strict showstopper gates
- reliability confidence -> breaker + latency trend alerts
- quality confidence -> golden set regression + drift checks

---

## Closeout Message

"You started by exploratory testing single responses. You now have a full agentic test lifecycle: design, automate, gate, monitor, and improve. That is the core tester skillset for modern AI systems."

