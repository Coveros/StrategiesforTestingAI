# Module 6: Multi-Agent Handoff & Trajectory Analysis Prompts

**Goal:** Run these prompts in multi-agent (crew) mode and observe how handoffs between the Triage Agent and specialists affect retrieval quality and query integrity. Use MLflow to diagnose handoff mutations, state corruption, and trajectory completeness.

**Module 6 Focus:** Handoff contracts, query integrity, multi-agent coordination

---

## How to Run

1. **Start the system:**
   ```bash
   python run.py              # Flask app
   mlflow server --backend-store-uri sqlite:///mlflow_data/mlflow.db --host 0.0.0.0 --port 5001  # MLflow (separate terminal)
   ```

2. **Run a prompt:**
   - Open http://localhost:5000 in your browser
   - Select **Agent Mode** (multi-agent / crew mode)
   - Enter a prompt from the list below
   - Click **Submit**

3. **Analyze in MLflow:**
   - Open http://localhost:5001 → Traces tab
   - Click your trace
   - Focus on: Handoff spans, query mutation, retrieval success/failure

---

## Prompt List & What to Look For

### Category 1: Handoff Integrity & State Mutation

**Prompt 1:** `Can you retrieve information about regression testing frameworks for ensuring LLM safety in 2024?`
- **Expected:** Triage Agent routes to RAG Specialist WITH original query intact
- **In MLflow:** Look at:
  - `handoff.original_query` (what Triage Agent sent): Contains "2024", "LLM safety", "regression testing"
  - `handoff.routed_query` (what RAG Specialist received): Should be identical or semantically equivalent
  - `query_knowledge_base` INPUT: Does it include the full context?
  - Retrieval success: Did the specialist get relevant docs?
- **Module 6 Concept:** Query integrity across handoff boundary
- **Test:** Is the context preserved, or mutated?

**Prompt 2:** `What are the key differences between deterministic and probabilistic test strategies?`
- **Expected:** Triage Agent routes to RAG Specialist; compare original vs received query
- **In MLflow:** Look for:
  - `handoff.original_query`: "deterministic vs probabilistic"
  - `handoff.routed_query`: Any simplification or rewording?
  - Retrieval TOOL OUTPUT: Did specialist get relevant docs for "test strategies"?
- **Module 6 Concept:** Handoff contract enforcement—does context survive routing?
- **Test:** Can the specialist reconstruct the original intent?

**Prompt 3:** `Compare two regression test strategies and explain which is better for GenAI applications.`
- **Expected:** Multi-step handoff with comparison reasoning
- **In MLflow:** Look for:
  - Handoff chain: Triage → Specialist → (any validator?)
  - Each handoff: Does specialist receive enough context for comparison?
  - Retrieval: Did it find docs on both strategies?
  - Agent response: Is it grounded in retrieval, or hallucinated comparisons?
- **Module 6 Concept:** Trajectory completeness across multi-step handoffs
- **Test:** Does the reasoning chain stay coherent across agent boundaries?

---

### Category 2: Handoff Routing Decisions (When to use RAG vs. General Chat)

**Prompt 4:** `I need help understanding test coverage metrics. Should I prioritize line coverage or branch coverage?`
- **Expected:** Triage Agent decides: Is this domain-specific (needs RAG) or general reasoning?
- **In MLflow:** Look for:
  - Triage Agent decision: Routes to RAG or general_chat_agent?
  - If RAG: `retrieval.documents_returned` > 0?
  - If general_chat: Why didn't it retrieve? (Agent decided coverage is general knowledge?)
- **Module 6 Concept:** Routing heuristics—how does Triage decide retrieval necessity?
- **Test:** Does the agent recognize test metrics as domain knowledge vs. general reasoning?

**Prompt 5:** `What are the best practices for testing AI applications at scale?`
- **Expected:** Topic is in knowledge base; Triage routes to RAG Specialist
- **In MLflow:** Look at:
  - `handoff.original_query`: "best practices for testing AI applications at scale"
  - Specialist retrieval: `query_knowledge_base` returns docs on "AI testing" or "scale"?
  - Response: Is it grounded in retrieval results?
- **Module 6 Concept:** Relevance detection—does Triage correctly identify retrieval-worthy queries?
- **Test:** Can the system distinguish in-domain knowledge vs. general reasoning?

---

### Category 3: Retrieval Quality & Grounding After Handoff

**Prompt 6:** `Find and summarize information about automated testing for LLMs`
- **Expected:** Triage routes to RAG Specialist; specialist retrieves and grounds response
- **In MLflow:** Look for:
  - Handoff query preservation
  - `query_knowledge_base` OUTPUT: Docs about "automated testing" + "LLMs"?
  - RAG Specialist response: Grounded in retrieved docs or hallucinated?
  - Evidence: Compare retrieval doc snippets vs. specialist's claim
- **Module 6 Concept:** Retrieval quality post-handoff—does grounding survive?
- **Test:** Is the specialist correctly using retrieved context, or making up information?

**Prompt 7:** `What guidelines exist for testing fairness and bias in AI systems?`
- **Expected:** RAG routes to Specialist; specialist uses retrieved fairness/bias guidelines
- **In MLflow:** Look at:
  - Retrieval match: Are docs about "fairness" + "bias" + "AI"?
  - Response quality: Does specialist cite guidelines, or overgeneralize?
  - Handoff integrity: Did Specialist receive "fairness" keyword intact?
- **Module 6 Concept:** Multi-word query preservation across handoff
- **Test:** Can specialist maintain context across multiple dimensions (fairness AND bias AND AI)?

---

### Category 4: Handoff Resilience & Degradation

**Prompt 8:** `Retrieve test strategies` (minimal context)
- **Expected:** Triage routes to RAG; retrieval works despite sparse query
- **In MLflow:** Look for:
  - `handoff.original_query`: Very short ("test strategies")
  - `query_knowledge_base` OUTPUT: Does sparse query still match docs?
  - Response quality: Vague or specific?
- **Module 6 Concept:** How well does the system handle incomplete context at handoff boundary?
- **Test:** Does the specialist recover gracefully, or does retrieval fail?

**Prompt 9:** `Compare unit testing vs integration testing in the context of LLM evaluation frameworks`
- **Expected:** Multi-faceted query; handoff should preserve all dimensions
- **In MLflow:** Look for:
  - Original query has 4 concepts: "unit testing", "integration testing", "LLM evaluation", "frameworks"
  - Handoff query: All concepts preserved or simplified?
  - Retrieval: Did specialist find docs on BOTH unit and integration?
  - Response: Are both approaches compared, or only one?
- **Module 6 Concept:** Handoff accuracy under query complexity
- **Test:** Does complex context survive multi-agent routing?

**Prompt 10:** Run Prompt 1 three times in sequence
- **Expected:** Three separate traces with same query
- **In MLflow:** Compare all three traces:
  - Does routing decision stay the same?
  - Does handoff query mutation pattern repeat?
  - Are retrieval results identical?
  - Latency variance?
- **Module 6 Concept:** Consistency of handoff behavior
- **Test:** Is handoff integrity deterministic or probabilistic?

---

## Recording Your Observations

| Prompt | Handoff Decision | Query Intact? | Retrieval Success? | Response Grounded? | Mutation Observed? |
|---|---|---|---|---|---|
| Regression + 2024 | RAG / Direct | Yes / No | Yes / No | Yes / No | — |
| Deterministic vs Probabilistic | RAG / Direct | Yes / No | Yes / No | Yes / No | — |
| Compare 2 strategies | RAG / Direct | Yes / No | Yes / No | Yes / No | — |
| Coverage metrics decision | RAG / Direct | Yes / No | Yes / No | Yes / No | Reason? |
| AI testing at scale | RAG / Direct | Yes / No | Yes / No | Yes / No | — |
| Automated LLM testing | RAG / Direct | Yes / No | Yes / No | Yes / No | — |
| Fairness + Bias testing | RAG / Direct | Yes / No | Yes / No | Yes / No | Keywords preserved? |
| Minimal "test strategies" | RAG / Direct | Sparse / Full | Yes / No | Yes / No | Recovery? |
| Complex multi-faceted | RAG / Direct | Yes / No | Both / One / None | Yes / No | Simplification? |
| Consistency (3x) | — | Same / Different | — | — | Pattern repeats? |

---

## Discussion Questions

After running these prompts, focus on **handoff integrity and trajectory analysis**:

1. **Which prompts preserved full query context through the handoff?** Which ones were simplified or mutated?
2. **Did handoff mutations cause retrieval failures?** Can you trace a mutation directly to a failed retrieval?
3. **For multi-faceted queries (like Prompt 9), did the specialist receive all dimensions?** Which ones were preserved, which lost?
4. **Did the three repetitions of Prompt 1 show consistent handoff behavior?** Or did query mutation vary?
5. **If you were designing a handoff contract, what would you require?** (Format validation? Checksum? Explicit state schema?)
6. **How would you detect a handoff corruption attack?** (Trace inspection? Metadata validation?)

---

## Tips for MLflow Analysis

- **Handoff spans:** Look for spans labeled with `handoff.original_query` and `handoff.routed_query` attributes
- **Query comparison:** Side-by-side: does the routed query match the original? Highlight differences.
- **Retrieval quality:** If handoff mutated the query, did retrieval fail to find relevant docs?
- **Multi-span comparison:** Use MLflow's compare feature to line up the same prompt across 3 runs—spot consistency/variance
- **Attributes section:** Look for `handoff.*` fields, `query_knowledge_base.input`, `retrieval.documents_returned`
- **Span tree depth:** More handoffs = deeper tree. Are all agents being invoked, or is one step skipped?

