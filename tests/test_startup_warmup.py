import os


def test_startup_warmup_disabled_by_default(monkeypatch):
    monkeypatch.delenv("RAG_WARMUP_ENABLED", raising=False)
    monkeypatch.delenv("AGENT_WARMUP_ON_STARTUP", raising=False)
    monkeypatch.delenv("CLASSROOM_PREWARM_ENABLED", raising=False)

    from app.rag_pipeline import RAGPipeline

    assert RAGPipeline._should_run_startup_warmup() is False
