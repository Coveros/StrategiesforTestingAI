# Exercise 2 Instructor Notes: Extend the UI Golden Suite

Facilitator reference: [Instructor Facilitation Rubric](Exercise-Instructor-Facilitation-Rubric.md)

## Purpose

Exercise 2 is now a black-box browser-testing exercise. The student-facing
suite is `tests/e2e/test_exercise2_ui.py`, not the legacy
`regression_testing/regression_testing.py` module.

Students run seven starter tests from the VS Code Testing beaker, inspect the
responses and MLflow traces, then use Copilot to add tests based on Exercise 1
exploratory findings.

## Preparation

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   python -m playwright install chromium
   ```
2. Start MLflow on port 5001.
3. Start the Flask app with `python run.py`.
4. Confirm the suite is discoverable:
   ```bash
   python -m pytest tests/e2e/test_exercise2_ui.py --collect-only -q
   ```
   Expected result: seven collected tests.
5. Confirm students can find the run artifact under:
   `artifacts/exercise2/ui_golden_run_*.json`.

## What to watch for

- Students should test stable behavior, not exact generated prose.
- A source count alone does not prove grounding; ask students to inspect source
  content and the corresponding `rag.retrieve` span.
- A latency assertion should be treated as an environment-dependent signal,
  not a quality judgment by itself.
- The oversized-input test should be understood as an application contract
  test: the expected result is a bounded HTTP 400 response.
- The empty-input test should not create a request or a chat message.

### Prompt-Specific Teaching Issue to Highlight
If students miss the defect, direct them to the exact behavior the prompts are designed to surface:
- Empty-input and oversized-input prompts should reveal contract boundaries, not model quality.
- The happy-path or grounded query should produce a useful answer plus source evidence, not just fluent text.
- Repeatability checks should show that a paraphrased question can still preserve valid response contracts, while a brittle exact-text assertion would fail for the wrong reason.
- The teaching issue is not a single "bad answer" but the difference between a stable product contract and a fragile test that depends on exact prose.

## Copilot coaching prompt

Recommend a prompt such as:

> Add a Playwright pytest test for a boundary or adversarial case from Exercise
> 1. Use the existing Ask UI, record the API response through the shared
> evidence helper, assert stable response/source behavior, and avoid exact
> generated-text matching.

Before students run generated code, ask them to identify:

1. What user-visible behavior is being tested?
2. Which assertion is stable across model wording variation?
3. Which MLflow trace should confirm the result?
4. What would make this test a false positive or false negative?

## Artifact and trace review

Each suite run records prompt, response, sources, timings, session ID, and
exercise number. Use the session and exercise values to locate the matching
MLflow trace. For Ask mode, the expected structure is:

```text
rag.query -> rag.retrieve -> rag.generate
```

The RAG spans should expose inputs and outputs. When Ollama returns usage
metadata, the generation response also includes prompt, completion, and total
token counts.

## Expected debrief

A strong student conclusion distinguishes:

- UI contract failure
- API payload failure
- retrieval or grounding failure
- generation-quality variation
- trace/evidence gap

The legacy regression framework may be mentioned as instructor/CI background,
but it is not required for the student activity.
