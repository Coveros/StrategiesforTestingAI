# Tracing Validation: QA Manager Workshop Scenarios

## Executive Summary

✅ **All three scenarios are valid for trajectory analysis**, but require complementary span attributes to make diagnosis clear and repeatable. Current instrumentation captures the **building blocks** (LLM outputs, tool calls, error status), but lacks **explicit governance signals** (loop counter, schema mismatch detection, efficiency ratio).

---

## Scenario-by-Scenario Validation

### Scenario 1: Infinite Politeness Loop ✅ VALID

**Observable through current tracing:**
- ✅ **Span sequence**: Agent callback chain shows Spans 1→2→3→4→5→42 (visible in Phoenix span graph)
- ✅ **Repeated patterns**: `tool.output` contains agent-to-agent text ("I need...", "Thank you...") repeated 38+ times
- ✅ **Latency explosion**: Span duration accumulation visible in timeline
- ✅ **Budget overrun**: Token count (llm.usage.total_tokens) increases per iteration
- ✅ **Error/timeout status**: Final span shows execution timeout or error status

**Missing for explicit detection:**
- ❌ **Loop counter attribute**: No `agent.loop_count` or `agent.repeated_handoff_count` span attribute
- ❌ **Conversation depth metric**: No `agent.conversation_depth` to distinguish loops from legitimate multi-turn
- ❌ **Circuit breaker signal**: No span attribute marking "exceeded max iterations"

**What students see in Phoenix:**
- Span graph with 38+ identical-looking nodes (clear visual pattern)
- Tool outputs showing repetitive "thank you" messages
- Token count steadily climbing
- Total latency >> SLA target

**Student analysis task:**
"Count the handoff cycles. At what span number should a circuit breaker have fired?"

**Recommended span attributes to add:**
```
agent.loop_depth: int (current call depth in cycle)
agent.repeated_span_count: int (how many identical spans in a row)
agent.max_iterations_reached: bool
```

---

### Scenario 2: Silent Context Loss ✅ VALID

**Observable through current tracing:**
- ✅ **Schema mismatch evidence**: Tool output from Span 2 shows plain text, but Span 3 input expects `{account_id: str, date_range: str}`
- ✅ **Parameter degradation**: Downstream span attributes show `account_id=null, date_range=null` 
- ✅ **Downstream failure**: Span 3 output shows "No logs found for account null" (null values visible in completions)
- ✅ **Error causality chain**: Trace shows exact moment input contract violated

**Missing for explicit detection:**
- ❌ **Schema validation span**: No dedicated span for "handoff_validation" to show expected vs actual schema
- ❌ **Parameter extraction results**: No span showing what values were extracted/defaulted
- ❌ **Contract mismatch flag**: No `handoff.schema_validation.result` = "FAILED"

**What students see in Phoenix:**
- Two consecutive tool spans showing output → input transition
- Output span: text summary (unstructured)
- Input span: error or null parameter logging
- Downstream error message with null values

**Student analysis task:**
"Find the handoff span. What format did the first agent send? What format did the second agent expect? Where was the converter?"

**Recommended span attributes to add:**
```
handoff.output_schema: str (e.g., "text")
handoff.input_schema_expected: str (e.g., "json")
handoff.schema_validation.passed: bool
handoff.parameters_lost: list[str]  (["account_id", "date_range"])
```

---

### Scenario 3: Span Thrashing & Inefficient Routing ✅ VALID

**Observable through current tracing:**
- ✅ **Routing sequence**: Span order shows Agent → Agent → Agent wrong → error → retry
- ✅ **Error spans**: Spans 3-4 show `tool.execution_result = error` or output contains rejection message
- ✅ **Redundant steps**: Spans 1→2→3→4→5 vs optimal 1→2→3 visible in count
- ✅ **Latency impact**: Sum of all 8 span durations = 52s vs optimal ~6s
- ✅ **Agent capability mismatch**: Tool error messages like "I do not fetch raw policy files" indicate wrong agent selected

**Missing for explicit detection:**
- ❌ **Efficiency ratio span attribute**: No `agent.trajectory.efficiency_ratio` = 0.375
- ❌ **Routing decision audit trail**: No span showing "Orchestrator evaluated: Report Writer, Analytics, Data Gathering (in that order)"
- ❌ **Capability matching score**: No `agent.routing_confidence` or `agent.capability_match_score`

**What students see in Phoenix:**
- 8-span trajectory in Phoenix graph (vs expected 3)
- Span 2: ReportWriter output "I need pricing data"
- Span 3: Analytics error "I do not fetch"
- Span 5: DataGathering success with pricing
- Span 7: Report Writer final success
- Total duration: 52s (visible in timeline)

**Student analysis task:**
"Calculate efficiency ratio. At which span should routing have been different? What capability signal was missing?"

**Recommended span attributes to add:**
```
agent.routing_decision.agent_name: str
agent.routing_decision.capability_required: str
agent.routing_confidence: float (0-1)
agent.trajectory.steps_actual: int
agent.trajectory.steps_optimal: int
agent.trajectory.efficiency_ratio: float (steps_optimal / steps_actual)
```

---

## Mapping to Current Codebase

### What We Currently Capture (✅ Good)

**File: `app/agentic_testops.py`**
```python
# Captured in tool spans:
span.set_attribute("tool.name", str(tool_name))
span.set_attribute("tool.input", str(input_str))
span.set_attribute("tool.output", output_str)
span.set_attribute("tool.execution_result", "success")  # or error

# Captured in LLM spans:
span.set_attribute("llm.model_name", str(model_name))
span.set_attribute("llm.completions.0.content", text_out)
span.set_attribute("llm.usage.prompt_tokens", int(prompt_tokens))
span.set_attribute("llm.usage.completion_tokens", int(completion_tokens))
```

✅ This allows students to see:
- Tool names and outputs (visible routing chain)
- Error messages from tools (capability mismatch evidence)
- LLM responses and token costs (budget overrun)
- Span hierarchy (parent/child call sequence)

### What We Should Add (❌ Enhancement Needed)

For explicit diagnosis of the three scenarios, we need:

**1. Loop Detection Attributes:**
```python
span.set_attribute("agent.iteration_number", iteration_count)
span.set_attribute("agent.max_iterations", max_iter)
span.set_attribute("agent.loop_detection.is_repeated_state", bool)
```

**2. Handoff Schema Attributes:**
```python
span.set_attribute("handoff.from_agent", agent_name)
span.set_attribute("handoff.to_agent", target_agent_name)
span.set_attribute("handoff.output_format", "text" | "json" | "structured")
span.set_attribute("handoff.expected_input_format", schema_str)
```

**3. Routing Decision Attributes:**
```python
span.set_attribute("routing.decision_made_by", orchestrator_name)
span.set_attribute("routing.selected_agent", selected_agent)
span.set_attribute("routing.reason", reason_text)
span.set_attribute("routing.success", bool)
```

---

## How This Aligns with Exercise 6

### Current Exercise 6 Coverage

**Part 1 (Classroom Demo):**
- Addresses **Scenario 1 signals** (different trajectories, tool variations)
- Addresses **Scenario 3 signals** (step count, efficiency concept)
- **Gap**: Doesn't explicitly show loops or schema mismatches

**Part 2 (Individual Handoff Corruption):**
- Focuses on **Scenario 2** (corrupted handoff data)
- Asks students to compare baseline vs corrupted traces
- Asks for "efficiency score" (Scenario 3 concept)
- **Gap**: Single agent pair (Triage → RAG Specialist) doesn't show multi-agent routing (Scenario 3)

### Recommendation for Curriculum Alignment

| Scenario | Exercise 6 Part 1 | Exercise 6 Part 2 | Fully Covered? |
|---|---|---|---|
| **Scenario 1: Infinite Loop** | ✅ Step count varies | ❌ Not explicit | ⚠️ Partial |
| **Scenario 2: Context Loss** | ❌ No schema testing | ✅ Handoff corruption | ✅ Yes |
| **Scenario 3: Inefficient Routing** | ✅ Efficiency ratio concept | ⚠️ Two-agent path only | ⚠️ Partial |

**To fully cover Scenario 1 & 3:**
- Add a 4-agent orchestration exercise (Orchestrator → Data Agent → Analytics Agent → Report Writer)
- Introduce "max iterations" configuration and loop detection
- Have students diagnose both "loop deadlock" and "inefficient routing"

---

## Validation Checklist: Are Your Scenarios Observable?

| Aspect | Observable? | Evidence in Trace | Notes |
|---|---|---|---|
| **Scenario 1: Loop repetition** | ✅ Yes | Repeated span sequence, token accumulation, timeout error | Add: loop_count attribute |
| **Scenario 1: Budget overrun** | ✅ Yes | `llm.usage.total_tokens` increases per iteration | Clear via token span attributes |
| **Scenario 2: Null parameters** | ✅ Yes | Downstream span shows `account_id=null` in output | Add: schema_validation span |
| **Scenario 2: Schema mismatch** | ✅ Yes | Tool output format (text) vs expected input format (JSON) | Add: handoff.output_schema attribute |
| **Scenario 3: Routing errors** | ✅ Yes | Error message "I do not fetch policy files" in span output | Clear via tool.output |
| **Scenario 3: Inefficiency** | ✅ Yes | 8 spans vs 3 optimal, 52s vs 6s latency | Add: efficiency_ratio attribute |
| **Scenario 3: Wrong agent selection** | ✅ Yes | Orchestrator routed to Analytics instead of DataGathering | Add: routing.selected_agent attribute |

---

## Conclusion

**✅ All three scenarios are pedagogically sound and traceable through multi-agent span analysis.**

The scenarios test:
1. **Scenario 1**: Control flow governance (loop/iteration limits)
2. **Scenario 2**: Data contract enforcement (handoff schema validation)
3. **Scenario 3**: Capability routing logic (agent selection optimization)

**To make diagnosis easier for students, recommend adding:**
- `agent.loop_depth`, `agent.iteration_number`, `agent.max_iterations_reached`
- `handoff.output_schema`, `handoff.expected_input_format`, `handoff.schema_validation.result`
- `routing.selected_agent`, `routing.reason`, `agent.trajectory.efficiency_ratio`

These are **enhancement** attributes—not required for students to diagnose, but they enable **automated test assertions** (which is your QA Manager workshop goal).

---

## Next Steps

1. **Short-term**: Exercise 6 Part 2 is ready to teach (Scenario 2 covered)
2. **Medium-term**: Add loop detection attributes to `agentic_testops.py` (enables Scenario 1 teaching)
3. **Long-term**: Create Module 6 Exercise (4-agent orchestration) for Scenarios 1 + 3 together
