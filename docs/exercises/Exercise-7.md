# Exercise 7: Validate NFR Evidence in MLflow

## Prerequisites
1. Exercise 6 completed
2. The application has handled at least one Ask, single-agent, and crew request.

## Goal

Determine whether the system provides enough evidence to assess latency,
token/cost overhead, reliability, and orchestration overhead. This exercise is
about validating the measurement system as well as measuring the application.

Do not fill a missing metric with an estimate. Record `not emitted` when the
trace does not contain the field, then explain why that limits the conclusion.

## Metrics evidence map

| Metric | Ask/RAG source | Agent/crew source | Evidence location |
|---|---|---|---|
| End-to-end latency | `rag.query` duration and API `total_time` | root agent trace duration and API `response_time` | MLflow trace duration and response JSON |
| Retrieval latency | API `retrieval_time` | retrieval/tool span duration | response JSON or child span |
| Generation latency | API `generation_time` | LLM span duration | response JSON or LLM span |
| Prompt tokens | Ollama `prompt_eval_count` | LangChain/MLflow LLM usage | `generation_metrics.prompt_tokens` or LLM span |
| Completion tokens | Ollama `eval_count` | LangChain/MLflow LLM usage | `generation_metrics.completion_tokens` or LLM span |
| Total tokens | sum of prompt and completion tokens | MLflow LLM usage | `generation_metrics.total_tokens` or LLM span |
| Provider durations | Ollama duration fields | provider/autolog fields when emitted | `generation_metrics` or `rag.provider.*` span attributes |
| Tool calls | not applicable | trajectory metadata and tool spans | UI Agent Execution block and trace |
| Handoffs | not applicable | handoff metadata and spans | UI handoff block and trace |
| Error/timeout | API status and error payload | error span/API status | trace status and response JSON |

## Activity 1: Compare Ask and agent overhead

Use the same question in Ask mode and single-agent mode. Capture one trace for
 each mode, then record:

1. end-to-end latency
2. retrieval and generation latency where available
3. prompt, completion, and total tokens
4. tool-call count
5. retry or redundant-call count
6. error or timeout status

Calculate overhead only when both values are present:

```text
latency overhead = (agent latency - Ask latency) / Ask latency * 100
 token overhead = (agent tokens - Ask tokens) / Ask tokens * 100
```

## Activity 2: Validate repeatability

Run the same Ask question three times or use the pre-generated `same_prompt`
traces. Compare:

- median and maximum latency
- token-count variation
- retrieved source consistency
- response structure
- trace structure

Then compare reworded `variation` traces and explain whether the variation is a
quality change, an expected wording change, or a retrieval change.

## Activity 3: Error resilience

Use one normal prompt and one malformed or unusual prompt. Record whether the
system:

- returns a bounded response
- returns a documented error
- times out
- creates a trace with an error status
- attempts unnecessary tool retries

Run the malformed case live only once. Use pre-generated traces for comparison
when possible so the class does not spend its time repeating slow inference.

## Results table

| Case | Mode | Latency | Prompt tokens | Completion tokens | Total tokens | Tools | Handoffs | Status | Evidence |
|---|---|---:|---:|---:|---:|---:|---:|---|---|
| Same prompt | Ask |  |  |  |  | N/A | N/A |  |  |
| Same prompt | Single-agent |  |  |  |  |  |  |  |  |
| Same prompt | Crew |  |  |  |  |  |  |  |  |
| Reworded prompt | Ask |  |  |  |  | N/A | N/A |  |  |
| Reworded prompt | Agent |  |  |  |  |  |  |  |  |
| Malformed prompt | Agent |  |  |  |  |  |  |  |  |

## Optional automation

Run:

```bash
python section7_nfr_quickrun.py
```

Use the generated artifact as a comparison aid, then verify at least one result
against its MLflow trace. The artifact is not a substitute for checking whether
the claimed metric was actually emitted.

## Team debrief

1. Which NFR metric was reliably available in every mode?
2. Which metric was missing or mode-dependent?
3. Did agent or crew overhead come from tokens, tools, handoffs, or retries?
4. Which metric should become a release threshold in Exercise 9?
