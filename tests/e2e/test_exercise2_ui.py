import pytest
from playwright.sync_api import Page

from .conftest import record_case, response_json, submit_ask


pytestmark = pytest.mark.e2e


def assistant_message(page: Page):
    return page.locator("#messagesContainer .message.assistant").last


def assert_successful_rag_payload(payload: dict) -> None:
    assert payload.get("status") == "success"
    assert payload.get("mode") == "rag"
    assert isinstance(payload.get("response"), str)
    assert payload["response"].strip()
    assert isinstance(payload.get("response_time"), (int, float))


def test_chat_page_exposes_ask_controls(ask_page: Page) -> None:
    record_case("chat_controls", "page load", controls_visible=True)
    assert ask_page.locator("#messageInput").is_visible()
    assert ask_page.locator("#sendButton").is_visible()
    assert ask_page.locator("#askModeBtn").get_attribute("aria-pressed") == "true"
    assert ask_page.locator("#agentModeBtn").get_attribute("aria-pressed") == "false"


def test_happy_path_returns_grounded_answer(ask_page: Page) -> None:
    response = submit_ask(ask_page, "What are the key challenges in testing GenAI applications?")
    payload = response_json(response)
    record_case("happy_path", "What are the key challenges in testing GenAI applications?", payload)

    assert response.ok
    assert_successful_rag_payload(payload)
    assert payload.get("sources"), "A known RAG question should return at least one source"
    assert assistant_message(ask_page).inner_text().strip()


def test_hallucination_question_covers_expected_topic(ask_page: Page) -> None:
    response = submit_ask(ask_page, "How should I test hallucinations in a GenAI application?")
    payload = response_json(response)
    record_case("hallucination_topic", "How should I test hallucinations in a GenAI application?", payload)
    assert response.ok
    assert_successful_rag_payload(payload)

    answer = payload["response"].lower()
    assert any(term in answer for term in ("hallucination", "ground", "unsupported", "fact"))


def test_rag_response_exposes_sources_and_timing(ask_page: Page) -> None:
    response = submit_ask(ask_page, "What metrics are useful for evaluating a RAG system?")
    payload = response_json(response)
    record_case("evidence_contract", "What metrics are useful for evaluating a RAG system?", payload)
    assert response.ok
    assert_successful_rag_payload(payload)
    assert isinstance(payload.get("sources"), list)
    assert isinstance(payload.get("retrieval_time"), (int, float))
    assert isinstance(payload.get("generation_time"), (int, float))
    assert isinstance(payload.get("total_time"), (int, float))
    for source in payload["sources"]:
        assert source.get("content")
        assert source.get("metadata", {}).get("source")


def test_empty_submission_does_not_add_a_chat_message(ask_page: Page) -> None:
    ask_page.locator("#messageInput").fill("")
    ask_page.locator("#sendButton").click()
    record_case("empty_input", "", submitted=False)
    assert ask_page.locator("#messagesContainer .message.assistant").count() == 0
    assert ask_page.locator("#messagesContainer .message.user").count() == 0


def test_oversized_input_returns_bounded_error(ask_page: Page) -> None:
    oversized_message = "x" * 2001
    response = submit_ask(ask_page, oversized_message)
    payload = response_json(response)
    record_case("oversized_input", oversized_message, payload)

    assert response.status == 400
    assert payload.get("status") == "error"
    assert "limit" in payload.get("error", "").lower()
    assert "error" in assistant_message(ask_page).inner_text().lower()


def test_equivalent_questions_return_repeatable_response_shape(ask_page: Page) -> None:
    first = response_json(submit_ask(ask_page, "What is regression testing for GenAI?"))
    second = response_json(submit_ask(ask_page, "Explain regression testing for generative AI."))
    record_case(
        "repeatability",
        "What is regression testing for GenAI? / Explain regression testing for generative AI.",
        first=first,
        second=second,
    )

    for payload in (first, second):
        assert_successful_rag_payload(payload)
        assert payload.get("sources")
        assert len(payload["response"]) >= 40
        assert "internal server error" not in payload["response"].lower()
        assert "traceback" not in payload["response"].lower()