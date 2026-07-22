# Phoenix Evaluations Guide: Automated AI Testing Metrics

## About Evaluations: Cost and API Keys

Phoenix Evaluations use external LLM services to score your outputs. You have options:

**Free Tier Options:**
- **Cohere** — Free tier (limited requests/month)
- **HuggingFace** — Free tier (limited inference)
- **Ollama** (local) — Completely free, but limited evaluation support
- **Anthropic Claude** — Free trial credits ($5-10)

**Paid Options:**
- **OpenAI GPT-4** — $0.01-0.05 per evaluation
- **Anthropic Claude (post-trial)** — Varies by model

**Cost Estimate:** If you run 100 evaluations on free tier, cost is $0-5. On paid tier, budget $1-5 per 100 traces.

**Bottom Line:** You *can* use a free API key (Cohere, HuggingFace) with limited quota, or free credits (Claude trial). This guide is still **optional** — you can test AI systems effectively using free **traces** alone.

---

## Overview

Phoenix Evaluations are **automated scoring functions** that assess LLM quality across multiple dimensions:
- **Hallucination Detection**: Did the model make up facts not in the context?
- **Relevance**: How well did the model answer the user's question?
- **Groundedness**: Did the model only use provided sources?
- **Tool Accuracy**: Did the agent call tools correctly?
- **Consistency**: Do repeated runs produce similar outputs?

This guide shows how to set up, run, and interpret evaluations for your 2-day testing course.

---

## Part 1: Built-In Evaluations (Easy Start)

### About Cost

Built-in evaluators use **external LLM API calls**. You have free and paid options:

- **Free Tier**: Cohere (limited quota), HuggingFace (limited), Claude trial ($5-10 free)
- **Paid**: OpenAI GPT-4 ($0.01-0.05 per evaluation)

If you use a free tier API, evaluations are free (subject to rate limits). If you use a paid API, budget accordingly.

### What's Available Out of the Box

Phoenix ships with evaluators powered by Claude/GPT/Cohere:

| Evaluator | Purpose | Input | Output |
|---|---|---|---|
| **Hallucination** | Detects unsupported claims | LLM output + context | score 0-1 |
| **Relevance** | Grades answer quality | User query + output | score 0-1 |
| **Groundedness** | Ensures source fidelity | Context + output | score 0-1 |
| **QA Correctness** | Compares to reference answer | Output + gold standard | score 0-1 |

### Step 1: Enable Built-In Evaluators in Your App

Choose your API provider (free or paid):

**Option A: Free Tier (Cohere)**
```bash
PHOENIX_EVAL_ENABLED=true
PHOENIX_EVAL_MODEL=cohere  # Free tier available
PHOENIX_EVAL_API_KEY=YOUR_COHERE_KEY
```

**Option B: Free Trial (Anthropic Claude)**
```bash
PHOENIX_EVAL_ENABLED=true
PHOENIX_EVAL_MODEL=claude-3-haiku
PHOENIX_EVAL_API_KEY=sk-ant-YOUR_KEY
```

**Option C: Paid (OpenAI)**
```bash
PHOENIX_EVAL_ENABLED=true
PHOENIX_EVAL_MODEL=gpt-4-turbo
PHOENIX_EVAL_API_KEY=sk-proj-YOUR_KEY
```

Or add to `.devcontainer/devcontainer.json`:
```json
"remoteEnv": {
  "PHOENIX_EVAL_ENABLED": "true",
  "PHOENIX_EVAL_MODEL": "cohere"
}
```

### Step 2: Access Evaluators Tab in Phoenix UI

1. Go to http://localhost:6006
2. Click **Evaluators** tab (next to Traces)
3. You should see a list of available evaluators
4. Click **"Run All"** or select specific evaluators

### Step 3: Select Traces to Evaluate

1. In the Evaluators panel, click **"Select Traces"**
2. Choose traces you want to score (e.g., all traces from today)
3. Click **"Run Evaluations"** 
4. Wait for evaluation jobs to complete (2-10 seconds per trace)

### Step 4: View Evaluation Results

Results appear in:
- **Evaluators Tab** → Shows individual evaluation scores
- **Traces Tab** → Scores appear as columns on each trace row
- **Projects → Analytics** → Aggregated metrics (average, distribution)

---

## Part 2: Pre-Built Evaluators for Your Course

### For Ask/RAG Mode

**Setup Code** (add to `app/rag_pipeline.py` or new file `app/evaluations.py`):

```python
from phoenix.evals import OpenAIModel, hallucination_evaluator, relevance_evaluator
import asyncio

async def evaluate_rag_quality(
    query: str, 
    response: str, 
    context: str,
    retrieved_docs: List[str],
):
    """Run RAG-specific evaluators."""
    
    client = OpenAIModel(model="gpt-4-turbo")
    
    # Hallucination: Did response make up facts?
    hallucination_score = await hallucination_evaluator(
        client,
        query=query,
        response=response,
        context=context,  # Concatenated retrieved docs
    )
    
    # Relevance: How well did it answer?
    relevance_score = await relevance_evaluator(
        client,
        query=query,
        response=response,
    )
    
    # Groundedness: Only used context?
    groundedness_score = await groundedness_evaluator(
        client,
        context=context,
        response=response,
    )
    
    return {
        "hallucination": hallucination_score,
        "relevance": relevance_score,
        "groundedness": groundedness_score,
    }
```

**Integration Point** (add to Flask route after RAG query):

```python
@app.route("/api/ask", methods=["POST"])
def ask():
    query = request.json.get("query")
    response_data = rag.query(query)
    
    # Optionally run evaluations
    if os.getenv("PHOENIX_EVAL_ENABLED") == "true":
        try:
            eval_scores = asyncio.run(evaluate_rag_quality(
                query=query,
                response=response_data["response"],
                context="\n\n".join(response_data.get("context_docs", [])),
            ))
            response_data["eval_scores"] = eval_scores
        except Exception as e:
            logger.warning("Evaluation failed: %s", e)
    
    return jsonify(response_data)
```

### For Agent Mode

```python
async def evaluate_agent_trajectory(
    query: str,
    agent_response: str,
    tools_used: List[str],
    tool_inputs: List[Dict],
    tool_outputs: List[str],
):
    """Evaluate agent decision-making and tool correctness."""
    
    client = OpenAIModel(model="gpt-4-turbo")
    
    # Tool Correctness: Were tools called appropriately?
    # (Create custom evaluator — see Part 3 below)
    
    # Final Answer Quality: Does agent response make sense?
    relevance = await relevance_evaluator(
        client,
        query=query,
        response=agent_response,
    )
    
    return {"tool_correctness": ..., "response_relevance": relevance}
```

---

## Part 3: Custom Evaluators (For Course-Specific Metrics)

### Example: Hallucination Detection for Testing

This evaluator checks if the response references facts **not** in the retrieved context:

```python
from phoenix.evals import OpenAIModel
from pydantic import BaseModel, Field

class HallucinationClassification(BaseModel):
    """Is the response hallucinating?"""
    score: float = Field(..., ge=0, le=1, description="0=fully hallucinating, 1=fully grounded")
    reasoning: str = Field(..., description="Why this score?")
    unsupported_facts: List[str] = Field(default_factory=list, description="Facts not in context")

async def hallucination_with_detail(
    client,
    query: str,
    response: str,
    context: str,
) -> HallucinationClassification:
    """Detailed hallucination detection."""
    
    prompt = f"""
    User Query: {query}
    
    Context (ONLY these facts should be referenced):
    {context}
    
    Model Response:
    {response}
    
    Task: Score 0-1 how much the response stays grounded in the context.
    - 1.0 = All facts come from context
    - 0.5 = Mix of grounded and hallucinated facts
    - 0.0 = Response is pure hallucination
    
    Also list any facts in the response NOT found in context.
    """
    
    completion = client.create_message(prompt=prompt)
    # Parse response into HallucinationClassification
    return parse_structured_output(completion, HallucinationClassification)
```

### Example: Tool Selection Correctness

```python
async def tool_selection_evaluator(
    client,
    query: str,
    tools_available: List[str],
    tools_used: List[str],
    tool_description: Dict[str, str],  # {tool_name: description}
) -> Dict:
    """Did the agent pick the right tool for the job?"""
    
    prompt = f"""
    User Query: {query}
    
    Available Tools:
    {json.dumps(tool_description, indent=2)}
    
    Tools Agent Selected: {', '.join(tools_used)}
    
    Task: Rate 0-1 whether the tool selection was appropriate.
    - 1.0 = Perfect tool choice
    - 0.5 = Acceptable but not optimal
    - 0.0 = Wrong tool for the job
    """
    
    completion = client.create_message(prompt=prompt)
    return parse_result(completion)
```

### Registering Custom Evaluators

```python
from phoenix.experiments import EvaluationDataset

# Register evaluator
evaluator_registry = {
    "hallucination_detail": hallucination_with_detail,
    "tool_selection": tool_selection_evaluator,
}

# Access in Phoenix UI:
# Go to Evaluators → Custom → Select "hallucination_detail"
```

---

## Part 4: Running Batch Evaluations on Historical Traces

### Via Python Script

```python
import asyncio
from phoenix.client import Client

async def batch_evaluate_traces():
    """Evaluate all traces from today."""
    
    client = Client()
    project = client.get_project("strategiesfortestingai")
    
    # Fetch all traces
    traces = project.traces()
    
    results = []
    for trace in traces:
        eval_result = await evaluate_trace(trace)
        results.append({
            "trace_id": trace.id,
            "timestamp": trace.start_time,
            **eval_result,
        })
    
    return results

# Run it
results = asyncio.run(batch_evaluate_traces())

# Save results
import pandas as pd
df = pd.DataFrame(results)
df.to_csv("evaluation_results.csv", index=False)
```

### Via Phoenix UI (No Code Required)

1. **Evaluators Tab** → **Batch Run**
2. Select evaluators (hallucination, relevance, groundedness)
3. Select date range (e.g., "last 24 hours")
4. Click **Run All**
5. Results populate automatically

---

## Part 5: Interpreting Evaluation Results

### Understanding Scores

| Score | Interpretation |
|---|---|
| **0.9-1.0** | Excellent; model is high quality |
| **0.7-0.89** | Good; acceptable for production |
| **0.5-0.69** | Fair; needs improvement |
| **0.3-0.49** | Poor; significant issues |
| **0.0-0.29** | Fail; unacceptable |

### Example Results Dashboard

After running evaluations, Phoenix shows:

```
Trace ID: trace-123
├─ Hallucination Score: 0.92 (Excellent)
├─ Relevance Score: 0.78 (Good)
├─ Groundedness Score: 0.85 (Good)
└─ Token Efficiency: 145 tokens / 200 input = 0.73

Summary: Response is well-grounded and relevant, minor hallucination risk
```

### What Each Score Means for Your Course

**Hallucination: 0.92**
- ✅ Response stays grounded in context
- Use this to teach: "Model correctly avoided speculation"

**Relevance: 0.78**
- ⚠️ Response somewhat answers the question
- Use this to teach: "Model missed nuances in the query"

**Groundedness: 0.85**
- ✅ Response sources are cited correctly
- Use this to teach: "Model properly used retrieval results"

---

## Part 6: Using Evaluations in Your Exercises

### Exercise: Hallucination Detection (Day 1)

**Student Task:**
1. Modify prompt to be intentionally vague
2. Compare hallucination scores before/after
3. Document: "What caused hallucination to spike?"

**Setup:**
```python
# Before: clear prompt
query = "What are the three main benefits of X?"
score_before = evaluate(query)  # e.g., 0.92

# After: vague prompt  
query = "Tell me about X"
score_after = evaluate(query)  # e.g., 0.65

# Students analyze the drop
```

### Exercise: Tool Correctness (Day 2)

**Student Task:**
1. Add a new tool to the agent
2. Run evaluation on tool selection
3. Verify agent uses tool appropriately

**Setup:**
```python
tools_evaluations = await evaluate_agent_trajectory(
    query="...",
    tools_used=["search", "calculator", "new_tool"],
)
# Students verify: Did agent use new_tool when needed?
# Expected: tool_correctness > 0.8
```

### Exercise: Consistency Testing (Day 3)

**Student Task:**
1. Run same query 5 times
2. Collect hallucination/relevance scores
3. Plot standard deviation

**Setup:**
```python
results = []
for run in range(5):
    score = evaluate_rag_quality(same_query)
    results.append(score)

# Plot distribution
import matplotlib.pyplot as plt
plt.hist([r["hallucination"] for r in results])
plt.title("Hallucination Score Distribution (5 runs)")
plt.show()
# Students learn: "High variance = unreliable model"
```

---

## Part 7: Troubleshooting Evaluations

### Problem: "Evaluations Tab is empty"

**Solution:**
1. Check Phoenix is running: `pgrep -f "phoenix.*serve"`
2. Verify at least one trace exists in Traces tab
3. Go to **Projects → [Your Project] → Configuration**
4. Click **"Auto-detect evaluators"** if available

### Problem: "Evaluations run but scores are all 0 or 1"

**Solution:**
- Evaluator model (GPT-4) may not have access to span data
- Ensure spans include `llm.prompts.0`, `llm.completions.0.content`, `input.value`
- Try running manually: `python -c "from phoenix.evals import hallucination_evaluator; ..."`

### Problem: "Evaluations are too slow (>30 sec per trace)"

**Solution:**
- Use cheaper model: `gpt-3.5-turbo` instead of `gpt-4`
- Sample traces: evaluate only 10% of all traces
- Run evaluations overnight in batch mode

### Problem: "I don't see my custom evaluator in Phoenix UI"

**Solution:**
- Custom evaluators don't auto-appear in UI
- Create them in a Python script and call manually
- Or submit to Phoenix's evaluator registry (advanced)

---

## Quick Start (5 Minutes)

### ⚠️ Before You Start: Do You Have a Free or Paid API Key?

**If NO API key** → Skip this section. Use free **Traces** tab instead (see PHOENIX_TESTING_DATA_GUIDE.md).

**If YES API key (free or paid)** → Continue below.

Free options: [Get Cohere key](https://dashboard.cohere.com) | [Get Claude trial](https://console.anthropic.com)

### Setup Steps

1. **Get an API key** (free or paid):
   - **Cohere Free Tier**: https://dashboard.cohere.com
   - **Claude Trial**: https://console.anthropic.com ($5-10 free credits)
   - **OpenAI**: https://platform.openai.com (paid)

2. **Add to `.env`:**
   ```bash
   PHOENIX_EVAL_ENABLED=true
   PHOENIX_EVAL_MODEL=cohere          # or claude-3-haiku or gpt-4-turbo
   PHOENIX_EVAL_API_KEY=YOUR_KEY_HERE
   ```

3. **Create a trace** (ask something on Flask app)

4. **Open Phoenix → Evaluators tab**

5. **Click "Run All Evaluators"** (uses your free/paid quota)

6. **Wait 10 seconds, then refresh**

7. **View scores in Traces tab or Evaluators tab**

That's it! You now have automated quality metrics for all three modes (Ask, Agent, Crew).

---

## References

- [Phoenix Evaluations Docs](https://docs.arize.com/phoenix/evals)
- [OpenAI Evals Library](https://github.com/openai/evals)
- [LLM Evaluators Best Practices](https://arxiv.org/abs/2401.10020)
