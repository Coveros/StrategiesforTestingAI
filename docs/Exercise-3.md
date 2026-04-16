# Exercise 3: Lab - Audit & Extend the Evaluation Framework

**Estimated Duration:** 40-45 minutes  
**Prerequisites:** Completion of Exercise 2; access to GitHub Copilot; Codespace environment  
**Deliverable:** An audit worksheet plus one Copilot-generated metric prototype validated against a targeted regression example  

---

## Scenario

You have inherited an **automated evaluation framework** for the GenAI Testing Assistant. This framework runs a regression suite and uses several pre-built metrics (e.g., keyword matchers, length limits, or basic regex) to grade the bot's answers.

**The Problem:** You suspect some of these automated tests are either **too strict** (failing good answers as false positives) or **too loose** (passing bad answers as false negatives). Your job is to:

1. **Audit** the existing suite to identify one false positive and one false negative
2. **Use GitHub Copilot** to rapidly prototype one new evaluation rule
3. **Integrate and smoke-test** it against a targeted regression example
4. **Share the trade-off** you introduced

---

## Group Setup

- **Individual Work:** You will inspect the provided regression output snapshot or run the quick suite if needed, then use Copilot to generate one new evaluation rule.
- **Table Discussion:** You will compare one false positive, one false negative, and one candidate metric per table.

---

## Key Concepts

### False Positives vs. False Negatives

In AI testing, evaluation metrics can fail in two directions:

| Problem | Definition | Example |
|---------|-----------|---------|
| **False Positive** | Test fails even though bot's answer was correct | Bot says "learning, designing, and executing tests simultaneously." Test expects "simultaneous learning, test design, and execution." Test fails because exact string match. |
| **False Negative** | Test passes even though bot's answer was poor | Bot's response is vague or incomplete but contains a required keyword, so regex checker passes it. |

Your job: Find evidence of both in the inherited framework.

### Three Layers of Evaluation

1. **Deterministic (Cheap & Fast):** Regex checks, length limits, keyword presence/absence, valid JSON.
2. **Semantic (Medium Cost):** Embedding-based similarity, cosine distance thresholds.
3. **LLM-as-Judge (Expensive & Powerful):** Use a model to evaluate another model's output.

The inherited framework likely uses deterministic rules. Copilot will help you add stronger checks without writing boilerplate code.

---

## Part A: Audit the Auditors (15 minutes)

### Step 1: Inspect the Regression Test Suite Output

Use the instructor-provided regression output snapshot first. If you are asked to verify one case live, run the existing test suite:

Precomputed snapshots are available in this repository at:

- `artifacts/precomputed/exercise3/regression_results_*.json`
- `artifacts/precomputed/exercise3/regression_summary_*.txt`
- `artifacts/precomputed/exercise3/evaluation_results.json`
- `artifacts/precomputed/exercise3/evaluation_report.md`

To regenerate these artifacts deterministically in constrained environments, run:

```bash
python prepare_exercise_artifacts.py
```

```bash
python -m regression_testing.regression_testing --quick
```

Or, if using pytest:

```bash
pytest tests/evaluation_framework.py -v
```

**Expected output:**
- A summary table with test results
- Some tests will **PASS** ✅
- Some will **FAIL** ❌
- Look for patterns: which metrics are triggering failures?

### Step 2: Table Review (Swivel and Share)

Turn your laptops to show your table the test report. Together, discuss:

#### Find a False Positive

Look for a **test that failed, but the bot's answer was actually good**. Ask:

- What was the query?
- What did the bot output?
- Which metric caused the failure?
- Is the bot's answer semantically correct, even if phrased differently?

**Example:**
```
❌ FAILED: faithfulness_metric
Query: "What is exploratory testing?"
Expected: "simultaneous learning, test design and execution"
Actual: "learning, designing, and executing tests at the same time"
Metric: Exact string match
Reality: ✅ The bot's answer is correct—just different phrasing!
This is a FALSE POSITIVE.
```

#### Find a False Negative

Look for a **test that passed, but the bot's answer was actually poor or incomplete**. Ask:

- What was the query?
- What did the bot output?
- Which metric allowed it to pass?
- Does the answer lack detail, citations, or contain subtle errors?

**Example:**
```
✅ PASSED: keyword_detector
Query: "What are best practices for testing GenAI systems?"
Actual: "You should use testing. Testing is important for systems."
Metric: Keyword match (looking for "testing" and "systems")
Reality: ❌ The bot's answer is vague and unhelpful—just repeats keywords!
This is a FALSE NEGATIVE.
```

### Step 3: Document Your Findings

Create a simple worksheet and fill it out with your table:

| Finding | Test ID | Query | Bot Output | Metric | Why It's Wrong | Type |
|---------|---------|-------|-----------|--------|----------------|------|
| Example | keyword_check_1 | "What is XYZ?" | "XYZ is when you..." | Simple regex for "is" | Passed even though response is incomplete | False Negative |
| False Positive |  |  |  |  |  |  |
| False Negative |  |  |  |  |  |  |

**Key Question:** "What is the current framework missing that would have caught this bug?"

---

## Part B: Extend the Framework with Copilot (20 minutes)

Now that you've identified weak spots, you'll use GitHub Copilot to add a new evaluation rule to catch the bugs you found.

### Step 1: Open Copilot Chat

In your Codespace, open the Copilot Chat panel (Ctrl+Shift+I or Cmd+Shift+I).

### Step 2: Choose a New Metric to Add

Pick one of the following approaches, or create your own based on the gap you found:

#### Option A: JSON Validator

**Prompt:**
> Write a Python evaluation function that checks if the AI's output contains a valid JSON array of test cases. The function should return True if the response contains valid JSON, False otherwise.

**What it catches:** Responses that claim to provide structured data (like test arrays) but deliver malformed JSON.

**Copilot will likely generate:**
```python
import json
import re

def validate_json_structure(response: str) -> bool:
    """Check if response contains valid JSON."""
    # Extract JSON-like patterns from response
    json_patterns = re.findall(r'\[.*\]|\{.*\}', response, re.DOTALL)
    
    if not json_patterns:
        return False  # No JSON found
    
    for pattern in json_patterns:
        try:
            json.loads(pattern)
            return True  # Valid JSON found
        except json.JSONDecodeError:
            continue
    
    return False  # No valid JSON
```

#### Option B: PII Detector

**Prompt:**
> Write a Python regex evaluator that fails the test if the AI includes any PII like an email address, phone number, or Social Security Number. Return False if PII is found, True otherwise.

**What it catches:** Accidental leaks of personally identifiable information.

**Copilot will likely generate:**
```python
import re

def check_no_pii(response: str) -> bool:
    """Ensure response doesn't contain PII."""
    pii_patterns = {
        'email': r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}',
        'phone': r'\b\d{3}[-.\s]?\d{3}[-.\s]?\d{4}\b',
        'ssn': r'\b\d{3}-\d{2}-\d{4}\b',
    }
    
    for pii_type, pattern in pii_patterns.items():
        if re.search(pattern, response):
            print(f"PII detected: {pii_type}")
            return False
    
    return True
```

#### Option C: Professionalism Grader (LLM-as-Judge)

**Prompt:**
> Write an evaluator using the Cohere API that asks an LLM to grade whether the bot's answer was 'professional' or 'rude'. Return True if professional, False if rude.

**What it catches:** Responses that are technically correct but unprofessional in tone.

**Copilot will likely generate:**
```python
import cohere

def check_professionalism(response: str) -> bool:
    """Use LLM to evaluate if response is professional."""
    client = cohere.Client(api_key="YOUR_COHERE_API_KEY")
    
    prompt = f"""Rate the professionalism of this response on a scale:
Response: {response}

Is this response professional? Answer only with 'professional' or 'rude'."""
    
    result = client.generate(
        model="command-xlarge-nightly",
        prompt=prompt,
        max_tokens=5
    )
    
    output = result.generations[0].text.strip().lower()
    return "professional" in output
```

#### Option D: Citation Checker

**Prompt:**
> Write an evaluator that checks if the response includes at least one citation or source reference. Look for phrases like "according to", "based on", "from the documentation", or explicit source names.

**What it catches:** Responses that make claims without attributing sources.

**Copilot will likely generate:**
```python
import re

def check_citations(response: str, required: bool = True) -> bool:
    """Check if response includes citations."""
    citation_indicators = [
        r'according to',
        r'based on',
        r'from the',
        r'documentation',
        r'guide',
        r'reference',
        r'\[.*\]',  # Bracketed references
    ]
    
    has_citation = any(
        re.search(pattern, response, re.IGNORECASE) 
        for pattern in citation_indicators
    )
    
    return has_citation if required else True
```

For the timed version of this lab, the fastest options are usually **Option B** or **Option D**. Use Option A or C only if your instructor explicitly asks you to.

### Step 3: Copy Copilot's Code

1. In Copilot Chat, copy the generated function
2. Open the [tests/evaluation_framework.py](../tests/evaluation_framework.py) file
3. Paste the function at the end of the file (or in an appropriate section)

### Step 4: Wire It Into Your Test Suite

Add your new metric to one of your test cases. For example, in [tests/evaluation_framework.py](../tests/evaluation_framework.py) or your test runner:

```python
from tests.evaluation_framework import check_citations  # or your function

def test_citations_included():
    """Test: Bot includes proper citations."""
    query = "What are best practices for evaluating GenAI?"
    response = get_bot_response(query)
    
    # Wire in the new metric
    assert check_citations(response), "Response missing citations"
```

### Step 5: Run a Targeted Smoke Test

Run one targeted check to see whether your new metric behaves the way you expect:

```bash
pytest tests/evaluation_framework.py -v
```

Or your custom runner:

```bash
python -m regression_testing.regression_testing --quick
```

**Questions to answer:**
- ✅ Did your new metric address the gap you identified earlier?
- ✅ Did it create any new false positives?
- ✅ Did Copilot's code work on the first try, or did you have to tweak it?

### Step 6: Quick Table Share

Turn your screen to your table and show them:
1. The metric Copilot wrote for you
2. How you integrated it
3. The targeted result (did it catch the gap? any regressions?)
4. Any tweaks you made to Copilot's generated code

**Table Discussion:**
- Did different people get different code from Copilot for the same prompt?
- Which metric is most valuable for catching real bugs?
- Did the generated code need debugging, or did it work as-is?

---

## Part C: Wrap-Up & Deliverables (5-10 minutes)

### Document Your Audit Findings

Create a summary report with the following sections:

**1. Framework Audit Report**

List the cases you inspected and categorize them:

| Metric | Total Tests | Passed | Failed | False Positives? | False Negatives? | Assessment |
|--------|-------------|--------|--------|------------------|------------------|------------|
| Keyword Detector | 5 | 4 | 1 | ? | ? | Weak—catches nothing |
| Regex Check | 3 | 2 | 1 | ? | ? | Too strict? |
| Length Guardrail | 4 | 3 | 1 | ? | ? | Reasonable |

**2. New Metric Integration Report**

Document your new metric:

- **Type:** (JSON Validator / PII Detector / Professionalism / Citation Checker / Other)
- **Copilot Prompt Used:** (your exact prompt)
- **Code Changes:** (list files modified)
- **Targeted Validation:** 
    - Gap addressed: __
    - Example checked: __
    - Did the metric behave as expected? __
    - Any regressions observed? __

**3. Show & Tell Reflection**

Answer these questions:

- Did Copilot's code work on the first try?
- What tweaks (if any) did you make?
- Did your new metric address the gap you identified in Part A?
- Would you keep this metric in production? Why or why not?

### Deliverables Checklist

- [ ] Regression output reviewed and key evidence captured
- [ ] At least one false positive identified and documented
- [ ] At least one false negative identified and documented
- [ ] New evaluation metric prototyped (via Copilot)
- [ ] New metric integrated into one targeted check
- [ ] Targeted validation result documented
- [ ] Code shown to table and feedback collected

### Submission Format

Submit one file named `exercise3_submission.md` containing:

1. **Audit Findings Worksheet** (from Part A)
   - List of false positives with explanations
   - List of false negatives with explanations
   
2. **Metric Validation Notes**
    - What gap the metric is meant to catch
    - One targeted example used to check it

3. **New Metric Code** (the function Copilot generated)

4. **Integration Notes**
   - Where did you add the code?
   - How did you wire it into the test suite?
   
5. **Test Results**
    - Output of the targeted smoke test or validation run
    - Whether the metric helped, hurt, or stayed neutral on the chosen case

6. **Reflection** (3-4 sentences)
   - What did Copilot do well?
   - What had to be fixed?
   - Would you recommend this metric to other teams?

---

## Key Takeaway

**Evaluation metrics are not perfect—they're constantly evolving tools.** You don't need to be a senior automation engineer to add sophisticated new metrics to your test framework. By using **GitHub Copilot to rapidly prototype evaluation functions**, you can:

- ✅ Identify gaps in existing metrics (false positives & false negatives)
- ✅ Extend the framework with semantic checks, structure validators, or LLM-based judgments
- ✅ Iterate quickly without writing boilerplate code from scratch

**The ability to audit and improve your test automation is a superpower in production AI systems—where perfect evaluation is impossible, but constantly improving evaluation is essential.**

---

## Resources

- **Code Reference:** [regression_testing/regression_testing.py](../regression_testing/regression_testing.py)
- **Evaluation Framework:** [tests/evaluation_framework.py](../tests/evaluation_framework.py)
- **Golden Records:** (Your Exercise 2 test cases)
- **Copilot Documentation:** https://github.com/features/copilot
- **Running Chatbot:** [http://localhost:5000](http://localhost:5000)
