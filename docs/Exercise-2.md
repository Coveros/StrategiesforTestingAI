# Exercise 2: Building and Auditing a Golden Test Set with Copilot

Audience: Students
Estimated Duration: 35-45 minutes
Type: Copilot-assisted test design + group rubric audit
Prerequisites: Exercise 1 completed; chatbot running at http://localhost:5000; GitHub Copilot Chat available in each student's Codespace
Deliverable: Copilot-generated test tables + selected group cases + inter-rater reliability audit + rewritten deterministic rubrics

## Why this exercise
Copilot can help a QA team generate test cases quickly, but speed is not the same as quality. A regression suite only becomes trustworthy when the prompts stress the system properly and the grading rules are deterministic enough that multiple reviewers apply them the same way. This exercise focuses on both parts: generating candidate test cases fast and then auditing whether the rubrics are actually ready for automation.

## What you receive before starting
1. A running GenAI Testing Assistant at http://localhost:5000.
2. A reminder of the product boundary: the assistant should provide software testing advice and refuse requests to write malicious hacking scripts.
3. A compact table assignment model for distributed test generation.
4. Access to GitHub Copilot Chat in each student's Codespace.
5. The worksheet templates included below.

## Learning goals
1. Use Copilot to scale up test generation across a QA team.
2. Distinguish strong testing prompts from weak or vague ones.
3. Identify when Copilot-generated evaluation criteria are too subjective for automation.
4. Practice improving rubric quality through inter-rater reliability checks.

## Scenario
You are the QA Lead evaluating the new GenAI Testing Assistant. The assistant must provide accurate software testing advice and strictly refuse requests to write malicious hacking scripts. To build your regression suite faster, your table will distribute the workload, with everyone using GitHub Copilot to generate specific types of test cases.

## Group setup
Use a three-category core model for the timed lab.

Core Category 1: Factual
1. Generate 2 Factual queries testing the bot's knowledge of software testing definitions.

Core Category 2: Reasoning
1. Generate 2 Reasoning queries where the bot must apply logic, such as generating edge cases or comparing test strategies.

Core Category 3: Boundary Risk
1. Generate 2 queries from one of these categories: Adversarial, Noise, or Out-of-Scope.

If your table has 4 to 5 people, extra people should help audit rubrics and improve determinism instead of generating a full extra category.

## Part A: Distributed Generation
Everyone works independently in their own Codespace for this part.

Open GitHub Copilot Chat and prompt Copilot to generate your assigned category.

Use this Copilot prompting tip:
1. Tell Copilot: "Format the output as a table with three columns: Category, User Prompt, and Evaluation Criteria. Do not write the exact expected answer. Write the strict rubric for how to grade the answer."

Why this matters:
1. Exact expected answers are often too brittle for GenAI systems.
2. Evaluation criteria are more useful when they tell reviewers what must be present, absent, refused, or redirected.
3. If the rubric is vague, the test will not be reliable enough to automate later.

### Category guidance
Use category-specific expectations while reviewing what Copilot gives you.

Factual:
1. The prompt should test definitions or core software testing concepts.
2. The rubric should require the answer to define terms accurately, not just sound fluent.

Reasoning:
1. The prompt should force the assistant to apply testing logic rather than repeat a definition.
2. The rubric should require concrete outputs such as edge cases, tradeoffs, or comparisons.

Adversarial:
1. The prompt should probe the assistant's safety boundary.
2. The rubric should require refusal or safe redirection and should make clear that malicious hacking-script help must not be provided.

Noise:
1. The prompt should include heavy typos, slang, or formatting issues.
2. The rubric should focus on whether the assistant still recovers the intended testing request or asks for clarification appropriately.

Out-of-Scope:
1. The prompt should be outside the product purpose without being outright malicious.
2. The rubric should require the assistant to redirect, narrow scope, or politely refuse instead of pretending to be a general-purpose assistant.

## Part B: The Round Robin Audit
Take 2 minutes to review what Copilot generated for you before talking as a table.

Ask yourself:
1. Did Copilot actually generate prompts that stress-test the model?
2. Are the evaluation criteria specific enough that two people would grade the same answer the same way?
3. Did Copilot accidentally produce a prompt or rubric that is too broad, too easy, or too subjective?

Your task:
1. Each active category owner must select the one best or trickiest test case from their list to present to the table.
2. Be ready to explain why you chose it.

Use this quick audit worksheet:

| Category | Chosen prompt | Why this is the best or trickiest case | What is weak or risky about the current rubric? |
|---|---|---|---|
| Example: Reasoning | Generate boundary-value tests for a password reset flow with rate limits. | It forces the bot to apply testing logic instead of defining a term. | "Must provide good edge cases" is too subjective. |

## Part C: Group Exercise - Inter-Rater Reliability
Now review only 2 selected cases as a table.

For each selected case:
1. The person whose turn it is reads their chosen prompt and Copilot-generated evaluation rubric out loud.
2. Use either a live chatbot response or an instructor-provided sample response.
3. Without talking, everyone else writes down a `Pass` or `Fail` grade based strictly on the rubric that was read.
4. Reveal the grades at the same time.
5. If everyone did not give the same grade, the rubric is too subjective.
6. Rewrite the rubric so it becomes more deterministic.

Important:
1. `Pass` or `Fail` must be based strictly on the rubric, not on your personal impression of whether the answer felt good.
2. One person at the table should capture the pass/fail votes and the final rewritten rubric for each case.
3. If a room full of QA testers cannot agree on the grade, you cannot automate that test reliably.

## Rewriting a vague rubric
Use this pattern when improving a weak Copilot-generated rubric.

Weak rubric example:
1. Must provide good edge cases.

Stronger deterministic rewrite:
1. Must list at least 3 distinct boundary values.
2. Must include one invalid input case.
3. Must mention expected system behavior for at least one failure mode.

## Submission format
Submit one file named `exercise2_submission.md` (or PDF) containing:
1. The Copilot-generated table for each active category used by your table.
2. The selected test case for each active category.
3. The group's initial pass/fail votes for the 2 reviewed cases.
4. The rewritten deterministic rubric for each case where disagreement happened.
5. A short reflection paragraph: What did this exercise teach you about using Copilot to generate regression tests and rubrics?

## Copilot support guidance
Copilot is useful here for scale and drafting, not for final judgment.

Good Copilot uses:
1. Generate category-specific prompts quickly.
2. Suggest initial evaluation criteria you can tighten.
3. Produce multiple prompt variants so you can choose the one that best stress-tests the assistant.

Avoid:
1. Accepting Copilot's first rubric without checking whether it is deterministic.
2. Letting Copilot write vague criteria such as `good`, `clear`, or `helpful` without measurable interpretation.
3. Assuming a test is automation-ready just because Copilot formatted it nicely.

## Key takeaway
Copilot is an incredible tool for scaling test generation, but humans must establish inter-rater reliability. If a room full of QA testers cannot agree on whether a test passed or failed based on the rubric, you cannot automate that test.

## Debrief questions
1. Which category produced the vaguest Copilot-generated rubrics?
2. Which case created the most disagreement during pass/fail voting?
3. What changed when you rewrote the rubric to be more deterministic?
4. Which category is safest to automate first?
5. What does this exercise show about the relationship between Copilot speed and QA rigor?
