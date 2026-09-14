# Module 7: Non-Functional Requirements (NFR) Testing Prompts

**Goal:** Run these prompts across **three modes (Ask, Agent single-agent, Crew multi-agent)** and measure performance overhead. Compare token counts, latency, error handling, and efficiency. Use MLflow to quantify the cost of agent routing and handoffs.

**Module 7 Focus:** Mode comparison (overhead analysis), error resilience, consistency verification

---

## How to Run

1. **Start the system:**
   ```bash
   python run.py              # Flask app
   mlflow server --backend-store-uri sqlite:///mlflow_data/mlflow.db --host 0.0.0.0 --port 5001  # MLflow (separate terminal)
   ```

2. **Run a prompt across all three modes:**
   - Open http://localhost:5000 in your browser
   - Run same prompt in **Ask Mode** (RAG only)
   - Then switch to **Agent Mode** (crew OFF)
   - Then switch to **Agent Mode** (crew ON, multi-agent)
   - Record metrics for each
   - Note the time or use browser dev tools

3. **Analyze in MLflow:**
   - Open http://localhost:5001 → Traces tab
   - Compare three traces side-by-side
   - Look at `duration`, `retrieval.documents_returned`, span count, tool calls

---

## Prompt List & What to Measure

### Category 1: Latency Overhead Across Modes

**Prompt 1:** `What are the primary challenges in evaluating large language models?`
- **Measure (Ask Mode):** Total trace duration, token count (from response metadata)
- **Measure (Agent Mode):** Same, but single-agent ReAct with callbacks
- **Measure (Crew Mode):** Same, but with Triage Agent routing to RAG Specialist
- **In MLflow:** Compare root span duration across three traces:
  - Ask: Direct retrieve → generate
  - Agent: Query → decide → retrieve → generate
  - Crew: Query → Triage decision → Specialist routing → retrieve → generate
- **Why:** Quantify routing and handoff overhead
- **NFR:** How much slower is Agent vs Ask? Crew vs Agent?

**Prompt 2:** `Explain the difference between unit and integration tests in the context of system safety`
- **Measure:** Compare latency across modes
- **In MLflow:** Look at:
  - Span tree depth (shallow = fast, deep = slow due to handoffs)
  - Retrieve span duration (same query, same docs, should be similar)
  - Agent decision span duration (Triage or routing logic overhead)
  - Generate span duration (varies with token count)
- **Why:** Tests whether complexity affects mode overhead differently
- **NFR:** Does query length increase overhead differently across modes?

**Prompt 3:** `List the key metrics for assessing LLM reliability in production`
- **Measure:** Token count and latency
- **In MLflow:** Quantify:
  - Prompt tokens (should be same across modes, depends on system prompt bloat in Agent/Crew)
  - Completion tokens (should be similar, response quality similar?)
  - Total tokens = prompt + completion
  - Calculate overhead % = (Agent tokens - Ask tokens) / Ask tokens
- **Why:** Tests if agent mode injected extra tokens (system prompts, tool definitions, etc.)
- **NFR:** What is the true token overhead of routing?

---

### Category 2: Error Resilience & Graceful Degradation

**Prompt 4:** `How should I handle test failures in distributed LLM systems? @#$%^&* error codes`
- **Measure (Ask):** Does RAG handle mixed query/noise?
- **Measure (Agent):** Does routing logic handle malformed input?
- **Measure (Crew):** Does Triage agent detect noise before routing?
- **In MLflow:** Look for:
  - Error spans (red indicators)
  - `error.type` classification: malformed_input, parsing_error, etc.
  - Recovery: Did system fallback gracefully or crash?
  - Response quality despite error
- **Why:** Tests error handling across modes—is one more robust?
- **NFR:** All modes should fail safely (bounded output, no crashes)

**Prompt 5:** `{ [[ INJECTION_ATTEMPT ]] } What are red-team strategies for AI systems?`
- **Measure:** Does each mode detect and handle injection?
- **In MLflow:** Look for:
  - Security gate spans (if enabled)
  - Did LLM attempt to parse brackets as code?
  - Error handling: Did system isolate the malformed part?
  - Response quality: Is useful content extracted or entire query rejected?
- **Why:** Tests whether routing/validation adds robustness
- **NFR:** Should handle gracefully, not error or execute injection

---

### Category 3: Consistency Across Modes

**Prompt 6:** `Describe the role of test data quality in LLM evaluation` (run 3x in Agent mode only)
- **Measure:** Latency variance across three runs (same prompt, same mode)
- **In MLflow:** Compare three traces:
  - Duration: Run 1 vs Run 2 vs Run 3 (are they identical, or variable?)
  - Tool calls: Does agent make same retrieval calls each time?
  - Retrieval docs: Are returned documents identical?
  - Response text: Identical or temperature variation?
- **Why:** Tests determinism of single-agent routing
- **NFR:** Same prompt should be reproducible (within acceptable variance)

**Prompt 7:** `What strategies should be used to test AI systems for robustness?` (run 2x, different modes: Agent vs Crew)
- **Measure:** Latency comparison for same query in Agent vs Crew
- **In MLflow:** Compare:
  - Agent mode: Query → decide → retrieve → generate latency
  - Crew mode: Query → Triage → Specialist → retrieve → generate latency
  - Difference: Crew overhead = (Crew latency - Agent latency) / Agent latency %
  - Consistency: If run again, do the latencies track together?
- **Why:** Tests whether Crew overhead is stable or variable
- **NFR:** Crew overhead should be consistent and predictable

---

### Category 4: Efficiency & Resource Usage Across Modes

**Prompt 8:** `When is manual testing preferred over automated testing for AI?` (run in Ask mode)
- **Measure:** Span tree depth and tool count (baseline: Ask mode has minimal overhead)
- **In MLflow:** Count:
  - Total spans (should be low: query → retrieve → generate)
  - Tools called (should be 0 or 1: query_knowledge_base only)
  - Nesting depth (shallow)
  - Duration / span count ratio (efficiency metric)
- **Why:** Ask mode is the efficiency baseline
- **NFR:** Ask should be the fastest and least complex

**Prompt 9:** `When is manual testing preferred over automated testing for AI?` (run in Agent mode for comparison)
- **Measure:** Same metrics as Prompt 8, but in Agent mode
- **In MLflow:** Compare to Prompt 8:
  - Span tree depth increased due to routing decision?
  - Tool count: Same (1 retrieval) or different?
  - Duration: Slower due to routing overhead?
  - Efficiency ratio: (Agent duration / Agent span count) vs (Ask duration / Ask span count)
- **Why:** Quantify agent routing overhead
- **NFR:** Agent overhead should be < X% (define acceptable threshold)

**Prompt 10:** `When is manual testing preferred over automated testing for AI?` (run in Crew mode for comparison)
- **Measure:** Full overhead of multi-agent handoff
- **In MLflow:** Compare to Prompts 8 and 9:
  - Span tree depth (Triage + Specialist routing adds layers)
  - Tool calls (same query, same tools, but called through Specialist?)
  - Duration (cumulative: Triage + Specialist + Retrieve + Generate)
  - Handoff overhead: (Crew duration - Ask duration) / Ask duration %
- **Why:** Quantify full multi-agent system cost
- **NFR:** Define acceptable Crew overhead (e.g., < 50% slower for routing value)

---

## Recording Your Observations

| Prompt | Mode | Duration (sec) | Tokens | Span Count | Tools Called | Error? | Notes |
|---|---|---:|---:|---:|---:|---|---|
| LLM Evaluation Challenges | Ask | — | — | — | — | — | Baseline |
| LLM Evaluation Challenges | Agent | — | — | — | — | — | vs Ask |
| LLM Evaluation Challenges | Crew | — | — | — | — | — | vs Agent |
| Unit vs Integration Tests | Ask | — | — | — | — | — | Routing overhead test |
| Unit vs Integration Tests | Agent | — | — | — | — | — | |
| Unit vs Integration Tests | Crew | — | — | — | — | — | |
| Key Metrics for Reliability | Ask | — | — | — | — | — | Token overhead test |
| Key Metrics for Reliability | Agent | — | — | — | — | — | |
| Key Metrics for Reliability | Crew | — | — | — | — | — | |
| Mixed Query + Noise | Ask | — | — | — | — | Pass/Fail | Error resilience |
| Mixed Query + Noise | Agent | — | — | — | — | Pass/Fail | |
| Injection Attempt | Ask | — | — | — | — | Pass/Fail | Malformed handling |
| Injection Attempt | Agent | — | — | — | — | Pass/Fail | |
| Test Data Quality (3x) | Agent | —/—/— | — | — | — | — | Consistency test |
| AI System Robustness (2x) | Agent vs Crew | —/— | — | — | — | — | Overhead comparison |

---

## Key Metrics to Look For in MLflow

**Latency (Duration):**
- Root span duration = total time
- Individual span duration = time at each step
- Retrieve span duration = retrieval overhead
- Generate span duration = generation time

**Efficiency (Span Structure):**
- Total span count = how many steps?
- Nesting depth = how complex?
- Tool calls = retrieval invoked?
- Handoff count = multi-agent overhead?

**Consistency (Compare traces):**
- Same prompt → same span tree?
- Same documents retrieved?
- Duration variance (%) = stable or flaky?

**Error Resilience:**
- Error spans present? (red/error indicators)
- Graceful fallback message?
- Response quality despite error?

---

## Discussion Questions

After running these prompts, focus on **mode comparison and overhead quantification**:

1. **What is the latency overhead of Agent mode vs Ask mode?** Calculate: (Agent - Ask) / Ask × 100%
2. **What is the latency overhead of Crew mode vs Agent mode?** Is it worth the routing capability?
3. **Did token count increase in Agent or Crew modes?** Why? (System prompts? Tool definitions? Extra reasoning?)
4. **Which mode handled errors best?** Did routing or validation add robustness?
5. **Was routing overhead consistent or variable?** (Run same prompt 3x, do overheads repeat?)
6. **If you had a 100ms latency budget, which mode would you use?** Which would you disable?

---

## Key Metrics to Look For in MLflow

**Latency (Duration):**
- Ask mode duration = baseline (minimal overhead)
- Agent mode duration = Ask + routing decision time
- Crew mode duration = Ask + Triage + handoff + Specialist invocation
- Overhead % = (slower mode - Ask) / Ask × 100%

**Token Efficiency:**
- Prompt tokens (ask): Base system prompt only
- Prompt tokens (agent/crew): System + tool definitions + routing reasoning
- Completion tokens: Usually similar, unless agent chooses different response style
- Token overhead % = (Agent tokens - Ask tokens) / Ask tokens × 100%

**Span Structure:**
- Ask: Retrieve → Generate (flat, ~2 spans)
- Agent: Query → Decide → Retrieve → Generate (deeper, ~4-5 spans)
- Crew: Query → Triage → Specialist → Retrieve → Generate (deepest, ~6-7 spans)
- Span count = proxy for orchestration complexity

**Error Resilience:**
- Error spans: Did malformed input trigger error handling?
- Error types: malformed_input, parsing_error, etc.
- Recovery: Was response still meaningful, or completely failed?
