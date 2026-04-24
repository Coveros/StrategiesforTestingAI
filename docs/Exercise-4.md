# Exercise 4: Diagnose RAG Failures Quickly

## Prerequisites
1. Chatbot and trace view available at http://localhost:5000.
2. Access to precomputed trace samples if live traces are slow.
3. Team of up to 5 people.

## Scenario
Product reports 3 bugs. Your team must quickly decide whether each bug is mostly retrieval, mostly generation, or shared ownership.

## Student tasks
1. Run or review 3 target queries and capture trace evidence.
2. For each case, classify: Context Precision, Groundedness, or Context Recall.
3. Assign an owning team (Data Engineering, Prompt Engineering, or Shared).
4. Write 3 short bug reports with one recommended fix each.

## How to run 3 queries and capture evidence
1. Start the app in one terminal:
	- `python run.py`
2. Open the UI at `http://localhost:5000` and run the 3 target queries in the chat.
3. For each query response in the UI, capture these evidence fields:
	- `response`
	- top 3 `sources[*].metadata.source`
	- top 3 `sources[*].similarity`
	- `retrieval_time`, `generation_time`, `total_time`
4. Record your findings in a small table with columns: Case ID, Query, Evidence, Failure Type, Owner.
5. Optional (if you need a saved JSON artifact): run the API capture command below in a second terminal:
	- `python -c "import requests, json; url='http://localhost:5000/api/chat'; qs=[('case1','What are the key differences between black-box and white-box testing for GenAI?'),('case2','According to production best practices, what is the recommended batch size for GenAI evaluations?'),('case3','Explain hallucination in the context of GenAI testing.')]; out=[]; [out.append({'id':cid,'query':q,'result':requests.post(url,json={'message':q,'mode':'rag'}).json()}) for cid,q in qs]; open('artifacts/precomputed/trace_samples/exercise4_live_run.json','w',encoding='utf-8').write(json.dumps(out,indent=2)); print('saved -> artifacts/precomputed/trace_samples/exercise4_live_run.json')"`
6. If live calls fail (network/rate-limit), use precomputed evidence:
	- `artifacts/precomputed/trace_samples/exercise4_trace_cases_20260416_190513.json`
7. Use the same 3 case IDs (case1, case2, case3) in your bug reports so your evidence is easy to audit.

## Sample target queries
1. What are the key differences between black-box and white-box testing for GenAI?
2. According to production best practices, what is the recommended batch size for GenAI evaluations?
3. Explain hallucination in the context of GenAI testing.

## Bug report template
- Bug title
- Expected behavior
- Actual behavior
- Failure type
- Owning team
- Recommended fix

## Team debrief questions
1. Which case was hardest to classify and why?
2. What trace evidence was most persuasive?
3. Which single fix should be prioritized first?

