# Module 6 Instructor Cheat Sheet — Phoenix Navigation

Keep this open during class while walking through Phoenix traces.

---

## Scenario 1: Infinite Politeness Loop

**What students should see in Phoenix:**
- Span tree with many identical-looking `agent.chain` nodes (10+ repeats)
- `tool.output` on each span contains repetitive "thank you" / "I need..." text
- Span durations accumulating → total latency well above SLA
- `llm.usage.total_tokens` climbing with each iteration

**Student analysis task:**
> "Count the handoff cycles. At what span number should a circuit breaker have fired?"

**If students can't find it:**
- Click the root `Triage Agent.ex6` span → expand the span tree on the left
- Look for repeated `agent.chain` spans at the same depth
- Click one and look at its `tool.output` — you'll see the repeated phrase

---

## Scenario 2: Silent Context Loss (Handoff Corruption)

**What students should see in Phoenix:**
- Parent span: `output.value` (OUTPUT panel) contains a text summary
- Child span: `input.value` (INPUT panel) contains a *different* or *truncated* query
- Downstream spans show null-like errors or retrieval misses

**Student analysis task:**
> "Find the handoff span. Compare the parent's OUTPUT panel to the child's INPUT panel. What changed?"

**If students can't find it:**
- Run: `simulate handoff corruption for retrieval query about 2024 regression failures`
- In Phoenix, click the `Triage Agent.ex6` span → expand children
- Click `RAG Specialist.ex6` child span
- Compare: parent OUTPUT panel text vs. child INPUT panel text — they should differ

**Key attributes to point to:**
- `input.value` / `output.value` → in the **INPUT / OUTPUT panels at the top** of span detail (not Attributes)
- `agent.role` → confirms which agent is which (triage vs. rag_specialist)

---

## Scenario 3: Span Thrashing & Inefficient Routing

**What students should see in Phoenix:**
- More spans than expected (e.g., 6 spans vs. optimal 3)
- One or more spans with `tool.execution_result: error` or rejection text in `tool.output`
- Total trace duration >> expected SLA

**Student analysis task:**
> "Count actual steps vs. optimal steps. At which span should routing have been different?"

**If students can't find it:**
- Click trace timeline view in Phoenix → count spans
- Look for red/error-marked spans — these are the wrong-agent calls
- Check `tool.output` on error spans for "I do not..." rejection messages

---

## Quick Phoenix Navigation Reference

| What to look for | Where in Phoenix |
|---|---|
| User's original message | Click root span → **INPUT panel** (top of detail) |
| Agent's final response | Click root span → **OUTPUT panel** (top of detail) |
| Handoff mutation | Parent OUTPUT vs. child INPUT on adjacent CHAIN spans |
| Token counts | Click LLM span → **Attributes** → `llm.usage.*` |
| Retrieval quality | Click RETRIEVER span → **Attributes** → `quality.retrieval.*` |
| Security decision | Click `security.gate` span → **Attributes** → `security.decision` |
| Error type | Click any red span → **Attributes** → `error.type`, `error.message` |
| Agent role | Click CHAIN span → **Attributes** → `agent.role` |
| Span timing | **Timeline view** → hover over spans |

---

## If Something Doesn't Look Right

| Symptom | Check |
|---|---|
| INPUT/OUTPUT panels empty | Span was generated before today's warmup fix — run a fresh prompt |
| No `security.gate` span | Flask not restarted after code update — `python run.py` |
| Tokens show 0 | Cold-start request — second run will have counts |
| Spans exist but no attributes | Phoenix not receiving data — check http://localhost:6006 is up |
