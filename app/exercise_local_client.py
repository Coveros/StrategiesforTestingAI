import time
import uuid
from typing import Any, Dict, Tuple


class _LocalResponse:
    def __init__(self, payload: Dict[str, Any], status_code: int) -> None:
        self._payload = payload
        self.status_code = status_code

    def get_json(self) -> Dict[str, Any]:
        return self._payload


class _LocalExerciseClient:
    """Minimal in-process client for exercise automation.

    This fallback supports only the API surface needed by the section quick-run
    scripts. It intentionally does not replace the Flask app.
    """

    def __init__(self) -> None:
        from app.agentic_testops import TestOpsAgent

        self._agent = TestOpsAgent()

    def post(self, path: str, json: Dict[str, Any] | None = None) -> _LocalResponse:
        if path != "/api/chat":
            return _LocalResponse({"error": "Endpoint not found", "status": "error"}, 404)

        data = json or {}
        message = str(data.get("message", "")).strip()
        if not message:
            return _LocalResponse({"error": "No message provided", "status": "error"}, 400)

        mode = str(data.get("mode", "rag")).strip().lower()
        if mode not in ("rag", "agentic"):
            return _LocalResponse({"error": "Invalid mode", "status": "error"}, 400)

        # The local fallback intentionally supports only agentic paths used by exercises 5-9.
        if mode != "agentic":
            return _LocalResponse(
                {
                    "error": "RAG mode unavailable in local fallback client",
                    "status": "error",
                },
                503,
            )

        include_trace = bool(data.get("include_trace", False))
        crew_mode = bool(data.get("crew_mode", False))
        session_id = str(data.get("session_id") or uuid.uuid4())

        start = time.time()
        payload = self._agent.process(
            message,
            session_id=session_id,
            include_trace=include_trace,
            crew_mode=crew_mode,
        )
        payload["response_time"] = round(time.time() - start, 3)
        payload["status"] = "success"
        payload["mode"] = mode
        payload["session_id"] = session_id
        return _LocalResponse(payload, 200)


def get_exercise_test_client() -> Tuple[Any, str]:
    """Return a client compatible with Flask test_client calls.

    Returns a tuple of (client, transport_name), where transport_name is
    either "flask" or "local-fallback".
    """
    try:
        from app.main import app

        return app.test_client(), "flask"
    except Exception:
        return _LocalExerciseClient(), "local-fallback"
