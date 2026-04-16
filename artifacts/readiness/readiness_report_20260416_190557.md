# Exercise Readiness Report

Timestamp: 2026-04-16T19:05:57.314720
Passed: 25 / 26
Failed: 1

## Checks

- PASS: run.py exists -> C:\Users\jpayne\Documents\Training\Notebooks for ML classes\StrategiesforTestingAI\run.py
- PASS: launch.py exists -> C:\Users\jpayne\Documents\Training\Notebooks for ML classes\StrategiesforTestingAI\launch.py
- PASS: section7 runner exists -> C:\Users\jpayne\Documents\Training\Notebooks for ML classes\StrategiesforTestingAI\section7_nfr_quickrun.py
- PASS: section9 runner exists -> C:\Users\jpayne\Documents\Training\Notebooks for ML classes\StrategiesforTestingAI\section9_agentic_test_suite.py
- PASS: artifact prep helper exists -> C:\Users\jpayne\Documents\Training\Notebooks for ML classes\StrategiesforTestingAI\prepare_exercise_artifacts.py
- PASS: Exercise-1.md exists -> C:\Users\jpayne\Documents\Training\Notebooks for ML classes\StrategiesforTestingAI\docs\Exercise-1.md
- PASS: Exercise-2.md exists -> C:\Users\jpayne\Documents\Training\Notebooks for ML classes\StrategiesforTestingAI\docs\Exercise-2.md
- PASS: Exercise-3.md exists -> C:\Users\jpayne\Documents\Training\Notebooks for ML classes\StrategiesforTestingAI\docs\Exercise-3.md
- PASS: Exercise-4.md exists -> C:\Users\jpayne\Documents\Training\Notebooks for ML classes\StrategiesforTestingAI\docs\Exercise-4.md
- PASS: Exercise-5.md exists -> C:\Users\jpayne\Documents\Training\Notebooks for ML classes\StrategiesforTestingAI\docs\Exercise-5.md
- PASS: Exercise-6.md exists -> C:\Users\jpayne\Documents\Training\Notebooks for ML classes\StrategiesforTestingAI\docs\Exercise-6.md
- PASS: Exercise-7.md exists -> C:\Users\jpayne\Documents\Training\Notebooks for ML classes\StrategiesforTestingAI\docs\Exercise-7.md
- PASS: Exercise-8.md exists -> C:\Users\jpayne\Documents\Training\Notebooks for ML classes\StrategiesforTestingAI\docs\Exercise-8.md
- PASS: Exercise-9.md exists -> C:\Users\jpayne\Documents\Training\Notebooks for ML classes\StrategiesforTestingAI\docs\Exercise-9.md
- PASS: Exercise 3 regression snapshot -> C:\Users\jpayne\Documents\Training\Notebooks for ML classes\StrategiesforTestingAI\artifacts\precomputed\exercise3\regression_results_20260416_190505.json
- PASS: Exercise 3 regression summary -> C:\Users\jpayne\Documents\Training\Notebooks for ML classes\StrategiesforTestingAI\artifacts\precomputed\exercise3\regression_summary_20260416_190505.txt
- PASS: Exercise 3 evaluation results -> C:\Users\jpayne\Documents\Training\Notebooks for ML classes\StrategiesforTestingAI\artifacts\precomputed\exercise3\evaluation_results.json
- PASS: Exercise 3 evaluation report -> C:\Users\jpayne\Documents\Training\Notebooks for ML classes\StrategiesforTestingAI\artifacts\precomputed\exercise3\evaluation_report.md
- PASS: Exercise 4 trace sample -> C:\Users\jpayne\Documents\Training\Notebooks for ML classes\StrategiesforTestingAI\artifacts\precomputed\trace_samples\exercise4_trace_cases_20260416_190513.json
- PASS: Exercise 6 trajectory sample -> C:\Users\jpayne\Documents\Training\Notebooks for ML classes\StrategiesforTestingAI\artifacts\precomputed\trace_samples\exercise6_trajectory_cases_20260416_190513.json
- PASS: Exercise 7 quickrun artifact -> C:\Users\jpayne\Documents\Training\Notebooks for ML classes\StrategiesforTestingAI\artifacts\precomputed\section7\section7_quickrun_20260416_190432.json
- PASS: Exercise 9 CI artifact -> C:\Users\jpayne\Documents\Training\Notebooks for ML classes\StrategiesforTestingAI\artifacts\precomputed\section9\section9_agentic_ci_20260416_190432.json
- PASS: Smoke: Section 7 quick-run -> exit=0
- PASS: Smoke: Section 9 CI suite -> exit=0
- FAIL: Smoke: Regression quick offline -> exit=1 | >
    print("\u26a0\ufe0f  sentence-transformers unavailable; using fallback similarity.")
  File "C:\Python311\Lib\encodings\cp1252.py", line 19, in encode
    return codecs.charmap_encode(input,self.errors,encoding_table)[0]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
UnicodeEncodeError: 'charmap' codec can't encode characters in position 0-1: character maps to <undefined>
- PASS: Smoke: Evaluation offline -> exit=0
