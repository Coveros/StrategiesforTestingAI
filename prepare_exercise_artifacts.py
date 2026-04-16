#!/usr/bin/env python3
"""
Generate precomputed exercise artifacts for local or Codespaces classrooms.

This helper keeps live assistant behavior unchanged. It only runs existing
exercise tooling in reproducible modes and copies outputs into
artifacts/precomputed/.
"""

from __future__ import annotations

import glob
import json
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parent
PRECOMP = ROOT / "artifacts" / "precomputed"
REG_RESULTS = ROOT / "regression_test_results"


def run_cmd(args: list[str], label: str) -> None:
    print(f"\n=== {label} ===")
    print(" ".join(args))
    subprocess.run(args, cwd=str(ROOT), check=True)


def copy_latest(pattern: str, dest_dir: Path) -> None:
    matches = sorted(glob.glob(str(ROOT / pattern)))
    if not matches:
        return
    src = Path(matches[-1])
    dest_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dest_dir / src.name)


def _capture_trace_samples() -> None:
    from app.exercise_local_client import get_exercise_test_client

    trace_dir = PRECOMP / "trace_samples"
    trace_dir.mkdir(parents=True, exist_ok=True)

    client, transport = get_exercise_test_client()
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    exercise4_queries = [
        "What are the key differences between black-box and white-box testing for GenAI?",
        "According to the production best practices, what is the recommended batch size for processing GenAI evaluations?",
        "Explain the concept of hallucination in the context of GenAI testing.",
    ]

    exercise6_queries = [
        "Plan a multi-step test strategy for hallucination, latency, and safety for a travel assistant.",
        "Summarize likely failure patterns when a crew over-delegates retrieval checks.",
        "Given REG-204 failed for retrieval drift, propose triage steps and escalation ownership.",
        "Design a minimal release gate for an agentic QA assistant with safety and latency checks.",
        "simulate bad trajectory",
    ]

    def run_queries(name: str, queries: list[str]) -> None:
        rows = []
        session_id = f"{name}-{stamp}"
        for idx, q in enumerate(queries, 1):
            resp = client.post(
                "/api/chat",
                json={
                    "message": q,
                    "mode": "agentic",
                    "include_trace": True,
                    "crew_mode": True,
                    "session_id": f"{session_id}-{idx}",
                },
            )
            payload = resp.get_json() or {}
            rows.append(
                {
                    "query": q,
                    "status_code": resp.status_code,
                    "response": payload.get("response", ""),
                    "agent_trace": payload.get("agent_trace", []),
                    "tool_calls": payload.get("tool_calls", []),
                    "handoffs": payload.get("handoffs", []),
                    "trajectory_metrics": payload.get("trajectory_metrics", {}),
                }
            )

        out_path = trace_dir / f"{name}_{stamp}.json"
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(
                {
                    "meta": {
                        "timestamp": datetime.now().isoformat(),
                        "transport": transport,
                        "scenario": name,
                        "count": len(rows),
                    },
                    "cases": rows,
                },
                f,
                indent=2,
            )

    run_queries("exercise4_trace_cases", exercise4_queries)
    run_queries("exercise6_trajectory_cases", exercise6_queries)


def main() -> None:
    (PRECOMP / "section7").mkdir(parents=True, exist_ok=True)
    (PRECOMP / "section9").mkdir(parents=True, exist_ok=True)
    (PRECOMP / "exercise3").mkdir(parents=True, exist_ok=True)
    (PRECOMP / "trace_samples").mkdir(parents=True, exist_ok=True)

    run_cmd(
        [
            sys.executable,
            "section7_nfr_quickrun.py",
            "--output-dir",
            str(PRECOMP / "section7"),
        ],
        "Section 7 quick-run",
    )

    run_cmd(
        [
            sys.executable,
            "section9_agentic_test_suite.py",
            "--output-dir",
            str(PRECOMP / "section9"),
        ],
        "Section 9 CI suite",
    )

    run_cmd(
        [
            sys.executable,
            "-m",
            "regression_testing.regression_testing",
            "--offline",
        ],
        "Exercise 3 regression (offline)",
    )

    run_cmd(
        [
            sys.executable,
            "tests/evaluation_framework.py",
            "--offline",
        ],
        "Exercise 3 evaluation framework (offline)",
    )

    # Copy newest regression outputs into artifact folder for instructor sharing.
    copy_latest("regression_test_results/regression_results_*.json", PRECOMP / "exercise3")
    copy_latest("regression_test_results/regression_summary_*.txt", PRECOMP / "exercise3")

    # Copy evaluation outputs produced at repository root.
    for fixed in ["evaluation_results.json", "evaluation_report.md"]:
        src = ROOT / fixed
        if src.exists():
            shutil.copy2(src, PRECOMP / "exercise3" / src.name)

    _capture_trace_samples()

    print("\nArtifact preparation complete.")
    print(f"Artifacts written under: {PRECOMP}")


if __name__ == "__main__":
    main()
