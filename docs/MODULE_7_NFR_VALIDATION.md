# Module 7 NFR Testing: Phoenix Setup & Exercise Validation

## Executive Summary

✅ **Your Module 7 concepts are well-aligned with Phoenix observability and our current instrumentation.** All major NFR categories (robustness, graceful degradation, latency, cost) are observable and testable. However, **Exercise 7 does not yet exist**—we need to create it to support hands-on NFR testing.

---

## Module 7 Concepts vs. Current Observability

### 1. Robustness & Resiliency ✅ FULLY OBSERVABLE

**Your concepts:**
- Maintain performance despite noisy inputs or model variability
- Dependency breaks (500 errors, timeouts from LLM/Vector DB)
- Graceful degradation & fallbacks

**What we currently capture in Phoenix:**
- ✅ **Error spans**: Exception events recorded via `span.record_exception(error)`
- ✅ **Timeout tracking**: `ollama_timeout_seconds` configured, timeouts visible in span latency
- ✅ **Error metadata**: Logged via logger.error() and captured in trace
- ✅ **Fallback status**: Can emit attributes like `app.fallback_triggered=true` on error paths

**What students see in Phoenix:**
- Error spans in Traces tab with exception details
- LLM spans with `error=true` attribute
- Tool spans showing `tool.execution_result=error`
- Downstream spans showing `null` parameters or "no data" responses

**Example student analysis:**
"Filter for spans with `error=true`. Compare 3 error types: timeout (60s+), empty payload (null), rate limit (429 status). Document how each degrades."

---

### 2. API Failures & Dependency Breaks ✅ FULLY OBSERVABLE

**Your concepts:**
- Telemetry exception capture (500 errors from OpenAI, Anthropic, Vector DB)
- Empty payloads validation
- Rate-limit rejection (HTTP 429 + Retry-After headers)

**Current instrumentation:**

[app/rag_pipeline.py](app/rag_pipeline.py):
```python
# Error recovery for Chroma initialization failures
except BaseException as init_error:
    error_text = str(init_error)
    recoverable_markers = ("default_tenant", "range start index", "PanicException")
    if any(marker in error_text for marker in recoverable_markers):
        # Backup and recover
```

[app/agentic_testops.py](app/agentic_testops.py):
```python
def on_tool_error(self, error: BaseException, run_id: Any = None, **kwargs: Any) -> Any:
    run_id = run_id or kwargs.get("run_id")
    self._end(run_id, error=error)  # Captures exception in span
```

**What students see in Phoenix:**
- ✅ Tool error spans with exception details
- ✅ LLM completion failures with empty response
- ⚠️ **Missing**: Explicit `http.status_code=429` attribute or `retry_after` header capture

**Recommendation:**
Add HTTP status code to LLM/tool spans:
```python
span.set_attribute("http.status_code", response.status_code)
if status_code == 429:
    span.set_attribute("http.response.header.retry_after", retry_after_seconds)
```

---

### 3. Graceful Degradation ✅ PARTIALLY OBSERVABLE

**Your concepts:**
- Model fallbacks (GPT-4 → GPT-3.5 or Llama)
- Static fallbacks (hard-coded responses)
- Circuit breaker triggers

**Current status:**
- ✅ Warmup completion tracked: `self.stats['warmup_completed']`
- ✅ Error tracking: `self.stats['errors']` counter
- ⚠️ **Missing**: No fallback chain implementation in code
- ⚠️ **Missing**: No circuit breaker pattern

**What students see in Phoenix:**
- Span showing first failure
- But no span showing fallback path triggered
- No attribute like `app.fallback_model=llama` or `circuit_breaker.state=OPEN`

**Recommendation:**
Add simple fallback tracking:
```python
# In rag_pipeline.py _generate_response on error:
try:
    response = requests.post(..., timeout=self.ollama_timeout_seconds)
except requests.Timeout:
    gen_span.set_attribute("llm.fallback.triggered", True)
    gen_span.set_attribute("llm.fallback.reason", "primary_timeout")
    gen_span.set_attribute("llm.fallback.model", "static_response")
    return "I encountered a brief connectivity issue. Try again in a moment."
```

---

### 4. Latency Metrics ✅ FULLY OBSERVABLE

**Your concepts:**
- **TTFT** (Time to First Token): Duration before first token generated
- **TBT** (Time Between Tokens): Generation smoothness
- **TTT** (Trace Total Time): End-to-end multi-step latency

**Current instrumentation:**
- ✅ **Span duration**: Phoenix automatically captures start/end time per span
- ✅ **Trace duration**: Sum of all spans visible in Phoenix trace graph
- ⚠️ **Missing**: No explicit TTFT/TBT attributes (streaming not implemented)

**What students see in Phoenix:**
- Trace details showing: "Duration: 42.3s"
- Per-span latencies: LLM span (30s), retrieval span (2s), generation span (10s)
- Latency Percentiles dashboard (if configured)

**What students can calculate:**
- TTT = sum of all span durations
- TTFT = latency of first LLM span start to first completion token (no explicit field, but visible in span timeline)

**Example student task:**
"In Phoenix Traces tab, find the slowest trace in your 12-trace batch from Exercise 6. Calculate TTT and identify the bottleneck span."

---

### 5. Throughput & Concurrency ⚠️ PARTIALLY OBSERVABLE

**Your concepts:**
- **TPM** (Tokens Per Minute): Stress test against provider limits
- **RPM** (Requests Per Minute): Concurrent users
- **Queue Management**: Prioritization under load
- **Latency degradation**: Concurrency → higher latency

**Current status:**
- ✅ Token counts captured: `llm.usage.prompt_tokens`, `llm.usage.completion_tokens`
- ⚠️ **Missing**: No TPM metric in traces
- ⚠️ **Missing**: No concurrent request handling; app is single-threaded
- ⚠️ **Missing**: No queue management or prioritization

**What students CAN observe:**
- Token usage per single request
- But NOT TPM aggregated across requests

**What students CANNOT easily test:**
- Concurrent user load (requires custom test harness)
- Queue behavior (not implemented)
- RPM limits

**Recommendation for Exercise 7:**
Create a stress test script that fires sequential requests and logs TPM:
```python
# section7_nfr_quickrun.py (existing pattern)
# or Exercise-7.md hands-on lab
# Task: Run 60 requests in sequence, calculate tokens/minute
```

---

### 6. Cost & Token Economics ✅ FULLY OBSERVABLE

**Your concepts:**
- Prompt vs completion token breakdown
- Agent loop tax (redundant tool calls)
- Cost rollups by model
- Cache hit rate

**Current instrumentation:**

[app/rag_pipeline.py](app/rag_pipeline.py#L603):
```python
gen_span.set_attribute("llm.usage.prompt_tokens", int(prompt_eval_count))
gen_span.set_attribute("llm.usage.completion_tokens", int(eval_count))
gen_span.set_attribute("llm.usage.total_tokens", int(eval_count) + int(prompt_eval_count))
```

[app/agentic_testops.py](app/agentic_testops.py#L175):
```python
span.set_attribute("llm.usage.prompt_tokens", int(prompt_tokens))
span.set_attribute("llm.usage.completion_tokens", int(completion_tokens))
```

**What students see in Phoenix:**
- ✅ Each span shows `llm.usage.*_tokens` attributes
- ✅ Token counts accumulate across trace spans
- ⚠️ **Missing**: Estimated cost in USD (requires pricing metadata)
- ⚠️ **Missing**: Loop detection (how many redundant iterations)

**What students CAN calculate:**
- Total tokens per trace: sum of all `llm.usage.total_tokens`
- Prompt vs completion ratio: compare prompt_tokens to completion_tokens
- "Loop tax": count repeated tool calls and their token cost

**What students CANNOT directly see:**
- Estimated USD cost per trace (Phoenix has this if we provide pricing)
- Cache hit rate (no cache implemented for local Ollama)

**Recommendation for Exercise 7:**
Add simple cost estimation attribute:
```python
# In agentic_testops.py or rag_pipeline.py
# Ollama is local/free, but track as if it had cost
# Example: Llama pricing ~ $0.05 per 1M input + $0.15 per 1M output (rough estimate)
estimated_cost_usd = (prompt_tokens / 1e6 * 0.05) + (completion_tokens / 1e6 * 0.15)
span.set_attribute("llm.cost.estimated_usd", round(estimated_cost_usd, 6))
```

---

### 7. AI Fuzzing & Stress Testing ⚠️ NOT YET IMPLEMENTED

**Your concepts:**
- Character-level perturbation (typos, leetspeak)
- Phrase-level perturbation (reordering, tone changes)
- Negative fuzzing (contradictory facts)
- Tools: Giskard, TextAttack, Promptfoo

**Current status:**
- ⚠️ **No fuzzing infrastructure** in app
- ✅ Robustness can be tested with generate_classroom_traces.py (which uses 4 question variations)
- ⚠️ **Missing**: Automated perturbation engine

**What students CAN do today:**
- Part 1 of Exercise 6 (classroom demo) tests 4 robustness variations manually
- Students could manually type variations and compare traces

**What students CANNOT easily do:**
- Automated 1000-variation fuzz runs
- Systematic boundary testing
- Negative injection testing

**Recommendation for Exercise 7:**
Create a fuzzing scenario (not full fuzzing framework, but structured):
```python
# Exercise-7.md Hands-On Lab: AI Fuzzing
# 1. Baseline query: "What are testing strategies for AI?"
# 2. Typo variant: "Whqt arr testing strategies 4 AI?"
# 3. Tone variant: "TESTING STRATEGIES FOR AI - GIVE ME ALL!!!!"
# 4. Negative variant: "I believe AI testing is impossible. Prove me wrong."
# 5. Compare traces and token costs
```

---

### 8. Tiered Testing Strategy ✅ CONCEPTUALLY SOUND

**Your concepts:**
- Tier 1 (Mocking): 90% of tests, $0 cost
- Tier 2 (Mini models): 10% regression, 90% cost savings
- Tier 3 (Full models): Final release validation only
- Telemetry cost auditing

**Current alignment:**
- ✅ Tier 1: Existing regression suite uses mocks (section9_agentic_test_suite.py)
- ✅ Tier 2: Using llama3.2:1b locally (no API cost, mini model equivalent)
- ✅ Tier 3: Optional—students could configure OpenAI/Claude if desired
- ✅ Cost auditing: Phoenix captures tokens for all tiers

**What students can demonstrate:**
- Run traces with Ollama (free local)
- Track tokens in Phoenix
- Estimate costs if they switched to GPT-4o mini or Claude
- Compare token efficiency across exercise runs

**Recommendation:**
Document the tiered strategy in Exercise 7:
```markdown
## Exercise 7: Tiered Testing & Cost Governance

Tier 1 (Mocking) - 0% cost: Run regression suite with static data
→ Example: section9_agentic_test_suite.py (mock mode)

Tier 2 (Mini Model) - ~99% savings: Run with llama3.2:1b
→ Example: your current setup with Ollama

Tier 3 (Production Model) - Full cost: Optional GPT-4o ($0.30/1M input)
→ Not required for classroom, but show how to estimate
```

---

## Phoenix Observability Readiness

### What We Have ✅

**Span Instrumentation:**
- ✅ LLM spans: prompts, completions, temperature, tokens
- ✅ Tool spans: names, inputs, outputs, execution status
- ✅ Retrieval spans: documents, similarity scores, latency
- ✅ Error spans: exceptions recorded with details
- ✅ Session tracking: session_id, exercise_number, app.mode

**Attributes Captured:**
| Category | Attributes | Status |
|---|---|---|
| LLM I/O | prompts, completions, model_name, temperature | ✅ |
| Tokens | prompt_tokens, completion_tokens, total_tokens | ✅ |
| Errors | error, exception details | ✅ |
| Latency | span duration (auto from Phoenix) | ✅ |
| Context | session.id, exercise_number, app.mode | ✅ |
| Quality | retrieval scores, tool execution result | ✅ |
| **Cost estimation** | *estimated_usd* | ❌ Missing |
| **Loop detection** | *iteration_number, loop_depth* | ❌ Missing |
| **Graceful degradation** | *fallback_triggered, circuit_breaker.state* | ❌ Missing |
| **HTTP status codes** | *http.status_code* | ❌ Missing |

### What We Should Add (Optional Enhancements)

**For Exercise 7 to fully support Module 7 concepts:**

1. **Cost estimation** (30 min):
   ```python
   # In agentic_testops.py on_llm_end():
   estimated_cost = (prompt_tokens / 1e6 * 0.05) + (completion / 1e6 * 0.15)
   span.set_attribute("llm.cost.estimated_usd", round(estimated_cost, 6))
   ```

2. **Loop detection** (30 min):
   ```python
   # In TestOpsAgent:
   span.set_attribute("agent.iteration_number", self.iteration_count)
   span.set_attribute("agent.max_iterations_reached", self.iteration_count >= max_iter)
   ```

3. **HTTP error codes** (20 min):
   ```python
   # In rag_pipeline.py _generate_response():
   try:
       response = requests.post(...)
   except requests.HTTPError as e:
       span.set_attribute("http.status_code", e.response.status_code)
   ```

4. **Fallback tracking** (20 min):
   ```python
   # On error in rag_pipeline.py:
   span.set_attribute("app.fallback.triggered", True)
   span.set_attribute("app.fallback.reason", error_type)
   ```

**Effort to add all**: ~2 hours
**Impact**: Students can diagnose all 8 NFR categories + automated assertions

---

## Exercise 7 Exists & Is Well-Structured ✅

**Current state:**
- Exercise 1-5: Complete (Ask, Agent, Crew modes)
- Exercise 6: Complete (Multi-agent handoff + trajectory analysis, 12 traces from generate_classroom_traces.py)
- **Exercise 7: Complete** ✅ (Reliability and Overhead: Ask vs Agent vs Crew comparison)

**Exercise 7 Structure (90-120 minutes):**

**Part 1 (Setup, 10 min):**
- Open live Phoenix Traces tab
- Reuse 12 traces from Exercise 6 Part 1 (classroom_traces_results.json)
- Each trace already has: latency, tokens, error status, tool calls captured

**Part 2 (Role-Based Analysis, 60-90 min):**
- 5 roles assigned to 5 students/teams:
  1. **Latency Overhead**: Compare Ask vs Agent latency on same prompt
  2. **Long-Input Stability**: Test robustness with long but valid input
  3. **Malformed Input Handling**: Test graceful degradation with garbage input
  4. **Loop Containment**: Verify single-agent loops are bounded
  5. **Handoff Resilience**: Verify multi-agent handoffs survive corruption

**Part 3 (Scorecard & Debrief, 10-20 min):**
- Fill NFR scorecard with evidence from Phoenix
- Team identifies weakest NFR area
- Propose one fix with smallest blast radius

**Key advantage: Zero new prompts needed!**
- The 12 Exercise 6 traces already exercise Ask/Agent/Crew modes
- Different input types (same, variation, different) test robustness
- Students analyze existing traces for latency, tokens, errors
- Saves ~12 × 30sec = 6 minutes of inference time

---

## Recommendations

### Immediate (Ready for this term) ✅
1. Module 7 concepts are sound and well-aligned with Phoenix
2. **Exercise 7 exists and is ready to teach**
3. **Key optimization: Explicitly link Exercise 7 to Exercise 6 traces**
   - Add intro section to Exercise-7.md: "Use the 12 traces from Exercise 6 Part 1 for this analysis"
   - Point to `classroom_traces_results.json` and Phoenix Traces tab filter
   - Saves students 6+ minutes of inference time
4. Students can observe latency, tokens, and errors using existing traces

### Short-term (Before next term, <2 hrs)
1. Update Exercise-7.md preamble to explicitly reuse Exercise 6 traces
2. Add optional span attributes for better diagnostics (cost estimation, loop detection)
3. Create example scorecard row showing how to read Phoenix traces for NFR metrics

### Medium-term (End of course or next iteration)
1. Add AI fuzzing scenario as optional Exercise 7 extension
2. Build cost estimation dashboard aggregation in Phoenix (if using paid APIs)
3. Add queue management simulation (concurrent user test harness)

---

## File Impact Summary

**No changes required now.** When ready, enhancements would target:
- [app/agentic_testops.py](app/agentic_testops.py): Add cost, loop detection, fallback attributes
- [app/rag_pipeline.py](app/rag_pipeline.py): Add HTTP status code, fallback trigger attributes
- `docs/exercises/Exercise-7.md`: NEW file (2-part hands-on lab)

---

## Conclusion

✅ **Your Module 7 is pedagogically sound, Phoenix-ready, and Exercise 7 is ready to teach.**

All major NFR concepts are **observable and testable** within the current setup. Exercise 7 smartly reuses the 12 traces from Exercise 6 for analysis rather than running new prompts, which is efficient and reduces classroom time.

**Immediate next action:** Add a brief preamble to Exercise-7.md:
```markdown
## Trace Reuse Optimization
You do not need to run new prompts for this exercise. The 12 traces generated 
in Exercise 6 Part 1 (stored in `classroom_traces_results.json`) already capture 
Ask, Agent, and Crew modes with varying input types. This exercise analyzes those 
same traces for NFR metrics instead.

To proceed:
1. Ensure Exercise 6 Part 1 has completed: `python generate_classroom_traces.py`
2. Open Phoenix: http://localhost:6006 → Traces tab
3. Filter for the 12 traces by scenario tag (same_prompt, variation, different_prompt)
4. Proceed to "Student tasks" below
```

This makes the efficiency gain explicit and saves students time.
