# Observability Enhancements Summary

## What Was Added

### ✅ Module 6 - Handoff Diagnostics
**New Spans & Attributes:**
- `agent.role` — Identifies handoff source (triage, rag_specialist, validator)
- `input.value` — Original query entering an agent
- `output.value` — Result produced by an agent
- Enables side-by-side comparison: `Parent output` vs `Child input` to detect mutations

**How to Use in Phoenix:**
1. Run a multi-agent prompt
2. Click on each span in the chain
3. Compare `input.value` (what it received) vs `output.value` (what it produced)
4. Check if Triage Agent's output matches RAG Specialist's input

### ✅ Module 7 - NFR Testing
**New Attributes:**
- `tool.is_retrieval` — Boolean flag for retrieval tools
- `retrieval.documents_returned` — Count of documents in retrieval result
- `error.type` — Classified error types (timeout, rate_limit, validation_error, auth_error)
- `error.message` — Full error text for debugging
- **Automatic:** Span duration (latency), token counts (already captured)

**How to Use in Phoenix:**
1. Filter traces for retrieval tool spans
2. Check `retrieval.documents_returned` count
3. Compare `error.type` across runs to identify failure patterns
4. Span duration shows latency overhead

### ✅ Module 8 - Red Team / Security Analysis
**New Root Span: `security.gate.ex#`**
Captures every request's security decision:
- `security.decision` — allowed / blocked / flagged
- `security.reason` — Why blocked (harmful_intent_detected, prompt_injection_detected, passed_all_gates)
- `security.severity` — critical / high / medium / low
- `security.layer` — input_validation / output_validation
- `injection_markers_detected` — Boolean for prompt injection attempts

**New Tool Error Classification:**
- `error.type` — tool_execution_failed / not_found / timeout / connection_error / permission_denied
- Classified automatically based on error message patterns

**How to Use in Phoenix:**
1. Look for `security.gate.ex8` spans in your traces
2. Students attempting injection will see: `security.decision=blocked, reason=prompt_injection_detected`
3. Students attempting harmful requests will see: `security.decision=blocked, reason=harmful_intent_detected`
4. Successful requests will show: `security.decision=allowed`

## OpenInference Standards Compliance

All attributes follow OpenInference v0.1.0 conventions:
- `security.*` — Custom security classification (not in base standard)
- `error.*` — Error classification
- `llm.*` — LLM instrumentation (standard)
- `tool.*` — Tool execution (standard)
- `input.value` / `output.value` — Message passing (standard)
- `retrieval.*` — Retrieval metrics (standard)

## What's Still Missing (Optional for Future)

Low-priority enhancements (not free/automatic):
- `llm.cost.estimated_usd` — Requires token pricing data
- `agent.iterations_used` / `agent.max_iterations` — Requires explicit loop tracking
- `handoff.schema_validation` — Requires schema registry
- `trajectory.redundant_calls` — Requires pattern analysis
- `user.id` / `request.id` — Requires request correlation in Flask

## How to Access in Phoenix

### Finding Security Spans:
1. Open Phoenix → Traces tab
2. Filter by span name: search for `security.gate`
3. Click to see: decision, reason, severity

### Finding Handoff Spans:
1. Look for `agent.chain` spans with `agent.role` attribute
2. Compare adjacent spans in tree to detect mutations

### Finding Error Spans:
1. Look for spans with orange/red error indicators
2. Check `error.type` and `error.message` attributes
3. Trace patterns across multiple runs

## Testing These Changes

Run a prompt now and observe:
```bash
# Terminal 1: Flask with warmup
python run.py

# Terminal 2: Generate traces (or use UI manually)
python generate_classroom_traces.py
```

In Phoenix (http://localhost:6006):
- Look for `security.gate.ex6` spans (one per request)
- Look for nested `agent.chain` spans with `agent.role` attributes
- Look for error classification in tool spans
