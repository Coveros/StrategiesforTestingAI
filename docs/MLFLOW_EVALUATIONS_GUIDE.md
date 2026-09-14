# MLflow Evaluations Guide: Automated AI Testing Metrics

## About Evaluations: No API Key Required

MLflow Evaluations use `mlflow.genai.scorers` to score your outputs. Unlike the previous Phoenix-based setup, scorers can run against a **local Ollama model** (`model="ollama:/<model-name>"`), so no external API key, quota, or per-call cost applies.

**Local Option (default for this course):**
- **Ollama** (local) — Free, no API key, uses the same model already running for the course

**Optional External Options** (if you want to compare judge models):
- **OpenAI GPT-4**, **Anthropic Claude**, **Cohere** — supported by `mlflow.genai.scorers` if you configure the relevant API key

**Bottom Line:** This guide's default path needs **no API key at all**. It is still **optional** — you can test AI systems effectively using free **traces** alone.

---

## Overview

MLflow Evaluations are **automated scoring functions** that assess LLM quality across multiple dimensions:
- **Hallucination Detection**: Did the model make up facts not in the context?
- **Relevance**: How well did the model answer the user's question?
- **Groundedness**: Did the model only use provided sources?
- **Tool Accuracy**: Did the agent call tools correctly?
- **Consistency**: Do repeated runs produce similar outputs?

This guide shows how to set up, run, and interpret evaluations for your 2-day testing course.

---

## Part 1: Built-In Evaluations (Easy Start)

### About Cost

Built-in scorers run against whatever judge model you configure. The default for this course is a **local Ollama model — no external API calls, no cost, no rate limits**.

### What's Available Out of the Box

`mlflow.genai.scorers` ships with built-in scorers:

| Scorer | Purpose | Input | Output |
|---|---|---|---|
| **Safety** | Flags unsafe/harmful content | LLM output | score 0-1 |
| **RelevanceToQuery** | Grades answer quality | User query + output | score 0-1 |
| **RetrievalGroundedness** | Ensures source fidelity | Context + output | score 0-1 |
| **Correctness** | Compares to reference answer | Output + gold standard | score 0-1 |

### Step 1: Enable Built-In Scorers in Your App

Point scorers at a local Ollama model — no API key needed:

```bash
MLFLOW_EVAL_ENABLED=true
MLFLOW_EVAL_MODEL=ollama:/llama3.2:1b  # local model, no API key required
```

Or add to `.devcontainer/devcontainer.json`:
```json
"remoteEnv": {
  "MLFLOW_EVAL_ENABLED": "true",
    "MLFLOW_EVAL_MODEL": "ollama:/llama3.2:1b"
}
```

### Step 2: Access Evaluators Tab in MLflow UI

1. Go to http://localhost:5001
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
from mlflow.genai.scorers import RelevanceToQuery, RetrievalGroundedness, Safety
import asyncio

async def evaluate_rag_quality(
    query: str, 
    response: str, 
    context: str,
    retrieved_docs: List[str],
):
    """Run RAG-specific scorers against a local Ollama model."""
    
    model = "ollama:/llama3.2:1b"
    
    # Safety: Did response avoid unsafe/harmful content?
    safety_score = Safety(model=model)(outputs=response)
    
    # RelevanceToQuery: How well did it answer?
    relevance_score = RelevanceToQuery(model=model)(inputs=query, outputs=response)
    
    # RetrievalGroundedness: Only used context?
    groundedness_score = RetrievalGroundedness(model=model)(
        inputs=query, outputs=response, context=context,
    )
    
    return {
        "safety": safety_score,
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
    if os.getenv("MLFLOW_EVAL_ENABLED") == "true":
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
    
    model = "ollama:/llama3.2:1b"
    
    # Tool Correctness: Were tools called appropriately?
    # (Create custom scorer — see Part 3 below)
    
    # Final Answer Quality: Does agent response make sense?
    relevance = RelevanceToQuery(model=model)(inputs=query, outputs=agent_response)
    
    return {"tool_correctness": ..., "response_relevance": relevance}
```

---

## Part 3: Custom Evaluators (For Course-Specific Metrics)

### Example: Hallucination Detection for Testing

This evaluator checks if the response references facts **not** in the retrieved context:

```python
from mlflow.genai.scorers import scorer
from pydantic import BaseModel, Field

class HallucinationClassification(BaseModel):
    """Is the response hallucinating?"""
    score: float = Field(..., ge=0, le=1, description="0=fully hallucinating, 1=fully grounded")
    reasoning: str = Field(..., description="Why this score?")
    unsupported_facts: List[str] = Field(default_factory=list, description="Facts not in context")

async def hallucination_with_detail(
    model,
    query: str,
    response: str,
    context: str,
) -> HallucinationClassification:
    """Detailed hallucination detection using a custom scorer."""
    
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
    
    completion = model.create_message(prompt=prompt)
    # Parse response into HallucinationClassification
    return parse_structured_output(completion, HallucinationClassification)
```

### Example: Tool Selection Correctness

```python
async def tool_selection_evaluator(
    model,
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
    
    completion = model.create_message(prompt=prompt)
    return parse_result(completion)
```

### Registering Custom Scorers

```python
from mlflow.genai.scorers import scorer

# Register scorer with the @scorer decorator
@scorer
def hallucination_detail(inputs, outputs, context) -> float:
    return hallucination_with_detail("ollama:/llama3.2:1b", inputs, outputs, context)

@scorer
def tool_selection(inputs, outputs, tools_used) -> float:
    return tool_selection_evaluator("ollama:/llama3.2:1b", inputs, [], tools_used, {})

# Access results in MLflow UI:
# Go to Traces → select a trace → Assessments panel
```

---

## Part 4: Running Batch Evaluations on Historical Traces

### Via Python Script

```python
import asyncio
import mlflow

async def batch_evaluate_traces():
    """Evaluate all traces from today."""
    
    client = mlflow.MlflowClient()
    experiment = client.get_experiment_by_name("strategiesfortestingai")
    
    # Fetch all traces
    traces = client.search_traces(experiment_ids=[experiment.experiment_id])
    
    results = []
    for trace in traces:
        eval_result = await evaluate_trace(trace)
        results.append({
            "trace_id": trace.info.trace_id,
            "timestamp": trace.info.timestamp_ms,
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

### Via MLflow UI (No Code Required)

1. **Traces Tab** → select traces → **Evaluate**
2. Select scorers (Safety, RelevanceToQuery, RetrievalGroundedness)
3. Select date range (e.g., "last 24 hours")
4. Click **Run**
5. Results populate as trace **Assessments**

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

After running evaluations, MLflow shows:

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

### Problem: "No assessments show up on my traces"

**Solution:**
1. Check MLflow is running: `pgrep -f "mlflow.*server"`
2. Verify at least one trace exists in Traces tab
3. Confirm `MLFLOW_EVAL_ENABLED=true` is set
4. Confirm Ollama is running and the model in `MLFLOW_EVAL_MODEL` is pulled

### Problem: "Scores are all 0 or 1"

**Solution:**
- Judge model (local Ollama) may not have access to span data
- Ensure spans include `input.value` and `output.value`
- Try running manually: `python -c "from mlflow.genai.scorers import Safety; print(Safety(model='ollama:/llama3.2:1b')(outputs='test'))"`

### Problem: "Evaluations are too slow (>30 sec per trace)"

**Solution:**
- Use a smaller local Ollama model (e.g., `llama3.2:1b`)
- Sample traces: evaluate only 10% of all traces
- Run evaluations overnight in batch mode

### Problem: "I don't see my custom scorer in MLflow UI"

**Solution:**
- Custom scorers don't auto-appear in UI
- Create them with the `@scorer` decorator and call manually
- Or register them for automated runs (advanced)

---

## Quick Start (5 Minutes)

### No API Key Needed

This guide's default path uses a **local Ollama model** as the judge — no external API key, quota, or cost. Optional external judge models (OpenAI, Claude, Cohere) are supported by `mlflow.genai.scorers` if you'd rather compare judge models, but are not required.

### Setup Steps

1. **Confirm Ollama is running** and has the model pulled (the same model used for the course app is fine).

2. **Add to `.env`:**
   ```bash
   MLFLOW_EVAL_ENABLED=true
    MLFLOW_EVAL_MODEL=ollama:/llama3.2:1b
   ```

3. **Create a trace** (ask something on Flask app)

4. **Open the MLflow UI → Traces tab**

5. **Select traces → Evaluate** (runs the configured scorers)

6. **Wait a few seconds, then refresh**

7. **View scores as Assessments on each trace**

That's it! You now have automated quality metrics for all three modes (Ask, Agent, Crew).

---

## References

- [MLflow GenAI Scorers Docs](https://mlflow.org/docs/latest/genai/eval-monitor/scorers/)
- [MLflow Evaluation Docs](https://mlflow.org/docs/latest/genai/eval-monitor/)
- [LLM Evaluators Best Practices](https://arxiv.org/abs/2401.10020)
