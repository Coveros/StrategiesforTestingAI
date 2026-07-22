# Observability Audit: OpenInference Fields for Modules 6-8

## Current Status

### ✅ Currently Captured (Free/Standard OpenInference)
- `session.id` — Session correlation
- `agent.mode` — single vs multi
- `exercise_number` — Course context
- `llm.model_name` — Model identifier
- `llm.invocation_parameters.temperature` — Temperature setting
- `llm.messages.0.content` — Input prompts
- `llm.prompts.0` — Full prompt text
- `llm.completions.0.content` — Output text
- `llm.completions.0.finish_reason` — stop/error/timeout
- `llm.usage.prompt_tokens` — Token count (input)
- `llm.usage.completion_tokens` — Token count (output)
- `llm.usage.total_tokens` — Total tokens
- `tool.name` — Tool identifier
- `tool.input` — Tool input parameters
- `tool.output` — Tool output/result
- `tool.execution_result` — success/error
- `input.value` (NEW) — Chain input data
- `output.value` (NEW) — Chain output data
- **Automatic spans:** duration, start/end time, error status

### ❌ Missing for Module 6 (Handoff Diagnostics)
- `handoff.source_agent` — Agent sending data
- `handoff.target_agent` — Agent receiving data
- `handoff.query_original` — Original query before mutation
- `handoff.query_received` — Query received by target
- `handoff.mutation_detected` — Boolean: did query change?
- `handoff.mutation_type` — truncation, substitution, etc.
- `user.id` or `request.id` — Request correlation across handoffs
- `session.user_id` — Student/user identifier

### ❌ Missing for Module 7 (NFR Testing)
- `agent.iterations_used` — Actual steps taken
- `agent.max_iterations_allowed` — Configured limit
- `agent.loop_detected` — Boolean: did loop occur?
- `retrieval.documents_returned` — Count of docs returned
- `retrieval.top_similarity_score` — Best match score
- `retrieval.average_similarity_score` — Mean relevance
- `llm.cost.estimated_usd` — Cost per inference (if pricing available)
- `throughput.requests_per_minute` — For batch analysis
- `error.latency_exceeded` — Timeout detection
- `error.tokens_exceeded` — Token limit breach

### ❌ Missing for Module 8 (Red Team / Security)
- `security.decision` — allowed / blocked / flagged
- `security.reason` — Why blocked (e.g., "injection marker", "harmful intent")
- `security.severity` — critical / high / medium / low
- `guardrail.layer` — input / output / logic
- `guardrail.check_name` — "content_filter", "prompt_injection", etc.
- `injection_attempt_detected` — Boolean
- `injection_markers` — Detected patterns
- `error.type` — timeout / injection / validation / tool_error
- `error.category` — For classification (security vs operational)
- `error.recoverable` — Can system recover?
- `trajectory.depth` — Span tree complexity
- `trajectory.redundant_calls` — Duplicate tool invocations
- `persona.shift_detected` — Config drift indicator

## Implementation Plan

### Phase 1: Handoff Metadata (Module 6)
Add to chain callbacks:
- Extract agent names from span name or serialized metadata
- Compare input.value vs output.value for mutation detection
- Emit `handoff.*` attributes on chain spans

### Phase 2: NFR Metrics (Module 7)
Add to agent execution context:
- Track iteration count during agent loop
- Capture retrieval document counts and scores
- Add error classification for timeouts/limits

### Phase 3: Security Fields (Module 8)
Add to process method and error handling:
- Classify security decisions (input/output guardrails)
- Emit error types and recovery status
- Track injection attempt patterns

## OpenInference Standards Used
- OpenInference Semantic Conventions v0.1.0
- Agent/Agentic trace shape
- LLM/Tool span hierarchy
- Error classification standards
