# Exercise 4: Decompose a RAG Failure - Retriever vs. Generator Diagnosis - Instructor Notes

---

## Overview

Students diagnose why the chatbot failed on specific queries by tracing the full RAG pipeline: retriever -> context injection -> generator. The key insight is that **a RAG failure can originate in either layer**, and the fix is different for each.

**Learning Objective:** Understand the dependency chain and develop debugging skills for complex AI systems where multiple layers can fail independently.

---

## Setup Checklist (5 minutes before class)

- [ ] Flask app running: `python launch.py` -> choose option 4 (Start Flask Application).
- [ ] Verify chatbot is accessible at [http://localhost:5000](http://localhost:5000).
- [ ] Have students' Exercise 2 golden records available (or ask them to reference their own work).
- [ ] Familiarize yourself with [app/rag_pipeline.py](../app/rag_pipeline.py), especially:
  - The `_retrieve_documents()` method (returns `documents`, `metadatas`, `distances`).
  - The `_generate_response()` method (injects context into the LLM prompt).
  - The `query()` method (returns sources with similarity scores in 0-100 range).
- [ ] Optional: Pre-run 2-3 of your own Exercise 2 queries to identify a clear retriever failure and a clear generator failure. Use these as examples during facilitation.
- [ ] Have [data/documents/](../data/documents/) visible for reference (4 knowledge base files).

---

## Timing

| Phase | Time | Notes |
|-|-|-|
| Introduction & Dependency Chain (3-5 minutes) | 3 minutes | Draw the dependency chain on whiteboard. Emphasize: "Garbage in, garbage out." |
| Part A: Inspect Retriever (students work) | 15-20 minutes | Circulate; help students read similarity scores and identify weak retrieval. |
| Part B: Inspect Generator (students work) | 10-15 minutes | Students compare retrieved context to response. Are claims grounded? |
| Part C: Propose Fixes (students draft) | 10-15 minutes | Expect variety (tuning, constraints, engineering). All are valid. |
| Part D: Document Findings (students write) | 10 minutes | Quick report; emphasis on clarity over perfection. |
| Debrief & Group Share (3-5 minutes) | 5 minutes | 2-3 students share findings. Bridge to Exercise 5 (automation). |
| **Total** | **50-60 minutes** | - |

---

## Expected Findings & Known Issues

### Likely Retriever Failures Students Will Find

**Query Type: Broad/Conceptual** (e.g., "What is a hallucination?")
- **Expected:** `faq_genai_testing.md` or `genai_testing_guide.md` ranked first.
- **Likely Actual:** `production_best_practices.md` or `evaluation_metrics.md` ranked first (both contain "hallucination" but aren't the primary source).
- **Root Cause:** Embedding similarity is high for all docs mentioning "hallucination"; chunk boundaries matter. If the FAQ has a better answer but it's in chunk 8, and another doc has one mention in chunk 2, chunk 2 gets ranked higher due to position or context.
- **Student Insight:** "All documents mention hallucination, but the FAQ specifically defines it. Similarity score alone doesn't capture 'best answer.'"
- **Teaching Point:** This is why hybrid search (keyword + semantic) helps. For FAQ-type queries, exact keyword match should boost FAQ document.

**Query Type: Specific Fact** (e.g., "What are the four key metrics?")
- **Expected:** `evaluation_metrics.md` ranked first with >80% similarity.
- **Likely Actual:** Lower similarity (70-75%) if the query phrasing doesn't match the document phrasing exactly.
- **Root Cause:** Chunk size (default 2000 chars) may be too large. If the "four metrics" section is buried in a large chunk with other content, the embedding is diluted. Smaller chunks (500-1000 chars) isolate key facts and improve similarity.
- **Student Insight:** "The answer was in the document, but the chunk was too big; embedding got confused by surrounding content."
- **Teaching Point:** Chunk size is a hyperparameter. Trade-off: smaller chunks = better granularity, but more retrieval calls.

**Query Type: Multi-Step Reasoning** (e.g., "If I want to ensure faithfulness, what metrics should I use?")
- **Expected:** Multiple documents (genai_testing_guide + evaluation_metrics) ranked high.
- **Likely Actual:** Top documents may not include evaluation_metrics; only faithfulness definitions are retrieved.
- **Root Cause:** Query is complex. Embedding captures "faithfulness" but misses the "metrics" aspect. Retriever returns documents about faithfulness (correct) but not the one listing metrics.
- **Student Insight:** "The retriever got part of the answer but missed the second half. I need more documents retrieved (increase top_k) or better query preprocessing."
- **Teaching Point:** For complex queries, increasing `top_k` from 5 to 10 helps. Or implement query decomposition (break into sub-queries).

### Likely Generator Failures Students Will Find

**Hallucination: Unsupported Claims**
- **Symptom:** Response includes facts not in retrieved sources.
- **Example Query:** "What is the difference between Precision and Recall in my context?"
  - Retrieved: `evaluation_metrics.md` (defines metrics).
  - Response: "Precision means accuracy of positive predictions. Recall means finding all true positives. In your GenAI context, high Precision means few false positives in hallucination detection, whereas high Recall means catching all hallucinations."
  - **Issue:** The second sentence is correct but the specific application to "hallucination detection" is inferred, not stated in the retrieved chunk.
- **Root Cause:** Generator filled the gap from pre-training. The Cohere model "knows" about Precision/Recall in ML contexts and applied that knowledge.
- **Fix:** Stricter system prompt. Current prompt says "Based on the provided context, please answer..." but doesn't explicitly forbid external knowledge.

**Incomplete Answer: "I Don't Know" When It Shouldn't**
- **Symptom:** Response is "I don't have information on..." but the answer was in the retrieved documents.
- **Example Query:** "What is faithfulness?"
  - Retrieved: `faq_genai_testing.md` (Chunk 3: "Faithfulness is the extent to which...")
  - Response: "I don't have specific information on faithfulness in your knowledge base."
  - **Issue:** The document was retrieved but the Generator didn't read it or deemed it irrelevant.
- **Root Cause:** Possible causes:
  1. Retrieved chunk is ranked 5th due to position bias; context window cut it off (context window limit ~4000 tokens).
  2. Similarity score was 0.62 (below threshold); chunk was retrieved but filtered before injection.
  3. LLM refused because chunk's tone was informal ("Q&A" format) vs. the assertive tone it expects.
- **Fix:** Lower similarity threshold. Or implement context distillation to boost signal-to-noise ratio.

**Off-Topic Answer: Fluent but Wrong**
- **Symptom:** Response is coherent but doesn't address the query.
- **Example Query:** "How do I evaluate a RAG system?"
  - Retrieved: `genai_testing_guide.md` (Chunk 7: "RAG systems have two layers: retrieval and generation. Test them separately.")
  - Response: "RAG systems are powerful because they combine retrieval with generation. A common approach is to use ChromaDB for retrieval and Cohere for generation. Here's how you'd set up a RAG pipeline: [setup instructions]"
  - **Issue:** Response talks about *building* RAG, not *evaluating* it.
- **Root Cause:** Retriever found a document about RAG structure (good) but not the evaluation methodology. Query phrasing ("evaluate") wasn't in the retriever's top results.
- **Fix:** Increase top_k or improve query expansion (e.g., "evaluate" -> "evaluate, assess, test, metric").

### Known Issues in the Chatbot (Intentional for Students)

From [app/rag_pipeline.py](../app/rag_pipeline.py), there are documented intentional issues:

1. **Line 201: Chunk size too large (2000 chars)**
   - Students may discover that reducing to 1000-1500 chars improves specificity.

2. **Line 335: max_tokens set to 300**
   - Some responses are truncated. Students may propose increasing to 500-800.

3. **Generator prompt not strict on external knowledge**
   - Doesn't explicitly forbid pre-training knowledge (only says "based on context").

4. **No similarity threshold filtering**
   - All retrieved documents (even low similarity) are injected. Students may propose threshold (0.60 or 0.70).

**Instructor note:** These are intentional teaching bugs. When students propose fixes, affirm them: "Great diagnostic thinking. That's exactly what production teams do."

---

## Facilitation Tips

### Part A: Helping Students Inspect Retriever

**If a student is stuck:**
- Q: "Look at the source filename. Is that the document you expected?"
- Q: "The similarity is 71%. That's pretty good. But look at the top result-it's 87%. Does the 87% result actually answer the question better?"
- Q: "If I were indexing these documents, what synonym could I add to help the retriever?"

**Common mistake:**
- Students assume all failures are bugs. Reframe: "The retriever found something relevant. The question is: is it the *most* relevant thing?"
- Or: "Similarity is just one signal. A document can be semantically close but still not have the specific fact you need."

### Part B: Helping Students Inspect Generator

**If a student is stuck on hallucination vs. grounded:**
- Point to a specific sentence in the response. Q: "Find this sentence in the retrieved context. (Pause.) Did you find it?"
- If no, prompt: "That's the hallucination. The model filled in a gap."
- If yes, follow-up: "Is it a direct quote, or did the model paraphrase?"

**Common mistake:**
- Students say the generator "ignored" context when it actually just didn't retrieve good context. Reframe: "If the retriever didn't find the answer, the generator has nothing to work with. This is a retriever failure, not a generator failure."

### Part C: Helping Students Propose Fixes

**If a student proposes a retriever fix:**
- Q: "Why would lowering the threshold from 0.75 to 0.60 help? What's the trade-off?"
- Expected answer: "More documents retrieved, but more noise. Might get irrelevant docs too."
- Affirm: "Right. You'd need to measure recall vs. precision."

**If a student proposes a generator fix:**
- Q: "You want to add a citation requirement. Would that change the retriever's output?"
- Expected answer: "No, just the format of the response."
- Affirm: "Right. The LLM still uses the same context, but now it has to cite it."

**If a student is paralyzed by choice:**
- Lean them toward **Option 1 (Retriever Tuning)** if their failure was clearly a retrieval issue.
  - Easier to validate: "Rerun the query with top_k=10 instead of 5. Do you get better documents?"
- Lean them toward **Option 2 (Generator Constraint)** if the retrieved context was good but misused.
  - More abstract; requires re-prompting the LLM.
- Lean them toward **Option 3 (Context Engineering)** if they want a middle ground.
  - Transform the context before injection; doesn't change retriever or generator code.

### Part D: Documenting Findings

**Icebreaker:**
- "This is not about perfect writing. It's about clarity. A teammate should understand your finding in 30 seconds."
- Provide the report template. Students fill in blanks; no essay required.

---

## Rubric (0-2 per dimension)

### Part A: Retriever Analysis (0-2 points)

- **0:** Worksheet not completed or no retriever diagnostics documented.
- **1:** Worksheet has entries; On Target / Off Target grades given, but root cause analysis is shallow or missing for off-target cases.
- **2:** Worksheet complete; all off-target grades have clear root cause analysis (e.g., "chunk size too large," "embedding similarity mismatch," "wrong doc ranked first").

### Part B: Generator Analysis (0-2 points)

- **0:** No generator assessment or assessment is incoherent.
- **1:** Generator quality assessed (grounded / hallucinated / off-topic) but root cause not clearly identified.
- **2:** Quality assessment complete; root cause identified (e.g., "context window cut off," "position bias," "hallucination from pre-training").

### Part C: Fix Proposal (0-2 points)

- **0:** No fix proposed or proposal is vague.
- **1:** Fix proposed in one category (Tuning / Constraint / Engineering) but justification is thin.
- **2:** Fix proposed with clear category, expected impact, and trade-offs understood (e.g., "lower threshold -> more false positives").

### Part D: Diagnosis Report (0-2 points)

- **0:** Report not completed or incomplete.
- **1:** Report filled in but lacks clarity; reader has to guess the findings.
- **2:** Report is clear and complete; a teammate could understand the diagnosis in 30 seconds.

**Total: 8 points (can scale to 0-10 or 0-100 as you prefer)**

**Grading Guidance:**
- A student who completes Parts A-C thoroughly but rushes Part D -> 6/8 (solid pass; report is secondary).
- A student who identifies one retriever failure and one generator failure with fixes -> 6/8 (good decomposition, even if not all 3-4 queries analyzed).

---

## Bridge to Next Section

### Opening (Connect to Exercise 3)

*"In Exercise 3, you audited the evaluation metrics themselves. Now we flip it again: **What makes a good evaluation metric is knowing where to measure.** A RAG system has two layers-retrieval and generation. When it fails, you need to know which layer broke. That's what this exercise teaches."*

### Mid-Exercise (Part A -> Part B)

*"So the retriever pulled these documents. Good news: if they're relevant, the generator has a fighting chance. Bad news: a weak retriever defeats the best generator. That's why we always fix the retriever first, then the generator."*

### Closing (to Section Bridge)

*"You just debugged 3-4 queries manually. But in production, you have 1,000 queries a day. You can't inspect each one by hand. Before we go further - the system we've been testing is about to get more complex. Take a few minutes for the section bridge and then we'll start Exercise 5."*

**After the Exercise 4 debrief, deliver the 5-10 minute section framing talk before handing out Exercise 5.**  
See: [Section-Bridge-RAG-to-Agentic.md](Section-Bridge-RAG-to-Agentic.md)

---

## Common Student Mistakes & Corrections

| Mistake | What You Hear | Correction |
|-|-|-|
| Assumes all failures = generator hallucinated | "The chatbot made stuff up." | "Maybe the retriever didn't find the right document. Check: what was retrieved? Is it relevant?" |
| Proposes fix without understanding trade-off | "I'll lower the threshold to 0.50." | "Why 0.50? What happens if you retrieve 10 documents instead of 5-do you get noise? How would you measure?" |
| Doesn't actually test the fix | "I think increasing top_k would help." | "Let's test it. Rerun with top_k=10 instead of 5. Tell me if the retrieved docs improved." |
| Conflates similarity score with relevance | "The similarity is high so the doc is relevant." | "High similarity to what? The query. But the query might be ambiguous. A doc can be semantically similar but not answer the question." |
| Attributes problem to LLM quality | "Cohere's model is weak." | "Maybe. But first: is Cohere getting good context? Fix the pipeline before blaming the model." |

---

## Answers to Anticipated Questions

**Q: Can I actually modify the chatbot code to test my fix?**
A: Yes! For retriever tuning (top_k, threshold), you can edit [app/rag_pipeline.py](../app/rag_pipeline.py) lines 310-325. For generator constraints, modify the system prompt in `_generate_response()` (line 335). After changes, restart the Flask server and re-query. (Or use [experiments/retrieval_experiments.py](../experiments/retrieval_experiments.py) to test retrieval tuning in isolation.)

**Q: What if the chatbot refuses to answer, but the document is clearly relevant?**
A: Possible causes:
1. Context window limit (context was truncated before reaching the LLM).
2. Similarity filtering (document was retrieved but then filtered out).
3. LLM confidence (Cohere's internal confidence was low).
Check the `retrieval_time`, number of sources injected, and source similarities. If sources look good but response is "I don't know," it's likely a context window or confidence issue.

**Q: Should I propose multiple fixes per query?**
A: One primary fix per query is fine for this exercise. In production, you'd iterate: fix the retriever, measure impact, then fix the generator. Don't try to fix both at once; you won't know which fix helped.

**Q: Can I use a different LLM to test generator issues?**
A: Not easily in this exercises-the chatbot is hardcoded to Cohere. But you can propose a fix conceptually (e.g., "add a citation requirement to the system prompt") and explain how you'd test it. In Exercise 5, you'll measure impact on real traffic.

**Q: What if I can't identify a clear retriever vs. generator failure?**
A: That's okay. Propose: "This looks like a mixed failure-retriever found a weak document, and the generator misused it." Then propose a fix that addresses one layer and explain what you'd measure to validate it.

---

## Optional Stretch Activities

If a group finishes early:

1. **Code Modification:** Have them edit [app/rag_pipeline.py](../app/rag_pipeline.py) to implement one of their tuning fixes (e.g., increase top_k) and re-run a query to measure before/after.
2. **Automated Trace:** Have them write a simple script that queries the chatbot 10 times, captures the sources, and logs any low-similarity results. Then propose a pattern (e.g., "queries with 'new' terminology tend to have low similarity").
3. **Prompt A/B Test:** Have them draft two versions of the system prompt (one strict, one loose on external knowledge) and compare responses to the same query.

---

## Pre-Class Prep for You

- [ ] Skim [app/rag_pipeline.py](../app/rag_pipeline.py), focus on:
  - `_retrieve_documents()` (line ~310): Returns `documents`, `metadatas`, `distances`.
  - `_generate_response()` (line ~335): System prompt where external knowledge constraints live.
  - `query()` (line ~375): Where sources are annotated with similarity scores.
- [ ] Run 2 of your own Exercise 2 queries and note:
  - Which sources were retrieved for each (write down filenames).
  - Were they the "right" documents?
  - Did the response stick to the retrieved context, or add external knowledge?
- [ ] Prepare a 3-minute demo of inspecting sources in the chatbot UI (show where similarity scores appear).
- [ ] If confident, prepare a live code edit: change `n_results = 5` to `n_results = 10` in rag_pipeline.py, restart Flask, and requery to show the difference.

---

## Debrief (5 minutes)

**Go around the room. Ask 2-3 students:**

1. *"Of your 3-4 failures, how many were retriever failures vs. generator failures?"*
   - Expected: Likely 2-3 retriever, 1-2 generator. Retriever is the constraint.
   
2. *"What was the most surprising finding-something you didn't expect to see in the sources?"*
   - Expected: E.g., "Low similarity score for a document I thought was obviously relevant," or "All 5 documents mentioned 'hallucination' but they were all tangentially related."
   
3. *"If you had to pick one fix to deploy today, what would it be?"*
   - Expected: Usually "increase top_k" or "lower similarity threshold" (retriever fixes are easy to implement). Affirm this: "Right-quick wins in production."


