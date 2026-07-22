# Phoenix Observability Data Guide for AI Testing

## Overview

Your application now emits rich telemetry data to Phoenix that supports comprehensive AI system testing. This guide explains what data is available and how to use it for the testing scenarios covered in the 2-day course.

---

## Available Testing Data by Category

### 1. **LLM Input/Output Testing**

**What's Captured:**
- **Prompts**: Full prompt text sent to Ollama (first 1000 chars, truncated for large prompts)
- **Completions**: Full model response text (first 1000 chars)
- **Model Parameters**: Temperature, max tokens, model name
- **Token Usage**: Prompt tokens, completion tokens, total tokens (when available from Ollama)
- **Finish Reason**: "stop", "length", or error state

**Where to Find in Phoenix:**
```
Span Type: LLM
Span Names: agent.llm, rag.generate
Attributes:
  - llm.prompts.0 → original prompt
  - llm.messages.0.content → chat message (if using messages)
  - llm.completions.0.content → model output
  - llm.completions.0.finish_reason → completion status
  - llm.usage.prompt_tokens → input tokens
  - llm.usage.completion_tokens → output tokens
  - llm.usage.total_tokens → total
  - llm.invocation_parameters.temperature → temperature used
  - llm.model_name → model identifier
```

**Test Scenarios:**
- Verify prompts are well-formed and contextual
- Check response quality and coherence
- Validate temperature effects on output variability
- Audit token usage to catch runaway generation
- Ensure consistent model behavior across runs

---

### 2. **Retrieval Augmented Generation (RAG) Testing**

**What's Captured:**
- **Query**: Original user question
- **Retrieved Documents**: Top 3 documents with content excerpts
- **Similarity Scores**: Vector similarity for each retrieved document (0-1 scale)
- **Retrieval Metrics**: Number of docs returned, top-1 similarity, average similarity
- **Context Quality**: Whether retrieved docs are relevant to the query

**Where to Find in Phoenix:**
```
Span Type: RETRIEVER
Span Names: rag.retrieve
Attributes:
  - rag.query → user's question
  - rag.n_results → number of docs requested
  - retrieval.documents.0.content → first retrieved doc
  - retrieval.documents.0.score → similarity score (0-1)
  - retrieval.documents.1.content → second doc
  - retrieval.documents.1.score → score
  - retrieval.documents.2.content → third doc
  - retrieval.documents.2.score → score
  - quality.retrieval.docs_returned → how many came back
  - quality.retrieval.top1_similarity → best match score
  - quality.retrieval.avg_similarity → average match score
```

**Test Scenarios:**
- **Hallucination Detection**: Compare retrieved docs to the response. Did the model reference retrieved content or make things up?
- **Relevance Testing**: Inspect similarity scores. Are high-relevance docs being retrieved?
- **Cold-Start Testing**: Does the first query retrieve good docs? (Compare first run vs second)
- **Query Ambiguity**: For vague queries, do you get diverse or low-quality results?
- **Grounding Validation**: Verify the response only used provided context

---

### 3. **Agent Trajectory & Decision Making**

**What's Captured:**
- **Chain Execution**: Named steps in agent reasoning (e.g., "agent.chain")
- **Agent Mode**: Single-agent (ReAct) vs multi-agent (CrewAI) routing
- **Tool Selection**: Which tools the agent chose to invoke
- **Tool Inputs**: Full input parameters passed to each tool
- **Tool Outputs**: Results returned by each tool
- **Agent Metadata**: Session ID, exercise number, agent mode

**Where to Find in Phoenix:**
```
Span Type: CHAIN
Span Names: agent.chain
Attributes:
  - chain.name → chain identifier
  - agent.mode → "react" or "crew"
  - session.id → test session identifier
  - exercise_number → which exercise (if applicable)
  - Spans contain tree structure showing call hierarchy

Span Type: TOOL
Span Names: agent.tool
Attributes:
  - tool.name → tool identifier
  - tool.input → full input to the tool
  - tool.output → result from the tool
  - tool.execution_result → "success" or error indicator
  - Tool spans nest under agent.chain spans
```

**Test Scenarios:**
- **Agent Behavior**: Trace reasoning steps to understand decision-making
- **Tool Misuse**: Verify tools are called with correct inputs and handle outputs correctly
- **Failure Modes**: When an agent fails, see which tool call broke and why
- **Convergence**: Do agents reach conclusions or get stuck in loops?
- **Consistency**: Run same prompt twice; do agents make same decisions?

---

### 4. **Performance & Latency Breakdown**

**What's Captured:**
- **Span Duration**: Precise timing for each operation
- **Retrieval Time**: How long vector search took
- **Generation Time**: How long LLM inference took
- **Total Time**: End-to-end response time
- **Cold vs Warm**: First request vs subsequent requests
- **Quality Signals**: Response length, completeness metrics

**Where to Find in Phoenix:**
```
Span Timing (View → Latency or Timeline):
  - Span duration shown in milliseconds
  - Nested spans show time breakdown
  
Quality Attributes:
  - quality.response.total_time_ms → total ms
  - quality.response.retrieval_time_ms → retrieval ms
  - quality.response.length_chars → response length
  - quality.response.source_count → how many sources
  
RAG Attributes:
  - retrieval_time → seconds
  - generation_time → seconds (from rag.query span)
  - total_time → seconds (from rag.query span)
```

**Test Scenarios:**
- **Cold Start Testing**: First inference is typically 15-30s on 2-core; subsequent requests are faster
- **SLA Compliance**: Are responses within acceptable latency budgets?
- **Resource Saturation**: Do you see degradation as concurrent requests increase?
- **Token-to-Latency Correlation**: Longer responses = longer generation time
- **Model Warm-up**: Verify pre-warming strategy is effective

---

### 5. **Error & Failure Tracking**

**What's Captured:**
- **Exception Details**: Full error message and stack trace
- **Error Span Markers**: Spans where errors occurred marked with "error: true"
- **Failure Context**: Which operation failed (LLM, retrieval, tool, agent)
- **Session Context**: Session ID and exercise context tied to the error

**Where to Find in Phoenix:**
```
Span Type: Any (marked with error)
Attributes:
  - error: true → indicates span had an error
  - Exception tab → shows full error traceback
  - openinference.span.kind → identifies which subsystem failed (LLM, RETRIEVER, TOOL, etc.)
```

**Test Scenarios:**
- **Failure Modes**: Understand which operations fail most often
- **Error Recovery**: Do agents gracefully handle tool failures?
- **Timeouts**: Identify requests that exceed timeout limits
- **Network Issues**: Catch connection failures to Ollama or vector DB
- **Data Issues**: Errors on malformed input validation

---

### 6. **Quality Metrics for Grading**

**What's Captured:**
- **Retrieval Quality**: Top-1 similarity, average similarity, doc count
- **Response Completeness**: Response length, source count, has_sources flag
- **Session Metadata**: Consistent session IDs for tracking student progress
- **Exercise Context**: Which exercise is being tested

**Where to Find in Phoenix:**
```
From rag.query span:
  - quality.response.total_time_ms
  - quality.response.retrieval_time_ms
  - quality.response.length_chars
  - quality.response.has_sources
  - quality.response.source_count

From rag.retrieve span:
  - quality.retrieval.docs_returned
  - quality.retrieval.top1_similarity
  - quality.retrieval.avg_similarity
```

**Test Scenarios:**
- **Automated Grading**: Use these metrics to score student implementations
- **Baseline Comparison**: Compare new model runs against known-good baselines
- **Regression Detection**: Flag when metrics drop below thresholds
- **Consistency Validation**: Ensure repeated runs produce similar scores

---

## How to Query This Data in Phoenix

### Via Phoenix UI - Finding Token Usage:

**Step 1: Open Traces Tab**
1. Go to http://localhost:6006
2. Click **Traces** tab (main table view)

**Step 2: Find Your Request**
- Look for span name: `rag.generate` (Ask mode) or `agent.llm` (Agent/Crew mode)
- Or search by attributes if available

**Step 3: Expand the Span**
- Click on the trace row to view detailed trace
- In the **left panel**, you'll see nested spans (CHAIN > LLM > TOOL structure)
- Click on the **LLM span** (blue or red box)

**Step 4: View Attributes Panel**
- **Right panel** shows all span attributes
- Scroll down in attributes to find:
  - `llm.usage.prompt_tokens` — Input token count
  - `llm.usage.completion_tokens` — Output token count
  - `llm.usage.total_tokens` — Total token count
  - `llm.prompts.0` — The actual prompt sent
  - `llm.completions.0.content` — The model's response
  - `llm.completions.0.finish_reason` — Why it stopped (stop, length, error)

**Step 5: For RAG Retrieval**
- Click on the **RETRIEVER span** (purple)
- Attributes panel shows:
  - `retrieval.documents.0.content` — First retrieved document
  - `retrieval.documents.0.score` — Similarity (0-1 scale)
  - `retrieval.documents.1.content`, `.1.score` — Second doc
  - `retrieval.documents.2.content`, `.2.score` — Third doc
  - `quality.retrieval.top1_similarity` — Best match score
  - `rag.query` — The original user question

## Phoenix Tabs Explained

### **Traces Tab** (Your Primary Focus)
- **Purpose**: View raw execution data from your LLM app
- **Contains**: Prompts, responses, tokens, latency, tool calls, errors
- **How to use**: Debug "what happened" in each request
- **Example**: "Why did the retrieval only find 2 docs instead of 5?"

### **Evaluators Tab** (Automated Grading)
- **Purpose**: Run automated scoring functions on your traces
- **Contains**: Quality scores (hallucination, relevance, groundedness)
- **How to use**: Measure aggregate quality across many traces
- **Example**: "Grade 100 traces for hallucination; get average score of 0.87"
- **See**: [PHOENIX_EVALUATIONS_GUIDE.md](PHOENIX_EVALUATIONS_GUIDE.md) for setup

### **Projects / Config Tab** (Settings)
- **Purpose**: Map span attributes to input/output roles
- **Contains**: Input key mappings, output key mappings, custom fields
- **How to use**: Tell Phoenix how to interpret your span structure
- **Example**: "Treat `llm.prompts.0` as Input, `llm.completions.0.content` as Output"
- **Default**: Phoenix auto-detects OpenInference conventions (your code uses these)

### Via Span Timeline:

1. **Traces → Timeline view**
2. **Hover over spans** to see duration and names
3. **Color coding**:
   - Blue = CHAIN, RED = LLM, GREEN = TOOL, PURPLE = RETRIEVER
4. **Click to expand** nested spans

### Via Attribute Search:

1. **Traces → Filter / Search panel**
2. **Search by attribute name** (e.g., "llm.model_name", "tool.name")
3. **Filter by value** (e.g., "agent.mode: crew" to see only multi-agent runs)

---

## Mapping to 2-Day Course Modules

| Course Topic | Data in Phoenix | Test Activity |
|---|---|---|
| **Model Inputs & Outputs** | `llm.prompts.0`, `llm.completions.0.content` | Inspect what model saw and what it produced |
| **Hallucination Detection** | `rag.query`, `retrieval.documents.*`, `llm.completions.0.content` | Compare response to retrieved docs |
| **Retrieval Quality** | `quality.retrieval.top1_similarity`, `retrieval.documents.*.score` | Validate vector search effectiveness |
| **Agent Reasoning** | `agent.chain`, `agent.tool` span hierarchy | Trace decision trees |
| **Tool Usage** | `tool.name`, `tool.input`, `tool.output` | Verify correct tool invocation |
| **Performance SLAs** | `total_time`, `generation_time`, `retrieval_time` | Check latency compliance |
| **Error Handling** | `error: true` span attribute + exception trace | Understand failure modes |
| **Token Economy** | `llm.usage.prompt_tokens`, `llm.usage.completion_tokens` | Track cost and efficiency |
| **Consistency Testing** | Session traces side-by-side | Compare determinism across runs |

---

## Troubleshooting: "I Still Don't See the Data"

### Problem: Only seeing span names, no attributes
**Solution:**
- Ensure Phoenix is running: `pgrep -f "phoenix.*serve"`
- Restart Flask app: `python run.py`
- Wait 30 seconds for first inference to warm up (cold-start timeout)
- Refresh Phoenix UI and create a new trace

### Problem: Spans exist but token counts are missing
**Solution (Ask/RAG mode):**
- Check `/tmp/ollama.log` for errors
- Ensure Ollama is responding: `curl http://127.0.0.1:11434/api/tags`
- Token data comes from Ollama's response payload — if missing, Ollama may not be returning them
- Look in terminal output for debug message: "Ollama response missing token counts. Payload keys: ..."

**Solution (Agent/Crew mode):**
- ChatOllama from LangChain might not be including `usage_metadata`
- Check `AGENT_MODEL` env var matches a model that returns token counts
- Look in terminal: "Response missing usage_metadata. Response attributes: ..."

### Problem: Spans exist but token counts show 0
**Solution:**
- This can happen on first/cold-start requests when model is loading
- Try again on second request (warm model)
- Token counting is accurate once model inference completes

### Problem: I see prompts but not completions
**Solution:**
- Completions are only set when the LLM response completes without error
- If you see error span markers, check exception trace
- Long-running requests may time out before completion is captured

### Problem: Retrieved documents are empty
**Solution:**
- Ensure documents are loaded: `curl http://localhost:5000/api/health`
- Check document count: Look at `documents_loaded` in response
- If count is 0, run the setup script to load documents

---

## Next Steps

1. **Create a trace** using the Flask app at http://localhost:5000
2. **Open Phoenix** → Traces tab
3. **Click on your trace** and expand nested spans
4. **Right panel** shows all attributes
5. **Use this data** to test hallucination, retrieval quality, agent logic, etc.

For detailed span structure and all available attributes, see the OpenInference specification:  
https://github.com/Arize-ai/open-inference-spec
