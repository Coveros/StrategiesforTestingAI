# Exercise 2: Extend a Golden UI Test Suite

## Prerequisites
1. Exercise 1 completed.
2. Review of Golden UI Test Suite
3. Demonstration of GitHub Copilot features

## Scenario

You are a black-box tester extending a small golden test suite for the Ask/RAG
experience. The starter suite uses Playwright through pytest, so you can run it
from the VS Code **Testing** beaker without editing the application or its RAG
implementation.

The suite deliberately validates stable behavior rather than exact generated
prose. A good generative-AI UI test checks the response contract, grounding
evidence, useful topic coverage, and bounded failure behavior. Note that since codespaces does not support virtual screens well, we are running these tests in a headless mode so you will not see tests executing in the browser UI.

## Run the seven starter tests

1. In VS Code, open the **Testing** beaker and run the existing UI test suite
2. Use GitHub Copilot to add a new test to `tests/e2e/test_exercise2_ui.py`
3. Rerun the test suite to ensure the new test is included and passes.
4. It the test fails, ask GitHub Copilot to fit it

You can also run the suite from the terminal in VS Code using this command:

python -m pytest tests/e2e/test_exercise2_ui.py -v

The starter cases cover:

| Test | What it validates |
|---|---|
| Chat controls | The Ask UI is available and starts in the expected mode |
| Happy path | A known RAG question returns an answer and sources |
| Topic coverage | A hallucination question produces relevant concepts |
| Evidence contract | Sources, similarity metadata, and timing fields are present |
| Empty input | The UI does not submit a blank request |
| Boundary input | Oversized input returns a bounded, understandable error |
| Repeatability | Rephrased questions preserve a valid grounded response shape |

## How the assertions work

Do not assert that the model returns one exact paragraph. Instead, the tests
check evidence that should remain stable across reasonable model variation:

- HTTP success or a documented validation error
- non-empty response text
- Ask/RAG mode
- source content and source metadata for grounded questions
- numeric retrieval, generation, and total timing fields
- expected topic concepts for a focused question
- bounded response length and no unhandled server-error text

The browser performs the interaction through the UI. The matching `/api/chat`
response is also inspected so the test can validate structured evidence that is
not visible in the chat bubble.

## Extend the suite with Copilot

Choose two exploratory tests from Exercise 1 and ask Copilot to add them to
`tests/e2e/test_exercise2_ui.py`. For example:

> Add a Playwright pytest test for a boundary question about long GenAI test
> prompts. Use the existing Ask UI, assert a valid response contract, require
> grounding sources when the question is in scope, and avoid exact response
> text matching.

After Copilot adds a test:

1. Read the assertions and confirm they test observable behavior.
2. Run the new test from the Testing beaker.
3. Record the prompt, result, evidence fields, and whether the failure is a product defect, test defect, or expected model variation.

## Results table

| Case | Prompt or behavior | Pass/fail | Response evidence | Interpretation |
|---|---|---|---|---|
| Starter 1 |  |  |  |  |
| Starter 2 |  |  |  |  |
| Starter 3 |  |  |  |  |
| Added test 1 |  |  |  |  |
| Added test 2 |  |  |  |  |

## Team debrief

1. Which assertion was most stable across model wording changes?
2. Which assertion gave the strongest evidence that the answer was grounded?
3. Which exploratory test should become part of the golden suite next?
4. What should be validated in the UI?
