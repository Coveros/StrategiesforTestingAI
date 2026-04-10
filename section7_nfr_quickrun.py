#!/usr/bin/env python3
"""
Quick runner for Section 7 NFR scenarios against the local agentic chatbot.

This script executes a deterministic set of failure and recovery prompts,
and writes both JSON and TXT artifacts that students can submit.
"""

import argparse
import json
import os
from datetime import datetime
from typing import Any, Dict, List

from app.main import app


def _now_stamp() -> str:
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def _safe_get(d: Dict[str, Any], key: str, default: Any = None) -> Any:
    return d.get(key, default) if isinstance(d, dict) else default


def _build_cases() -> List[Dict[str, Any]]:
    return [
        {
            "id": "dep_outage_1",
            "prompt": "run quick regression simulate dependency outage",
            "expect": "degraded",
        },
        {
            "id": "dep_outage_2",
            "prompt": "run quick regression simulate dependency outage",
            "expect": "degraded",
        },
        {
            "id": "breaker_block",
            "prompt": "run quick regression suite",
            "expect": "breaker_open",
        },
        {
            "id": "breaker_reset",
            "prompt": "reset circuit breaker",
            "expect": "reset_ok",
        },
        {
            "id": "post_reset_normal",
            "prompt": "run quick regression suite",
            "expect": "normal",
        },
        {
            "id": "timeout_case",
            "prompt": "run quick regression simulate tool timeout",
            "expect": "degraded",
        },
        {
            "id": "rate_limit_case",
            "prompt": "run quick regression simulate rate limit",
            "expect": "degraded",
        },
        {
            "id": "empty_input",
            "prompt": "   ",
            "expect": "handled",
        },
        {
            "id": "gibberish_input",
            "prompt": "xqz@@##123###??",
            "expect": "handled",
        },
    ]


def _evaluate(case: Dict[str, Any], payload: Dict[str, Any], status_code: int) -> Dict[str, Any]:
    metrics = _safe_get(payload, "trajectory_metrics", {})
    response = str(_safe_get(payload, "response", ""))

    degraded = bool(_safe_get(metrics, "degraded_mode", False))
    circuit_open = bool(_safe_get(metrics, "circuit_open", False))

    expect = case["expect"]
    passed = False

    if status_code != 200:
        passed = False
    elif expect == "degraded":
        passed = degraded is True
    elif expect == "breaker_open":
        passed = circuit_open is True or "circuit" in response.lower()
    elif expect == "reset_ok":
        passed = "reset" in response.lower()
    elif expect == "normal":
        passed = degraded is False and circuit_open is False
    elif expect == "handled":
        passed = len(response.strip()) > 0

    tool_calls = int(_safe_get(metrics, "tool_calls", 0) or 0)
    redundant = int(_safe_get(metrics, "redundant_tool_calls", 0) or 0)
    loop_tax = round(redundant / (tool_calls + 1), 3)

    return {
        "passed": passed,
        "status_code": status_code,
        "degraded_mode": degraded,
        "circuit_open": circuit_open,
        "steps": int(_safe_get(metrics, "steps", 0) or 0),
        "tool_calls": tool_calls,
        "redundant_tool_calls": redundant,
        "loop_tax": loop_tax,
        "response_preview": response[:160],
    }


def run_suite(session_id: str, include_trace: bool, crew_mode: bool) -> Dict[str, Any]:
    client = app.test_client()
    cases = _build_cases()
    results: List[Dict[str, Any]] = []

    for case in cases:
        request_payload = {
            "message": case["prompt"],
            "mode": "agentic",
            "include_trace": include_trace,
            "crew_mode": crew_mode,
            "session_id": session_id,
        }

        response = client.post("/api/chat", json=request_payload)
        payload = response.get_json() or {}
        eval_row = _evaluate(case, payload, response.status_code)

        results.append(
            {
                "id": case["id"],
                "prompt": case["prompt"],
                "expect": case["expect"],
                "evaluation": eval_row,
                "raw": {
                    "mode": _safe_get(payload, "mode"),
                    "response_time": _safe_get(payload, "response_time"),
                    "trajectory_metrics": _safe_get(payload, "trajectory_metrics", {}),
                    "handoffs": _safe_get(payload, "handoffs", []),
                },
            }
        )

    total = len(results)
    passed = len([r for r in results if _safe_get(_safe_get(r, "evaluation", {}), "passed", False)])
    avg_response = round(
        sum((_safe_get(_safe_get(r, "raw", {}), "response_time", 0) or 0) for r in results) / max(total, 1),
        3,
    )
    worst_response = round(
        max((_safe_get(_safe_get(r, "raw", {}), "response_time", 0) or 0) for r in results),
        3,
    )

    return {
        "run_meta": {
            "timestamp": datetime.now().isoformat(),
            "session_id": session_id,
            "include_trace": include_trace,
            "crew_mode": crew_mode,
            "total_cases": total,
            "passed_cases": passed,
            "pass_rate": round(passed / max(total, 1), 3),
            "avg_response_time": avg_response,
            "worst_response_time": worst_response,
        },
        "results": results,
    }


def write_artifacts(report: Dict[str, Any], out_dir: str) -> Dict[str, str]:
    os.makedirs(out_dir, exist_ok=True)
    stamp = _now_stamp()

    json_path = os.path.join(out_dir, f"section7_quickrun_{stamp}.json")
    txt_path = os.path.join(out_dir, f"section7_quickrun_summary_{stamp}.txt")

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

    meta = report["run_meta"]
    lines = [
        "Section 7 NFR Quick-Run Summary",
        "=" * 36,
        f"Timestamp: {meta['timestamp']}",
        f"Session ID: {meta['session_id']}",
        f"Crew Mode: {meta['crew_mode']}",
        f"Include Trace: {meta['include_trace']}",
        f"Cases Passed: {meta['passed_cases']} / {meta['total_cases']}",
        f"Pass Rate: {meta['pass_rate']}",
        f"Avg Response Time: {meta['avg_response_time']}s",
        f"Worst Response Time: {meta['worst_response_time']}s",
        "",
        "Case Details",
        "-" * 36,
    ]

    for row in report["results"]:
        ev = row["evaluation"]
        lines.append(
            f"{row['id']}: {'PASS' if ev['passed'] else 'FAIL'} | "
            f"degraded={ev['degraded_mode']} circuit_open={ev['circuit_open']} "
            f"steps={ev['steps']} tools={ev['tool_calls']} loop_tax={ev['loop_tax']}"
        )

    with open(txt_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")

    return {"json": json_path, "txt": txt_path}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run Section 7 NFR quick scenarios and export artifacts.")
    parser.add_argument("--session-id", default=f"section7-{_now_stamp()}", help="Session ID used for all prompts")
    parser.add_argument(
        "--output-dir",
        default="regression_test_results",
        help="Directory where JSON/TXT artifacts will be written",
    )
    parser.add_argument("--no-trace", action="store_true", help="Disable trace collection to reduce output size")
    parser.add_argument("--no-crew", action="store_true", help="Run in single-agent mode instead of crew mode")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    report = run_suite(
        session_id=args.session_id,
        include_trace=not args.no_trace,
        crew_mode=not args.no_crew,
    )
    paths = write_artifacts(report, args.output_dir)

    meta = report["run_meta"]
    print("Section 7 quick-run completed")
    print(f"Passed: {meta['passed_cases']} / {meta['total_cases']} ({meta['pass_rate']})")
    print(f"Avg response time: {meta['avg_response_time']}s | Worst: {meta['worst_response_time']}s")
    print(f"JSON report: {paths['json']}")
    print(f"Summary report: {paths['txt']}")


if __name__ == "__main__":
    main()
