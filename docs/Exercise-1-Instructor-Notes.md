# Exercise 1 Instructor Notes

Audience: Instructor only
Estimated Duration: 15 minutes prep + 35-45 minutes in class + 10 minutes debrief

## Distribution plan
Share with students:
1. docs/Exercise-1.md

Keep private:
1. This file (facilitation notes and expected findings)

## Facilitation goals
1. Make students feel the difference between testing a deterministic system and testing a probabilistic GenAI system.
2. Push students to produce QA evidence, not just opinions about whether the bot felt good or bad.
3. Show why exact-match assertions create false failures for acceptable GenAI answers.
4. Prepare students for later sections on heuristics, regression strategy, and layered oracles.

## Setup checklist
1. Confirm the Flask app is running before class.
2. Verify each student can hit http://localhost:5000.
3. Confirm API key and dependencies are set in the class environment.
4. Have one backup machine or browser session ready for live demo.
5. Remind students that the bot is a GenAI testing assistant, so negative prompts should challenge scope boundaries rather than only chase random adversarial behavior.

## Optional temperature variability mini-demo
Use this before the main exercise to set up the determinism test and show why exact string matching is fragile for LLM output.

Run from project root:
1. python temperature_demo.py --prompt "Create a practical test plan for evaluating hallucination risk in a travel assistant." --repeats 5 --high-temp 1.0 --low-temp 0.0

Notes:
1. The script uses the same chatbot pipeline and retrieval flow as the app.
2. If you are on a trial key, keep the default delay to reduce rate-limit errors.
3. Ask students to separate stable content from wording variation.
4. Make the point explicitly: if the substance is acceptable but the string is different, `Assert.AreEqual(...)` is the wrong oracle.

## Optional browser-based instructor control
If you prefer a UI demo instead of the terminal script:
1. Open the chatbot using http://localhost:5000/?instructor=1.
2. In the header, enable Instructor Temp.
3. Set temp to 1.0 and send the same prompt 3 to 5 times.
4. Set temp to 0.0 and repeat with the same prompt.
5. Compare stable content versus wording variation with students.

Important:
1. Without the ?instructor=1 query parameter, students do not see these controls.
2. The app default behavior is unchanged when Instructor Temp is disabled.

## Timing
1. 5 minutes: Frame the QA scenario and explain the reduced scope.
2. 15-18 minutes: Students execute the three charters with 2 prompts each and record evidence.
3. 6-8 minutes: Students run the determinism test in two separate chats.
4. 5-7 minutes: Students identify exact-match assertion failures and draft heuristics.
5. 5 minutes: Pair or small-group synthesis.
6. 5-7 minutes: Full-group debrief.

## Time-box guidance
1. If time slips, keep the Negative charter to 1 prompt instead of 2.
2. Do not add a third determinism run during class; save that for optional extension.
3. Treat heuristic polish as homework if students are still capturing evidence.

## What good student work looks like

### Strong Happy Path prompts
Students ask realistic QA questions that the assistant should handle well.

Examples:
1. Asking for a hallucination test checklist.
2. Asking for RAG evaluation metrics.
3. Asking for exploratory test ideas for a GenAI feature.

Look for:
1. Concrete QA intent.
2. Evidence that the answer was useful, not just fluent.
3. Notes about what would count as acceptable variation.

### Strong Boundary prompts
Students keep the prompt relevant but make the input messy, long, or structurally difficult.

Look for:
1. Massive pasted text or mixed constraints.
2. Weird formatting that still contains a valid testing request.
3. Observations about whether the assistant preserved the important parts.

### Strong Negative prompts
Students test scope boundaries, not just random nonsense.

Look for:
1. Clearly out-of-domain requests.
2. Attempts to redirect the assistant away from testing support.
3. Evaluation of whether the response appropriately refused, redirected, or constrained itself.

## Expected findings
Common patterns students should notice:
1. Happy Path responses are often useful but not identical across runs.
2. Boundary prompts may expose dropped constraints, partial answers, or weaker structure.
3. Negative prompts may reveal inconsistent refusal or redirection behavior.
4. The same complex prompt can produce different ordering, examples, or phrasing while remaining semantically acceptable.
5. Exact-match assertions would fail on many acceptable answers, especially list-based or paragraph-based responses.
6. Students often discover that a strong QA observation sounds more like an oracle discussion than a binary bug report.

## Coaching notes
If students get stuck, push them with these prompts:
1. What exact traditional assumption were you relying on here: stable output, fixed ordering, one correct phrasing, or binary pass/fail?
2. If the answer changed, did usefulness or correctness change too?
3. Could you explain this as a risk without demanding a single exact response?
4. What deterministic signal could you check without pretending the whole response should be identical?

If students label everything a defect, coach them toward exploratory QA language:
1. `Acceptable` for useful in-scope variation.
2. `Needs Follow-up` for inconclusive or incomplete behavior.
3. `Risky Behavior` for behavior that could mislead users or break trust.
4. `Out-of-Scope Response` for failures to respect the assistant's intended boundary.

## Using the assertion-problem evidence
Require teams to preserve at least one exact output excerpt and use it during debrief.

Listen for examples such as:
1. The assistant gives the same ideas in a different order.
2. The assistant uses synonyms or different bullet wording.
3. The assistant returns 4 bullets on one run and 5 on another while still covering the same core concepts.

The key teaching point:
1. Exact string equality is often a bad oracle for probabilistic systems.
2. Students should be able to explain why the output is still acceptable even when the literal string changes.

## Heuristic examples to steer students toward
Good deterministic heuristic directions:
1. Required-term presence for prompts about RAG, hallucination testing, or groundedness.
2. Minimum and maximum word-count thresholds.
3. Regex checks for expected sections such as `Metrics`, `Risks`, or `Test Cases`.
4. JSON schema validation for structured-output prompts.

Coach students to include one risk in each heuristic:
1. False positive risk: a good answer may use synonyms and still fail a keyword rule.
2. False negative risk: a long answer may pass length checks but still be poor quality.

## Rubric (0-2 per dimension)
Score each team on a 0-2 scale per dimension.
1. Charter design quality
2. Evidence quality
3. Determinism analysis quality
4. Assertion-problem analysis quality
5. Heuristic quality

Interpretation:
1. 9-10: Strong QA reasoning with clear oracle thinking.
2. 6-8: Solid start, but needs sharper evidence or better heuristics.
3. 0-5: Focus coaching on separating observation, risk, and automation strategy.

## Debrief
Ask teams:
1. Which charter most clearly exposed the gap between traditional black-box testing and GenAI testing?
2. Which output changes were acceptable, and which introduced real risk?
3. Which exact-match failure example best illustrates a bad oracle?
4. Which deterministic heuristic would you automate first, and why?
5. What still requires human review even after you add heuristics?

Map to next-step controls:
1. Variation with acceptable meaning -> semantic or partial assertions instead of exact-match checks.
2. Scope-boundary failures -> refusal checks and boundary policies.
3. Missing constraints in long or messy prompts -> prompt robustness testing and stronger evaluation datasets.
4. Useful but non-identical answers -> layered oracles, heuristics, and human review.

## Bridge to Next Section
Bridge language:
1. In this exercise, students saw that a GenAI system can be acceptable without being identical run to run.
2. That means traditional black-box assertions are often too brittle on their own.
3. Next, we turn these observations into repeatable heuristics and stronger evaluation approaches.
4. Later, we layer weak oracles, strong oracles, semantic checks, and human review.

## Optional extension
If groups finish early:
1. Ask each group to convert one heuristic into a pseudo automated test.
2. Ask each group to identify one false positive and one false negative for that heuristic.
3. Ask each group to rewrite one exact-match assertion as a safer partial or semantic check.
