import logging
import os
from contextlib import contextmanager, nullcontext
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)

OPENINFERENCE_SPAN_KIND = "openinference.span.kind"

_REGISTERED = False
_REGISTER_FAILED = False


def _is_truthy(value: str) -> bool:
    return str(value).strip().lower() in {"1", "true", "yes", "on"}


def _set_span_attribute(span: Any, key: str, value: Any) -> None:
    if value is None:
        return
    if isinstance(value, (bool, int, float, str)):
        span.set_attribute(key, value)
        return
    span.set_attribute(key, str(value))


def _register_once(project_name: str) -> bool:
    global _REGISTERED, _REGISTER_FAILED

    if _REGISTERED:
        return True
    if _REGISTER_FAILED:
        return False

    try:
        from phoenix.otel import register

        register(project_name=project_name)
        _REGISTERED = True
        return True
    except Exception as exc:
        _REGISTER_FAILED = True
        logger.warning("Phoenix tracing unavailable: %s", exc)
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

    project_name = os.getenv("PHOENIX_PROJECT_NAME", default_project_name)
    if not _register_once(project_name):
        return None, False

    from opentelemetry import trace

    return trace.get_tracer(component_name), True


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

    with tracer.start_as_current_span(name) as span:
        if span_kind:
            span.set_attribute(OPENINFERENCE_SPAN_KIND, span_kind)
        if attrs:
            for key, value in attrs.items():
                _set_span_attribute(span, key, value)
        yield span