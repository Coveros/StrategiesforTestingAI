"""MLflow-backed tracing helpers.

Drop-in replacement for app/phoenix_tracing.py: same get_tracer()/start_span()
call shape so app/rag_pipeline.py and app/agentic_testops.py did not need to be
rewritten, only re-pointed at this module. Spans are created with
mlflow.start_span() and a curated set of attributes is mirrored onto the
current trace's tags via mlflow.update_current_trace() so traces stay
searchable/filterable in the MLflow UI (equivalent to Phoenix's attribute
search) even though MLflow's search_traces() only queries trace-level tags,
not span attributes.
"""
import logging
import os
from contextlib import contextmanager, nullcontext
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)

# Attributes worth promoting to trace-level tags for MLflow UI search/filtering.
_TAG_WORTHY_KEYS = {
    "session.id",
    "exercise_number",
    "course.exercise.number",
    "app.mode",
    "agent.mode",
    "agent.role",
    "security.decision",
    "error.type",
}

# Map our span_kind strings onto MLflow's built-in SpanType values where a
# sensible match exists; anything else is kept as a free-form attribute.
_SPAN_TYPE_MAP = {
    "LLM": "LLM",
    "CHAIN": "CHAIN",
    "TOOL": "TOOL",
    "RETRIEVER": "RETRIEVER",
    "AGENT": "AGENT",
    "EMBEDDING": "EMBEDDING",
}

_CONFIGURED = False
_CONFIG_FAILED = False


def _is_truthy(value: str) -> bool:
    return str(value).strip().lower() in {"1", "true", "yes", "on"}


def _set_span_attribute(span: Any, key: str, value: Any) -> None:
    if value is None:
        return
    if isinstance(value, (bool, int, float, str)):
        span.set_attribute(key, value)
        return
    span.set_attribute(key, str(value))


def _configure_once(experiment_name: str) -> bool:
    """Point the mlflow client at the tracking server and enable autolog once per process."""
    global _CONFIGURED, _CONFIG_FAILED

    if _CONFIGURED:
        return True
    if _CONFIG_FAILED:
        return False

    try:
        import mlflow

        tracking_uri = os.getenv("MLFLOW_TRACKING_URI", "http://127.0.0.1:5001").strip()
        mlflow.set_tracking_uri(tracking_uri)
        mlflow.set_experiment(experiment_name)

        # Autolog captures LangChain chain/tool/LLM spans (with real inputs,
        # outputs, and token usage) automatically for the agentic path -
        # confirmed richer than hand-rolled callback instrumentation.
        if _is_truthy(os.getenv("MLFLOW_AUTOLOG_LANGCHAIN", "true")):
            mlflow.langchain.autolog()

        _CONFIGURED = True
        return True
    except Exception as exc:
        _CONFIG_FAILED = True
        logger.warning("MLflow tracing unavailable: %s", exc)
        return False


def get_tracer(
    component_name: str,
    *,
    enable_env: str,
    default_enabled: bool,
    default_project_name: str,
):
    env_default = "true" if default_enabled else "false"
    if not _is_truthy(os.getenv(enable_env, env_default)):
        return None, False

    experiment_name = os.getenv("MLFLOW_EXPERIMENT_NAME", default_project_name)
    if not _configure_once(experiment_name):
        return None, False

    # No persistent client/tracer object is needed for mlflow (unlike OTEL);
    # the component name is kept as a truthy sentinel so start_span() below
    # can tell "tracing enabled" apart from "tracing disabled" (None).
    return component_name, True


@contextmanager
def start_span(
    tracer: Any,
    name: str,
    *,
    span_kind: Optional[str] = None,
    attrs: Optional[Dict[str, Any]] = None,
):
    if tracer is None:
        with nullcontext() as span:
            yield span
        return

    import mlflow

    span_type = _SPAN_TYPE_MAP.get((span_kind or "").upper(), "UNKNOWN")
    with mlflow.start_span(name=name, span_type=span_type) as span:
        if span_kind:
            span.set_attribute("span.kind", span_kind)
        if attrs:
            for key, value in attrs.items():
                _set_span_attribute(span, key, value)

            tags = {
                key: str(value)
                for key, value in attrs.items()
                if key in _TAG_WORTHY_KEYS and value is not None
            }
            if tags:
                try:
                    mlflow.update_current_trace(tags=tags)
                except Exception:
                    # Tagging is best-effort; never fail the request over it.
                    pass
        yield span
