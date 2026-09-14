import json
import os
from datetime import datetime, timezone
from pathlib import Path

import pytest
import requests
from playwright.sync_api import APIResponse, Page


BASE_URL = os.getenv("E2E_BASE_URL", "http://127.0.0.1:5000").rstrip("/")
_RUN_EVIDENCE = []


def record_case(test_name: str, prompt: str, payload: dict | None = None, **observations) -> None:
    """Keep classroom-safe evidence for Exercise 3 analysis."""
    entry = {
        "test_name": test_name,
        "prompt": prompt,
        "recorded_at": datetime.now(timezone.utc).isoformat(),
        "observations": observations,
    }
    if payload is not None:
        entry["response"] = {
            "status": payload.get("status"),
            "mode": payload.get("mode"),
            "exercise_number": payload.get("exercise_number"),
            "session_id": payload.get("session_id"),
            "response": payload.get("response", ""),
            "sources": payload.get("sources", []),
            "response_time": payload.get("response_time"),
            "retrieval_time": payload.get("retrieval_time"),
            "generation_time": payload.get("generation_time"),
            "total_time": payload.get("total_time"),
            "error": payload.get("error"),
        }
    _RUN_EVIDENCE.append(entry)


def pytest_sessionfinish(session, exitstatus) -> None:
    if not _RUN_EVIDENCE:
        return
    output_dir = Path(os.getenv("E2E_ARTIFACT_DIR", "artifacts/exercise2"))
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / f"ui_golden_run_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    output_file.write_text(
        json.dumps(
            {
                "suite": "exercise2_ui_golden",
                "generated_at": datetime.now(timezone.utc).isoformat(),
                "exit_status": exitstatus,
                "base_url": BASE_URL,
                "cases": _RUN_EVIDENCE,
            },
            indent=2,
        ),
        encoding="utf-8",
    )


@pytest.fixture(scope="session")
def base_url() -> str:
    return BASE_URL


@pytest.fixture(scope="session", autouse=True)
def require_running_app(base_url: str) -> None:
    """Fail with a useful classroom setup message when Flask is not running."""
    try:
        response = requests.get(f"{base_url}/api/health", timeout=5)
    except Exception as exc:
        pytest.fail(
            f"The Flask app is not reachable at {base_url}. Start it with `python run.py` "
            f"before running the Exercise 2 browser suite. Details: {exc}"
        )

    if not response.ok:
        pytest.fail(f"Flask health check returned HTTP {response.status} at {base_url}/api/health")


@pytest.fixture
def ask_page(page: Page, base_url: str) -> Page:
    page.goto(f"{base_url}/?exercise=2", wait_until="domcontentloaded")
    page.locator("#askModeBtn").click()
    return page


def submit_ask(page: Page, message: str) -> APIResponse:
    """Submit through the UI and return the matching API response for assertions."""
    with page.expect_response("**/api/chat") as response_info:
        page.locator("#messageInput").fill(message)
        page.locator("#sendButton").click()

    response = response_info.value
    page.locator("#messagesContainer .message.assistant").last.wait_for(state="visible")
    return response


def response_json(response: APIResponse) -> dict:
    payload = response.json()
    assert isinstance(payload, dict), "The chat endpoint must return a JSON object"
    return payload