import os

import pytest
import requests
from playwright.sync_api import APIResponse, Page


BASE_URL = os.getenv("E2E_BASE_URL", "http://127.0.0.1:5000").rstrip("/")


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