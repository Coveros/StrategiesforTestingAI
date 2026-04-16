# Precomputed Exercise Artifacts

This folder stores reproducible, in-repo artifacts used as preconditions for
shortened Exercises 3, 4, 6, 7, and 9.

Generate or refresh artifacts with:

```bash
python prepare_exercise_artifacts.py
```

Outputs are grouped by exercise area:

- `exercise3/` quick regression snapshot + evaluation framework outputs
- `trace_samples/` precomputed trace and trajectory captures for Exercises 4 and 6
- `section7/` NFR quick-run JSON/TXT outputs
- `section9/` CI-style gate JSON/TXT outputs

These are intended for classroom setup (local and Codespaces) where students
need evidence artifacts immediately, without requiring all runs to execute live.
