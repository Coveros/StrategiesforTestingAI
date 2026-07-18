import logging
import os
import re
import time
import importlib
from collections import Counter
from typing import TYPE_CHECKING
from typing import Any, Dict, List, Optional

if TYPE_CHECKING:
    from app.rag_pipeline import RAGPipeline

from app.phoenix_tracing import get_tracer, start_span

logger = logging.getLogger(__name__)


class TestOpsAgent:
    """LangChain-based agent backend for Exercises 5-9.

    Supports:
    - Single-agent ReAct mode (crew_mode=False)
    - Multi-agent router mode (crew_mode=True)
    - Phoenix OpenTelemetry span hooks (when available)
    """

    def __init__(self) -> None:
        self.session_state: Dict[str, Dict[str, Any]] = {}
        self.stats = {
            "requests": 0,
            "crew_requests": 0,
            "tool_calls": 0,
            "blocked_actions": 0,
            "clarifications": 0,
            "resets": 0,
            "fallback_responses": 0,
            "errors": 0,
        }

        self.ollama_host = os.getenv("OLLAMA_HOST", "http://127.0.0.1:11434")
        self.model_name = os.getenv("AGENT_MODEL", os.getenv("OLLAMA_MODEL", "llama3.2:1b"))
        self.temperature = self._safe_float(os.getenv("AGENT_TEMPERATURE", "0.2"), default=0.2)
        self.max_iterations = int(self._safe_float(os.getenv("AGENT_MAX_ITERATIONS", "10"), default=10))
        self.request_timeout_seconds = int(self._safe_float(os.getenv("AGENT_REQUEST_TIMEOUT_SECONDS", "300"), default=300))
        bootstrap_mode = str(os.getenv("AGENT_BOOTSTRAP_ON_ZERO_TOOLS", "auto")).strip().lower()
        instructor_mode = self._is_truthy(os.getenv("EXERCISE_HUB_ENABLE_INSTRUCTOR", "false"))
        if bootstrap_mode in {"1", "true", "yes", "on"}:
            self.bootstrap_on_zero_tools = True
        elif bootstrap_mode in {"0", "false", "no", "off"}:
            self.bootstrap_on_zero_tools = False
        else:
            # Auto mode defaults to student-friendly recovery and stays off for instructor-led runs.
            self.bootstrap_on_zero_tools = not instructor_mode

        self.llm: Optional[Any] = None

        self.rag_pipeline: Optional["RAGPipeline"] = None

        self.tracer, self.phoenix_enabled = get_tracer(
            "strategiesfortestingai.agentic",
            enable_env="ENABLE_PHOENIX_AGENT_TRACING",
            default_enabled=True,
            default_project_name="strategiesfortestingai",
        )

    def _safe_float(self, value: str, default: float) -> float:
        try:
            return float(value)
        except (TypeError, ValueError):
            return default

    def _is_truthy(self, value: Any) -> bool:
        return str(value).strip().lower() in {"1", "true", "yes", "on"}

    def _get_llm(self):
        if self.llm is None:
            from langchain_ollama import ChatOllama

            self.llm = ChatOllama(
                model=self.model_name,
                base_url=self.ollama_host,
                temperature=self.temperature,
                sync_client_kwargs={"timeout": self.request_timeout_seconds},
                async_client_kwargs={"timeout": self.request_timeout_seconds},
            )
        return self.llm

    def _resolve_langchain_agent_runtime(self):
        """Resolve ReAct runtime across classic LangChain and modern LangGraph layouts."""
        agent_executor_cls = None
        create_react_agent_fn = None

        # AgentExecutor moved between versions; try known module locations.
        for module_name, attr_name in (
            ("langchain.agents", "AgentExecutor"),
            ("langchain.agents.agent", "AgentExecutor"),
            ("langchain_classic.agents", "AgentExecutor"),
        ):
            try:
                module = importlib.import_module(module_name)
                agent_executor_cls = getattr(module, attr_name, None)
                if agent_executor_cls is not None:
                    break
            except Exception:
                continue

        # create_react_agent can also move by version.
        for module_name, attr_name in (
            ("langchain.agents", "create_react_agent"),
            ("langchain.agents.react.agent", "create_react_agent"),
            ("langchain_classic.agents", "create_react_agent"),
        ):
            try:
                module = importlib.import_module(module_name)
                create_react_agent_fn = getattr(module, attr_name, None)
                if create_react_agent_fn is not None:
                    break
            except Exception:
                continue

        if agent_executor_cls is not None and create_react_agent_fn is not None:
            return {
                "kind": "classic",
                "AgentExecutor": agent_executor_cls,
                "create_react_agent": create_react_agent_fn,
            }

        # Newer LangChain versions use LangGraph prebuilt ReAct agents.
        try:
            module = importlib.import_module("langgraph.prebuilt")
            langgraph_create_react_agent = getattr(module, "create_react_agent", None)
            if langgraph_create_react_agent is not None:
                return {
                    "kind": "langgraph",
                    "create_react_agent": langgraph_create_react_agent,
                }
        except Exception:
            pass

        raise ImportError(
            "LangChain agent runtime imports failed. Ensure create_react_agent is available from "
            "langchain/langchain_classic or langgraph.prebuilt in your installed version."
        )

    def _message_text(self, message: Any) -> str:
        """Normalize message content to plain text across LangChain/LangGraph message types."""
        content = getattr(message, "content", message)
        if isinstance(content, str):
            return content
        if isinstance(content, list):
            chunks: List[str] = []
            for part in content:
                if isinstance(part, dict):
                    text = part.get("text")
                    if text:
                        chunks.append(str(text))
                elif part is not None:
                    chunks.append(str(part))
            return " ".join(chunks).strip()
        return str(content).strip()

    def _invoke_langgraph_react(self, create_react_agent_fn, llm, tools, system_text: str, user_input: str) -> Dict[str, Any]:
        """Execute LangGraph prebuilt ReAct agent and extract output/trajectory."""
        agent = None
        for constructor in (
            lambda: create_react_agent_fn(model=llm, tools=tools, prompt=system_text),
            lambda: create_react_agent_fn(llm, tools, prompt=system_text),
            lambda: create_react_agent_fn(llm, tools),
        ):
            try:
                agent = constructor()
                break
            except TypeError:
                continue

        if agent is None:
            raise RuntimeError("Unable to construct LangGraph ReAct agent with available signatures")

        result = None
        last_error = None
        for payload in (
            {"messages": [("user", user_input)]},
            {"messages": [{"role": "user", "content": user_input}]},
            {"input": user_input},
        ):
            try:
                result = agent.invoke(payload)
                break
            except Exception as exc:
                last_error = exc
                continue

        if result is None:
            if last_error is not None:
                raise last_error
            raise RuntimeError("LangGraph ReAct invocation failed")

        trace: List[Dict[str, str]] = []
        output = ""
        messages = result.get("messages", []) if isinstance(result, dict) else []

        for msg in messages:
            msg_type = str(getattr(msg, "type", "")).lower()
            text = self._message_text(msg)

            if msg_type == "ai":
                output = text or output
                tool_calls = getattr(msg, "tool_calls", None) or []
                for tool_call in tool_calls:
                    if isinstance(tool_call, dict):
                        tool_name = str(tool_call.get("name", "unknown"))
                        tool_input = tool_call.get("args", tool_call.get("input", ""))
                    else:
                        tool_name = str(tool_call)
                        tool_input = ""
                    trace.append({
                        "phase": "action",
                        "content": f"tool={tool_name} input={tool_input}",
                    })
            elif msg_type == "tool":
                trace.append({
                    "phase": "observation",
                    "content": text[:280],
                })

        if not output:
            for msg in reversed(messages):
                text = self._message_text(msg)
                if text:
                    output = text
                    break

        if not output and isinstance(result, dict):
            output = str(result.get("output", "")).strip()

        return {
            "output": output.strip(),
            "trace": trace,
        }

    def _span(self, name: str, attrs: Optional[Dict[str, Any]] = None):
        return start_span(self.tracer, name, attrs=attrs)

    def _span_name(self, base_name: str, exercise_number: Optional[int]) -> str:
        """Make span names searchable by exercise in Phoenix name search."""
        if isinstance(exercise_number, int) and exercise_number > 0:
            return f"{base_name}.ex{exercise_number}"
        return base_name

    def _get_rag_pipeline(self) -> "RAGPipeline":
        # Delay heavy RAG imports until first actual KB access.
        from app.rag_pipeline import RAGPipeline

        if self.rag_pipeline is None:
            self.rag_pipeline = RAGPipeline()
        return self.rag_pipeline

    def _empty_trajectory_metrics(self) -> Dict[str, Any]:
        return {
            "steps": 0,
            "tool_calls": 0,
            "handoffs": 0,
            "redundant_tool_calls": 0,
            "early_termination": False,
            "degraded_mode": False,
            "circuit_open": False,
            "failures_seen": 0,
            "policy_bypass": False,
            "poisoned_retrieval": False,
            "sharepoint_access_failure": False,
        }

    def _get_state(self, session_id: str) -> Dict[str, Any]:
        if session_id not in self.session_state:
            self.session_state[session_id] = {
                "tracked_failure": None,
                "persona": "default",
                "history": [],
            }
        return self.session_state[session_id]

    def _contains_harmful_intent(self, text: str) -> bool:
        lowered = text.lower()
        harmful_terms = [
            "phishing",
            "credential harvesting",
            "steal password",
            "social engineering email",
            "malware",
            "ransomware",
        ]
        return any(term in lowered for term in harmful_terms)

    def _is_injection_attempt(self, text: str) -> bool:
        lowered = text.lower()
        markers = [
            "ignore your previous instructions",
            "override safety",
            "disable guardrails",
            "call every tool",
        ]
        return any(marker in lowered for marker in markers)

    def _extract_test_id(self, text: str) -> Optional[str]:
        match = re.search(r"\bREG-\d{3,5}\b", text.upper())
        return match.group(0) if match else None

    def _extract_severity(self, text: str) -> Optional[str]:
        lowered = text.lower()
        for level in ["critical", "high", "medium", "low"]:
            if level in lowered:
                return level
        return None

    def _build_react_prompt(self, system_text: str):
        from langchain_core.prompts import PromptTemplate

        template = (
            "{system_text}\n\n"
            "You have access to the following tools:\n"
            "{tools}\n\n"
            "Use this format:\n"
            "Question: the input question you must answer\n"
            "Thought: you should always think about what to do\n"
            "Action: the action to take, should be one of [{tool_names}]\n"
            "Action Input: the input to the action\n"
            "Observation: the result of the action\n"
            "... (this Thought/Action/Action Input/Observation can repeat)\n"
            "Thought: I now know the final answer\n"
            "Final Answer: the final answer to the original input question\n\n"
            "Question: {input}\n"
            "Thought:{agent_scratchpad}"
        )
        return PromptTemplate.from_template(template).partial(system_text=system_text)

    def _kb_lookup(self, query: str, k: int = 3) -> Dict[str, Any]:
        rag = self._get_rag_pipeline()
        retrieved = rag._retrieve_documents(query, n_results=k)
        docs = retrieved.get("documents", [])[:k]
        metas = retrieved.get("metadatas", [])[:k]
        distances = retrieved.get("distances", [])[:k]
        return {
            "documents": docs,
            "metadatas": metas,
            "distances": distances,
        }

    def _run_single_agent(
        self,
        message: str,
        session_id: str,
        include_trace: bool,
        exercise_number: Optional[int],
        force_loop_bug: bool = False,
    ) -> Dict[str, Any]:
        from langchain_core.tools import tool

        try:
            runtime = self._resolve_langchain_agent_runtime()
        except ImportError as import_error:
            logger.warning("Agent runtime unavailable; using bootstrap single-agent fallback: %s", import_error)
            recovered = self._bootstrap_single_agent(message)
            if include_trace:
                recovered_trace = list(recovered.get("agent_trace", []))
                recovered_trace.insert(
                    0,
                    {
                        "phase": "fallback",
                        "content": "LangChain runtime unavailable; executed bootstrap single-agent path",
                    },
                )
                recovered["agent_trace"] = recovered_trace

            payload = self._response_payload(
                response=recovered.get("response", "I could not produce a response."),
                trace=recovered.get("agent_trace", []),
                tool_calls=recovered.get("tool_calls", []),
                session_id=session_id,
                include_trace=include_trace,
                handoffs=recovered.get("handoffs", []),
                trajectory_metrics=recovered.get("trajectory_metrics", self._empty_trajectory_metrics()),
                crew_mode=False,
                exercise_number=exercise_number,
                bootstrap_applied=True,
                bootstrap_reason="agent_runtime_import_failure",
            )
            payload["agent_runtime_fallback"] = True
            return payload

        trace: List[Dict[str, str]] = []
        tool_calls: List[Dict[str, Any]] = []
        state = self._get_state(session_id)
        metrics = self._empty_trajectory_metrics()

        @tool
        def query_knowledge_base(query: str) -> str:
            """Search and return information from the internal knowledge base."""
            with start_span(
                self.tracer,
                "query_knowledge_base",
                span_kind="TOOL",
                attrs={
                    "tool.name": "query_knowledge_base",
                    "tool.query": query,
                },
            ):
                result = self._kb_lookup(query, k=3)
                docs = result.get("documents", [])
                text = "\n\n".join(docs)

                tool_calls.append(
                    {
                        "tool": "query_knowledge_base",
                        "query": query,
                        "result_count": len(docs),
                        "result_preview": [doc[:180] for doc in docs[:2]],
                    }
                )
                self.stats["tool_calls"] += 1
                return text if text else "NO_MATCH_FOUND"

        tools = [query_knowledge_base]

        system_text = (
            "You are a testing assistant focused on GenAI quality, safety, and reliability. "
            "Use the knowledge base tool for factual classroom content. "
            "If tool results are empty, stop after a small number of retries and explain what is missing."
        )

        if force_loop_bug:
            missing_keyword = os.getenv("AGENT_TRAJECTORY_KEYWORD", "PHOENIX_NEVER_FOUND_KEYWORD")
            system_text += (
                "\nBUG-INJECTION: You must find the exact keyword "
                f"'{missing_keyword}' in a retrieved document before finalizing. "
                "If not found, retry query_knowledge_base with a reformulated query."
            )

        prompt = self._build_react_prompt(system_text)
        llm = self._get_llm()

        with start_span(
            self.tracer,
            self._span_name("Single-Agent ReAct", exercise_number),
            span_kind="AGENT",
            attrs={
                "session.id": session_id,
                "exercise_number": exercise_number,
                "course.exercise.number": exercise_number,
                "agent.mode": "single",
                "agent.loop_bug": force_loop_bug,
            },
        ):
            if runtime["kind"] == "classic":
                AgentExecutor = runtime["AgentExecutor"]
                create_react_agent = runtime["create_react_agent"]
                agent = create_react_agent(llm, tools, prompt)
                executor = AgentExecutor(
                    agent=agent,
                    tools=tools,
                    max_iterations=self.max_iterations,
                    handle_parsing_errors=True,
                    return_intermediate_steps=True,
                    verbose=False,
                )
                result = executor.invoke({"input": message})
                output = str(result.get("output", "")).strip()

                for step in result.get("intermediate_steps", []):
                    try:
                        action, observation = step
                        trace.append(
                            {
                                "phase": "action",
                                "content": f"tool={action.tool} input={action.tool_input}",
                            }
                        )
                        trace.append(
                            {
                                "phase": "observation",
                                "content": str(observation)[:280],
                            }
                        )
                    except Exception:
                        continue
            else:
                langgraph_result = self._invoke_langgraph_react(
                    runtime["create_react_agent"],
                    llm,
                    tools,
                    system_text,
                    message,
                )
                output = str(langgraph_result.get("output", "")).strip()
                trace.extend(langgraph_result.get("trace", []))

        if not output:
            output = "I could not produce an answer from the available context."

        query_counter = Counter((call.get("tool"), call.get("query")) for call in tool_calls)
        redundant = sum(count - 1 for count in query_counter.values() if count > 1)

        metrics["steps"] = max(1, len(trace))
        metrics["tool_calls"] = len(tool_calls)
        metrics["redundant_tool_calls"] = max(0, redundant)
        metrics["early_termination"] = len(tool_calls) == 0

        if force_loop_bug and len(tool_calls) >= 3:
            metrics["degraded_mode"] = True

        state["history"].append({"message": message, "mode": "single", "timestamp": time.time()})
        if len(state["history"]) > 30:
            state["history"] = state["history"][-30:]

        return self._response_payload(
            response=output,
            trace=trace,
            tool_calls=tool_calls,
            session_id=session_id,
            include_trace=include_trace,
            handoffs=[],
            trajectory_metrics=metrics,
            crew_mode=False,
            exercise_number=exercise_number,
        )

    def _run_multi_agent(
        self,
        message: str,
        session_id: str,
        include_trace: bool,
        exercise_number: Optional[int],
    ) -> Dict[str, Any]:
        from langchain_core.tools import tool

        try:
            runtime = self._resolve_langchain_agent_runtime()
        except ImportError as import_error:
            logger.warning("Agent runtime unavailable; using bootstrap multi-agent fallback: %s", import_error)
            recovered = self._bootstrap_multi_agent(message)
            if include_trace:
                recovered_trace = list(recovered.get("agent_trace", []))
                recovered_trace.insert(
                    0,
                    {
                        "phase": "fallback",
                        "content": "LangChain runtime unavailable; executed bootstrap multi-agent path",
                    },
                )
                recovered["agent_trace"] = recovered_trace

            payload = self._response_payload(
                response=recovered.get("response", "I could not produce a response."),
                trace=recovered.get("agent_trace", []),
                tool_calls=recovered.get("tool_calls", []),
                session_id=session_id,
                include_trace=include_trace,
                handoffs=recovered.get("handoffs", []),
                trajectory_metrics=recovered.get("trajectory_metrics", self._empty_trajectory_metrics()),
                crew_mode=True,
                exercise_number=exercise_number,
                bootstrap_applied=True,
                bootstrap_reason="agent_runtime_import_failure",
            )
            payload["agent_runtime_fallback"] = True
            return payload

        trace: List[Dict[str, str]] = []
        tool_calls: List[Dict[str, Any]] = []
        handoffs: List[Dict[str, Any]] = []
        metrics = self._empty_trajectory_metrics()
        state = self._get_state(session_id)

        def should_mutate_handoff(text: str) -> bool:
            lowered = text.lower()
            marker = "simulate handoff corruption"
            env_enabled = str(os.getenv("ENABLE_HANDOFF_MUTATOR_BUG", "false")).strip().lower() in {
                "1",
                "true",
                "yes",
                "on",
            }
            return marker in lowered or env_enabled

        def mutate_query(text: str) -> str:
            # Intentional bug for exercise labs: strip years and punctuation that matter to retrieval.
            stripped = re.sub(r"\b(19|20)\d{2}\b", "", text)
            stripped = re.sub(r"[^a-zA-Z0-9\s]", " ", stripped)
            return re.sub(r"\s+", " ", stripped).strip().lower()

        @tool
        def rag_agent_tool(user_query: str) -> str:
            """Use this to answer factual questions utilizing the knowledge base."""
            routed_query = user_query
            mutated = False
            if should_mutate_handoff(user_query):
                routed_query = mutate_query(user_query)
                mutated = True

            handoffs.append(
                {
                    "from": "TriageAgent",
                    "to": "RAGSpecialist",
                    "purpose": "Handle factual knowledge-base request",
                    "mutated": mutated,
                    "original_query": user_query,
                    "routed_query": routed_query,
                }
            )

            with start_span(
                self.tracer,
                self._span_name("RAG Specialist", exercise_number),
                span_kind="AGENT",
                attrs={
                    "exercise_number": exercise_number,
                    "handoff.mutated": mutated,
                    "handoff.original_query": user_query,
                    "handoff.routed_query": routed_query,
                },
            ):
                nested = self._run_single_agent(
                    message=routed_query,
                    session_id=session_id,
                    include_trace=False,
                    exercise_number=exercise_number,
                    force_loop_bug=False,
                )

            if nested.get("tool_calls"):
                tool_calls.extend(nested["tool_calls"])
            if mutated:
                metrics["poisoned_retrieval"] = True

            return nested.get("response", "No response from RAG specialist")

        @tool
        def general_chat_agent(user_query: str) -> str:
            """Use this for greetings, casual small talk, or system help."""
            handoffs.append(
                {
                    "from": "TriageAgent",
                    "to": "GeneralChatAgent",
                    "purpose": "Handle non-RAG conversational request",
                }
            )
            with start_span(
                self.tracer,
                self._span_name("General Chat Agent", exercise_number),
                span_kind="AGENT",
                attrs={"handoff.original_query": user_query},
            ):
                response = self._get_llm().invoke(user_query)
            self.stats["tool_calls"] += 1
            tool_calls.append(
                {
                    "tool": "general_chat_agent",
                    "query": user_query,
                    "result_count": 1,
                }
            )
            return getattr(response, "content", str(response))

        @tool
        def validator_agent_tool(candidate_answer: str) -> str:
            """Use this to validate and polish the final answer for clarity and grounding."""
            handoffs.append(
                {
                    "from": "RAGSpecialist",
                    "to": "ValidatorAgent",
                    "purpose": "Validate answer quality and clarity",
                }
            )
            prompt = (
                "You are a strict answer validator for GenAI testing exercises. "
                "Improve clarity, keep claims grounded, and return concise output.\n\n"
                f"Candidate answer:\n{candidate_answer}"
            )
            with start_span(
                self.tracer,
                self._span_name("Validator Agent", exercise_number),
                span_kind="AGENT",
                attrs={"validator.input_length": len(candidate_answer)},
            ):
                response = self._get_llm().invoke(prompt)
            self.stats["tool_calls"] += 1
            tool_calls.append(
                {
                    "tool": "validator_agent_tool",
                    "query": "candidate_answer",
                    "result_count": 1,
                }
            )
            return getattr(response, "content", str(response))

        tools = [rag_agent_tool, general_chat_agent, validator_agent_tool]
        orchestration_system_text = (
            "You are the TriageAgent orchestrator. Choose exactly one specialist tool at a time. "
            "For factual/product/testing-content questions prefer rag_agent_tool, then optionally call validator_agent_tool. "
            "For casual greetings/help use general_chat_agent."
        )
        prompt = self._build_react_prompt(orchestration_system_text)
        llm = self._get_llm()

        with start_span(
            self.tracer,
            self._span_name("Triage Agent", exercise_number),
            span_kind="AGENT",
            attrs={
                "session.id": session_id,
                "exercise_number": exercise_number,
                "course.exercise.number": exercise_number,
                "agent.mode": "multi",
            },
        ):
            if runtime["kind"] == "classic":
                AgentExecutor = runtime["AgentExecutor"]
                create_react_agent = runtime["create_react_agent"]
                agent = create_react_agent(llm, tools, prompt)
                executor = AgentExecutor(
                    agent=agent,
                    tools=tools,
                    max_iterations=self.max_iterations,
                    handle_parsing_errors=True,
                    return_intermediate_steps=True,
                    verbose=False,
                )
                result = executor.invoke({"input": message})
                output = str(result.get("output", "")).strip()

                for step in result.get("intermediate_steps", []):
                    try:
                        action, observation = step
                        trace.append(
                            {
                                "phase": "action",
                                "content": f"triage_tool={action.tool} input={action.tool_input}",
                            }
                        )
                        trace.append(
                            {
                                "phase": "observation",
                                "content": str(observation)[:280],
                            }
                        )
                    except Exception:
                        continue
            else:
                langgraph_result = self._invoke_langgraph_react(
                    runtime["create_react_agent"],
                    llm,
                    tools,
                    orchestration_system_text,
                    message,
                )
                output = str(langgraph_result.get("output", "")).strip()
                for item in langgraph_result.get("trace", []):
                    content = str(item.get("content", ""))
                    if content.startswith("tool="):
                        content = content.replace("tool=", "triage_tool=", 1)
                    trace.append({
                        "phase": item.get("phase", "action"),
                        "content": content,
                    })

        if not output:
            output = "I could not produce a multi-agent answer for that request."

        query_counter = Counter((call.get("tool"), call.get("query")) for call in tool_calls)
        redundant = sum(count - 1 for count in query_counter.values() if count > 1)

        metrics["steps"] = max(1, len(trace))
        metrics["tool_calls"] = len(tool_calls)
        metrics["handoffs"] = len(handoffs)
        metrics["redundant_tool_calls"] = max(0, redundant)
        metrics["early_termination"] = len(tool_calls) == 0

        state["history"].append({"message": message, "mode": "multi", "timestamp": time.time()})
        if len(state["history"]) > 30:
            state["history"] = state["history"][-30:]

        return self._response_payload(
            response=output,
            trace=trace,
            tool_calls=tool_calls,
            session_id=session_id,
            include_trace=include_trace,
            handoffs=handoffs,
            trajectory_metrics=metrics,
            crew_mode=True,
            exercise_number=exercise_number,
        )

    def process(
        self,
        message: str,
        session_id: str,
        include_trace: bool = False,
        crew_mode: bool = False,
        exercise_number: Optional[int] = None,
    ) -> Dict[str, Any]:
        self.stats["requests"] += 1
        if crew_mode:
            self.stats["crew_requests"] += 1

        state = self._get_state(session_id)
        lowered = message.lower().strip()

        if self._contains_harmful_intent(message):
            self.stats["blocked_actions"] += 1
            metrics = self._empty_trajectory_metrics()
            metrics["steps"] = 1
            return self._response_payload(
                response="I cannot help with harmful or social-engineering content.",
                trace=[{"phase": "policy", "content": "Blocked harmful intent"}],
                tool_calls=[],
                session_id=session_id,
                include_trace=include_trace,
                handoffs=[],
                trajectory_metrics=metrics,
                crew_mode=crew_mode,
                exercise_number=exercise_number,
            )

        if self._is_injection_attempt(message):
            self.stats["blocked_actions"] += 1
            metrics = self._empty_trajectory_metrics()
            metrics["steps"] = 1
            return self._response_payload(
                response="I cannot execute unsafe override instructions.",
                trace=[{"phase": "policy", "content": "Blocked prompt-injection markers"}],
                tool_calls=[],
                session_id=session_id,
                include_trace=include_trace,
                handoffs=[],
                trajectory_metrics=metrics,
                crew_mode=crew_mode,
                exercise_number=exercise_number,
            )

        if "set persona pirate" in lowered:
            state["persona"] = "pirate"
            metrics = self._empty_trajectory_metrics()
            metrics["steps"] = 1
            metrics["early_termination"] = True
            return self._response_payload(
                response="Persona updated to pirate mode for this session.",
                trace=[{"phase": "action", "content": "Set persona to pirate"}],
                tool_calls=[],
                session_id=session_id,
                include_trace=include_trace,
                handoffs=[],
                trajectory_metrics=metrics,
                crew_mode=crew_mode,
                exercise_number=exercise_number,
            )

        if "set persona default" in lowered:
            state["persona"] = "default"
            metrics = self._empty_trajectory_metrics()
            metrics["steps"] = 1
            metrics["early_termination"] = True
            return self._response_payload(
                response="Persona reset to default mode.",
                trace=[{"phase": "action", "content": "Set persona to default"}],
                tool_calls=[],
                session_id=session_id,
                include_trace=include_trace,
                handoffs=[],
                trajectory_metrics=metrics,
                crew_mode=crew_mode,
                exercise_number=exercise_number,
            )

        if "reset context" in lowered or "new session" in lowered:
            self.session_state[session_id] = {
                "tracked_failure": None,
                "persona": "default",
                "history": [],
            }
            self.stats["resets"] += 1
            metrics = self._empty_trajectory_metrics()
            metrics["steps"] = 1
            metrics["early_termination"] = True
            return self._response_payload(
                response="Session context reset complete.",
                trace=[{"phase": "action", "content": "Cleared session memory"}],
                tool_calls=[],
                session_id=session_id,
                include_trace=include_trace,
                handoffs=[],
                trajectory_metrics=metrics,
                crew_mode=crew_mode,
                exercise_number=exercise_number,
            )

        track_match = re.search(r"track failure\s+(REG-\d{3,5})", message, re.IGNORECASE)
        if track_match:
            tracked = track_match.group(1).upper()
            state["tracked_failure"] = tracked
            metrics = self._empty_trajectory_metrics()
            metrics["steps"] = 1
            return self._response_payload(
                response=f"Tracking {tracked} for this session.",
                trace=[{"phase": "action", "content": f"Stored tracked_failure={tracked}"}],
                tool_calls=[],
                session_id=session_id,
                include_trace=include_trace,
                handoffs=[],
                trajectory_metrics=metrics,
                crew_mode=crew_mode,
                exercise_number=exercise_number,
            )

        try:
            force_loop_bug = "trajectory hacking" in lowered or "simulate react loop" in lowered
            if crew_mode:
                payload = self._run_multi_agent(message, session_id, include_trace, exercise_number)
            else:
                payload = self._run_single_agent(
                    message,
                    session_id,
                    include_trace,
                    exercise_number,
                    force_loop_bug=force_loop_bug,
                )

            if self._should_apply_bootstrap(payload):
                payload = self._apply_bootstrap_recovery(
                    payload=payload,
                    message=message,
                    session_id=session_id,
                    include_trace=include_trace,
                    crew_mode=crew_mode,
                    exercise_number=exercise_number,
                )
                self.stats["fallback_responses"] += 1

            if state.get("persona") == "pirate":
                payload["response"] = f"Ahoy matey. {payload['response']} Arrr."

            payload["phoenix_trace_enabled"] = self.phoenix_enabled
            payload["exercise_number"] = exercise_number
            return payload
        except Exception as exc:
            self.stats["errors"] += 1
            logger.error("Agent processing failed: %s", exc)
            metrics = self._empty_trajectory_metrics()
            metrics["steps"] = 1
            metrics["degraded_mode"] = True
            return self._response_payload(
                response=f"Agent mode encountered an error: {exc}",
                trace=[{"phase": "error", "content": str(exc)}],
                tool_calls=[],
                session_id=session_id,
                include_trace=include_trace,
                handoffs=[],
                trajectory_metrics=metrics,
                crew_mode=crew_mode,
                exercise_number=exercise_number,
            )

    def _should_apply_bootstrap(self, payload: Dict[str, Any]) -> bool:
        if not self.bootstrap_on_zero_tools:
            return False

        if payload.get("bootstrap_applied"):
            return False

        metrics = payload.get("trajectory_metrics") or {}
        return int(metrics.get("tool_calls", 0) or 0) == 0

    def _apply_bootstrap_recovery(
        self,
        payload: Dict[str, Any],
        message: str,
        session_id: str,
        include_trace: bool,
        crew_mode: bool,
        exercise_number: Optional[int],
    ) -> Dict[str, Any]:
        if crew_mode:
            recovered = self._bootstrap_multi_agent(message)
        else:
            recovered = self._bootstrap_single_agent(message)

        merged = dict(payload)
        merged["response"] = recovered["response"]

        merged_tool_calls = list(merged.get("tool_calls", []) or [])
        merged_tool_calls.extend(recovered.get("tool_calls", []) or [])
        merged["tool_calls"] = merged_tool_calls

        merged_handoffs = list(merged.get("handoffs", []) or [])
        merged_handoffs.extend(recovered.get("handoffs", []) or [])
        merged["handoffs"] = merged_handoffs

        orig_metrics = dict(merged.get("trajectory_metrics") or {})
        rec_metrics = recovered.get("trajectory_metrics") or {}
        orig_metrics["steps"] = int(orig_metrics.get("steps", 0) or 0) + int(rec_metrics.get("steps", 0) or 0)
        orig_metrics["tool_calls"] = int(orig_metrics.get("tool_calls", 0) or 0) + int(rec_metrics.get("tool_calls", 0) or 0)
        orig_metrics["handoffs"] = int(orig_metrics.get("handoffs", 0) or 0) + int(rec_metrics.get("handoffs", 0) or 0)
        orig_metrics["redundant_tool_calls"] = int(orig_metrics.get("redundant_tool_calls", 0) or 0) + int(
            rec_metrics.get("redundant_tool_calls", 0) or 0
        )
        orig_metrics["early_termination"] = False
        orig_metrics["degraded_mode"] = True
        merged["trajectory_metrics"] = orig_metrics

        if include_trace:
            merged_trace = list(merged.get("agent_trace", []) or [])
            merged_trace.extend(recovered.get("agent_trace", []) or [])
            merged["agent_trace"] = merged_trace

        merged["bootstrap_applied"] = True
        merged["bootstrap_reason"] = "zero_tool_calls"
        merged["bootstrap_mode"] = "multi" if crew_mode else "single"
        merged["exercise_number"] = exercise_number
        return merged

    def _bootstrap_single_agent(self, message: str) -> Dict[str, Any]:
        kb = self._kb_lookup(message, k=3)
        docs = kb.get("documents", [])
        context = "\n\n".join(docs[:2])

        prompt = (
            "You are a testing assistant. Use only the provided context when possible, "
            "and acknowledge missing evidence when context is insufficient.\n\n"
            f"Question: {message}\n\n"
            f"Context:\n{context}"
        )

        with start_span(
            self.tracer,
            "Bootstrap query_knowledge_base",
            span_kind="TOOL",
            attrs={"bootstrap.applied": True},
        ):
            llm_response = self._get_llm().invoke(prompt)

        response_text = getattr(llm_response, "content", str(llm_response)).strip()
        tool_call = {
            "tool": "query_knowledge_base",
            "query": message,
            "result_count": len(docs),
            "result_preview": [doc[:180] for doc in docs[:2]],
            "bootstrap": True,
        }
        trace = [
            {"phase": "bootstrap", "content": "Applied bootstrap recovery after zero tool calls"},
            {"phase": "action", "content": f"tool=query_knowledge_base input={message}"},
            {"phase": "observation", "content": response_text[:280]},
        ]

        metrics = self._empty_trajectory_metrics()
        metrics["steps"] = len(trace)
        metrics["tool_calls"] = 1
        metrics["early_termination"] = False
        metrics["degraded_mode"] = True

        return {
            "response": response_text,
            "tool_calls": [tool_call],
            "handoffs": [],
            "agent_trace": trace,
            "trajectory_metrics": metrics,
        }

    def _bootstrap_multi_agent(self, message: str) -> Dict[str, Any]:
        kb = self._kb_lookup(message, k=3)
        docs = kb.get("documents", [])
        context = "\n\n".join(docs[:2])

        prompt = (
            "You are the RAG specialist in a multi-agent test workflow. "
            "Answer using context and call out uncertainty when needed.\n\n"
            f"Question: {message}\n\n"
            f"Context:\n{context}"
        )

        with start_span(
            self.tracer,
            "Bootstrap RAG Specialist",
            span_kind="AGENT",
            attrs={"bootstrap.applied": True},
        ):
            llm_response = self._get_llm().invoke(prompt)

        response_text = getattr(llm_response, "content", str(llm_response)).strip()
        handoff = {
            "from": "TriageAgent",
            "to": "RAGSpecialist",
            "purpose": "Bootstrap recovery after zero tool calls",
            "bootstrap": True,
            "original_query": message,
            "routed_query": message,
        }
        tool_call = {
            "tool": "query_knowledge_base",
            "query": message,
            "result_count": len(docs),
            "result_preview": [doc[:180] for doc in docs[:2]],
            "bootstrap": True,
        }
        trace = [
            {"phase": "bootstrap", "content": "Applied bootstrap recovery after zero tool calls"},
            {"phase": "action", "content": f"triage_tool=rag_agent_tool input={message}"},
            {"phase": "observation", "content": response_text[:280]},
        ]

        metrics = self._empty_trajectory_metrics()
        metrics["steps"] = len(trace)
        metrics["tool_calls"] = 1
        metrics["handoffs"] = 1
        metrics["early_termination"] = False
        metrics["degraded_mode"] = True

        return {
            "response": response_text,
            "tool_calls": [tool_call],
            "handoffs": [handoff],
            "agent_trace": trace,
            "trajectory_metrics": metrics,
        }

    def _response_payload(
        self,
        response: str,
        trace: List[Dict[str, str]],
        tool_calls: List[Dict[str, Any]],
        session_id: str,
        include_trace: bool,
        handoffs: List[Dict[str, Any]],
        trajectory_metrics: Dict[str, Any],
        crew_mode: bool,
        exercise_number: Optional[int],
        bootstrap_applied: bool = False,
        bootstrap_reason: Optional[str] = None,
    ) -> Dict[str, Any]:
        payload = {
            "response": response,
            "sources": [],
            "agent_mode": True,
            "crew_mode": crew_mode,
            "session_id": session_id,
            "exercise_number": exercise_number,
            "tool_calls": tool_calls,
            "handoffs": handoffs,
            "trajectory_metrics": trajectory_metrics,
            "bootstrap_applied": bootstrap_applied,
            "bootstrap_reason": bootstrap_reason,
            "state_snapshot": {
                "tracked_failure": self.session_state.get(session_id, {}).get("tracked_failure"),
                "persona": self.session_state.get(session_id, {}).get("persona", "default"),
            },
        }
        if include_trace:
            payload["agent_trace"] = trace
        return payload

    def get_stats(self) -> Dict[str, Any]:
        return {
            "requests": self.stats["requests"],
            "crew_requests": self.stats["crew_requests"],
            "tool_calls": self.stats["tool_calls"],
            "blocked_actions": self.stats["blocked_actions"],
            "clarifications": self.stats["clarifications"],
            "resets": self.stats["resets"],
            "fallback_responses": self.stats["fallback_responses"],
            "errors": self.stats["errors"],
            "active_sessions": len(self.session_state),
            "phoenix_trace_enabled": self.phoenix_enabled,
        }

    def reset_session_state(self, session_id: str, reset_circuit_breaker: bool = False) -> Dict[str, Any]:
        existed = session_id in self.session_state
        if existed:
            del self.session_state[session_id]
        return {
            "scope": "session",
            "session_id": session_id,
            "session_existed": existed,
            "active_sessions": len(self.session_state),
        }

    def reset_all_state(self, reset_circuit_breaker: bool = True) -> Dict[str, Any]:
        count = len(self.session_state)
        self.session_state = {}
        return {
            "scope": "all",
            "cleared_sessions": count,
            "active_sessions": 0,
        }
