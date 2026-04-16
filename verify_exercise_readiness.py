#!/usr/bin/env python3
"""Exercise readiness verifier for Exercises 1-9.

Checks that required code paths, scripts, and precomputed artifacts exist,
and optionally executes key smoke commands.
"""

from __future__ import annotations

import argparse
import glob
import json
import os
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent


@dataclass
class CheckResult:
    name: str
    ok: bool
    details: str


def latest(pattern: str) -> Path | None:
    matches = sorted(glob.glob(str(ROOT / pattern)))
    if not matches:
        return None
    return Path(matches[-1])


def exists_check(name: str, path: Path) -> CheckResult:
    ok = path.exists()
    return CheckResult(name, ok, str(path))


def glob_check(name: str, pattern: str) -> CheckResult:
    found = latest(pattern)
    return CheckResult(name, found is not None, pattern if found is None else str(found))


def run_cmd(name: str, args: list[str]) -> CheckResult:
    try:
        env = dict(os.environ)
        env["PYTHONIOENCODING"] = "utf-8"
        proc = subprocess.run(
            args,
            cwd=str(ROOT),
            capture_output=True,
            text=True,
            env=env,
            encoding="utf-8",
            errors="replace",
        )
    except Exception as e:
        return CheckResult(name, False, f"failed to run: {e}")

    ok = proc.returncode == 0
    details = f"exit={proc.returncode}"
    if not ok:
        tail = (proc.stdout + "\n" + proc.stderr).strip()
        details += f" | {tail[-400:]}"
    return CheckResult(name, ok, details)


def collect_checks(smoke: bool) -> list[CheckResult]:
    checks: list[CheckResult] = []

    # Core app/scripts
    checks.append(exists_check("run.py exists", ROOT / "run.py"))
    checks.append(exists_check("launch.py exists", ROOT / "launch.py"))
    checks.append(exists_check("section7 runner exists", ROOT / "section7_nfr_quickrun.py"))
    checks.append(exists_check("section9 runner exists", ROOT / "section9_agentic_test_suite.py"))
    checks.append(exists_check("artifact prep helper exists", ROOT / "prepare_exercise_artifacts.py"))

    # Exercise docs
    for i in range(1, 10):
        checks.append(exists_check(f"Exercise-{i}.md exists", ROOT / "docs" / f"Exercise-{i}.md"))

    # Precomputed artifacts expected for shortened labs
    checks.append(glob_check("Exercise 3 regression snapshot", "artifacts/precomputed/exercise3/regression_results_*.json"))
    checks.append(glob_check("Exercise 3 regression summary", "artifacts/precomputed/exercise3/regression_summary_*.txt"))
    checks.append(exists_check("Exercise 3 evaluation results", ROOT / "artifacts/precomputed/exercise3/evaluation_results.json"))
    checks.append(exists_check("Exercise 3 evaluation report", ROOT / "artifacts/precomputed/exercise3/evaluation_report.md"))
    checks.append(glob_check("Exercise 4 trace sample", "artifacts/precomputed/trace_samples/exercise4_trace_cases_*.json"))
    checks.append(glob_check("Exercise 6 trajectory sample", "artifacts/precomputed/trace_samples/exercise6_trajectory_cases_*.json"))
    checks.append(glob_check("Exercise 7 quickrun artifact", "artifacts/precomputed/section7/section7_quickrun_*.json"))
    checks.append(glob_check("Exercise 9 CI artifact", "artifacts/precomputed/section9/section9_agentic_ci_*.json"))

    if smoke:
        checks.append(run_cmd("Smoke: Section 7 quick-run", [sys.executable, "section7_nfr_quickrun.py", "--output-dir", "artifacts/precomputed/section7"]))
        checks.append(run_cmd("Smoke: Section 9 CI suite", [sys.executable, "section9_agentic_test_suite.py", "--output-dir", "artifacts/precomputed/section9"]))
        checks.append(run_cmd("Smoke: Regression quick offline", [sys.executable, "-m", "regression_testing.regression_testing", "--quick", "--offline"]))
        checks.append(run_cmd("Smoke: Evaluation offline", [sys.executable, "tests/evaluation_framework.py", "--offline"]))

    return checks


def write_report(checks: list[CheckResult]) -> tuple[Path, Path]:
    out_dir = ROOT / "artifacts" / "readiness"
    out_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    passed = [c for c in checks if c.ok]
    failed = [c for c in checks if not c.ok]

    report = {
        "timestamp": datetime.now().isoformat(),
        "total": len(checks),
        "passed": len(passed),
        "failed": len(failed),
        "checks": [{"name": c.name, "ok": c.ok, "details": c.details} for c in checks],
    }

    jpath = out_dir / f"readiness_report_{stamp}.json"
    mpath = out_dir / f"readiness_report_{stamp}.md"

    with open(jpath, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

    lines = [
        "# Exercise Readiness Report",
        "",
        f"Timestamp: {report['timestamp']}",
        f"Passed: {report['passed']} / {report['total']}",
        f"Failed: {report['failed']}",
        "",
        "## Checks",
        "",
    ]

    for c in checks:
        status = "PASS" if c.ok else "FAIL"
        lines.append(f"- {status}: {c.name} -> {c.details}")

    with open(mpath, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")

    return jpath, mpath


def main() -> None:
    parser = argparse.ArgumentParser(description="Verify exercise readiness for Exercises 1-9")
    parser.add_argument("--smoke", action="store_true", help="Run key smoke commands in addition to file checks")
    args = parser.parse_args()

    checks = collect_checks(smoke=args.smoke)
    jpath, mpath = write_report(checks)

    failed = [c for c in checks if not c.ok]
    print("Exercise readiness verification complete")
    print(f"Checks: {len(checks)} | Failed: {len(failed)}")
    print(f"JSON report: {jpath}")
    print(f"Markdown report: {mpath}")

    if failed:
        sys.exit(1)


if __name__ == "__main__":
    main()
