# Exercise 1 Instructor Notes

Audience: Instructor only
Estimated Duration: 15 minutes prep + 30-40 minutes in class + 15 minutes debrief

## Distribution plan
Share with students:
1. docs/Exercise-1.md

Keep private:
1. This file (facilitation notes and expected findings)

## Facilitation goals
1. Establish the shift from exact-match testing to quality-oriented evaluation.
2. Build comfort with ambiguity while keeping rigor.
3. Prepare students for later sections on regression, metrics, and layered oracles.

## Setup checklist
1. Confirm the Flask app is running before class.
2. Verify each student can hit http://localhost:5000.
3. Confirm API key and dependencies are set in the class environment.
4. Have one backup machine/session ready for live demo.

## Optional temperature variability mini-demo
Use this before the main exercise to show why exact string matching is fragile for LLM output.

Run from project root:
1. python temperature_demo.py --prompt "Suggest a 3-day itinerary for Tokyo." --repeats 5 --high-temp 1.0 --low-temp 0.0

Notes:
1. The script uses the same chatbot pipeline and retrieval flow as the app.
2. If you are on a trial key, keep the default delay to reduce rate-limit errors.
3. Ask students to identify core facts that stay stable versus wording/style that varies.

## Optional browser-based instructor control
If you prefer a UI demo instead of terminal script:
1. Open the chatbot using http://localhost:5000/?instructor=1
2. In the header, enable Instructor Temp.
3. Set temp to 1.0 and send the same prompt 3 to 5 times.
4. Set temp to 0.0 and repeat with the same prompt.
5. Compare stable content versus creative variation with students.

Important:
1. Without the ?instructor=1 query parameter, students do not see these controls.
2. The app default behavior is unchanged when Instructor Temp is disabled.

## Timing
1. 5 minutes: Frame exercise and expected output.
2. 20-25 minutes: Student exploratory testing.
3. 10 minutes: Pair/group synthesis of findings.
4. 10-15 minutes: Full-group debrief.

## Expected findings
Common patterns students should notice:
1. Good relevance on in-domain prompts.
2. Variable structure/style across repeated prompts.
3. Inconsistent handling of off-topic and adversarial requests.
4. Possible mismatch between response confidence and source grounding.
5. Latency variation under repeated use.

## Rubric (0-2 per dimension)
Score each team on a 0-2 scale per dimension.
1. Observation quality
2. Evidence quality
3. Risk classification quality
4. Heuristic quality

Interpretation:
1. 7-8: Strong analytic testing mindset.
2. 5-6: Solid start, needs sharper heuristics.
3. 0-4: Focus coaching on evidence and testability.

## Debrief (5 minutes)
Ask teams:
1. Which heuristic had the best signal-to-noise ratio?
2. Which prompt category exposed the highest risk?
3. What one check should become an automated regression test first?

Map to next-step controls:
1. Variability risk -> semantic assertions instead of exact-match checks.
2. Safety risk -> hard refusal checks and escalation logic.
3. Relevance risk -> retriever/generator split diagnostics.

## Bridge to Next Section
Bridge language:
1. We observed variability and oracle ambiguity.
2. Next we convert qualitative observations into repeatable checks.
3. Later we layer weak oracles, strong oracles, and human review.

## Optional extension
If groups finish early:
1. Ask each group to convert one heuristic into a pseudo automated test.
2. Ask each group to propose one false positive risk for their heuristic.
