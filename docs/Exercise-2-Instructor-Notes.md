# Exercise 2 Instructor Notes

Audience: Instructor only
Estimated Duration: 15 minutes prep + 45-55 minutes in class + 15 minutes debrief

## Distribution plan
Share with students:
1. docs/Exercise-2.md

Keep private:
1. This file

---

## Facilitation goals
1. Students leave able to distinguish a well-formed golden record from a vague one.
2. Students see the direct connection between lecture anatomy and the same chatbot they explored in Exercise 1.
3. Students develop a healthy skepticism: a passing regression test only means as much as its gold standard is worth.
4. Students build familiarity with the regression_testing module they will run in later exercises.

---

## Setup checklist
1. Confirm the Flask app is still running from Exercise 1 so students can verify their gold standards against the live chatbot.
2. Confirm students can read regression_testing/regression_testing.py and data/documents/ in the repo.
3. Have the anatomy slide visible during Part A for reference.
4. Remind students the four knowledge base files are data/documents/genai_testing_guide.md, faq_genai_testing.md, production_best_practices.md, and evaluation_metrics.md.

---

## Timing
1. 2 minutes: Frame both parts. Part A uses the same chatbot - students should verify their gold standards live before committing to them.
2. 20-25 minutes: Part A individual/pair work.
3. 5 minutes: Brief share-out of one record per team before moving to Part B.
4. 15-20 minutes: Part B code review.
5. 10-15 minutes: Full-group debrief.

---

## Known weaknesses in the existing golden records (Part B answers)
Use these to guide debrief if students miss them.

### hallucination_basic
- Input quality: Good. Specific and realistic.
- Gold standard: Good. Mentions key concepts correctly.
- Keywords: 'AI' and 'generative' are very generic. A hallucinated response could contain both and still be wrong.
- Improvement: Replace 'AI' with 'training data' or 'context window' to be more discriminating.

### rag_evaluation
- Input quality: Good.
- Keywords: 'BLEU' and 'ROUGE' are specific, which is good. But 'human evaluation' is so common it adds little discriminating value.
- Length range: (150, 500) is wide. A 150-character response would be nearly a stub.
- Improvement: Tighten the minimum to 250 to rule out incomplete responses.

### edge_case_empty
- Gold standard: 'ERROR: Empty query provided' is the system-level message, not a user-facing message. The chatbot actually returns a 400 HTTP error, not this string. The record would pass or fail depending on whether you are testing the API or the pipeline directly.
- Improvement: Clarify whether this tests the API layer (HTTP 400) or the pipeline layer (ValueError). They need separate records.

### edge_case_irrelevant (pizza)
- Pass criteria are evaluating refusal behavior.
- Gold standard is very specific about what the refusal should say. In practice the model might refuse correctly but use different words.
- Keyword 'cannot answer' is a substring match - a response containing "I cannot answer every question" would pass even if it then hallucinates a pizza recommendation.
- Improvement: Add a negative keyword check (assert response does NOT contain a pizza recommendation).

### Overall gap in the existing set
- No adversarial records (prompt injection, jailbreak attempts).
- No records testing response formatting or length appropriateness for complex questions.
- All records are English only.

---

## Rubric (0-2 per dimension)
Score each team 0-2 per dimension.

Part A:
1. Record completeness (all fields present)
2. Gold standard specificity (would a hallucinated but fluent response pass?)
3. Keyword discrimination (do keywords actually distinguish good from bad?)
4. Edge/adversarial design (what is the correct expected behavior, and is it stated?)

Part B:
1. Critique quality (did they find real issues, not just formatting nits?)
2. Improvement proposals (are they actionable?)
3. Gap record quality (does it fill a genuine hole?)

Interpretation:
1. 12-14: Strong analytical mindset. Ready for regression tooling exercises.
2. 8-11: Solid foundation. Needs sharper keyword and threshold thinking.
3. 0-7: Focus coaching on what makes a gold standard fail silently.

---

## Debrief (5 minutes)
Ask teams:
1. Which golden-record field most often weakened test quality?
2. Which existing record was most likely to create a false signal?
3. What one rubric criterion should be mandatory in every future record?

Map to controls:
1. Weak keywords -> specificity and negative checks.
2. Weak expectations -> clearer pass/fail criteria.
3. Weak edge handling -> explicit API-vs-pipeline behavior assertions.

## Bridge to Next Section
Bridge language:
1. We now know how to design golden records that are worth trusting.
2. Next we look at how to run them automatically and interpret results at scale.
3. The repo's regression testing framework will execute the very records we just critiqued.

