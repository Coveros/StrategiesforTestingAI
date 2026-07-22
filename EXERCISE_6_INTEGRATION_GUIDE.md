# Exercise 6: Classroom Demo Integration Guide

## Summary

I've created a solution for your goal: **Have students run batch traces together with you, then walk through them in Phoenix, then do individual exercises.**

## What's New

### 1. **`generate_classroom_traces.py`** ✅
A new Python script that generates 12 traces in 3 categories:
- **5 same-prompt traces** (consistency testing)
- **4 variation traces** (robustness testing)  
- **3 different-prompt traces** (diversity/edge cases)

**Students can run this with you in class:**
```bash
python generate_classroom_traces.py
```

**Output:** 
- 12 traces sent to Ollama (takes ~5-7 minutes)
- Results saved to `classroom_traces_results.json`
- Phoenix auto-receives all traces

### 2. **Updated Exercise 6 (Student-Facing)**
Restructured with two parts:

**Part 1 (30 min): Classroom Demo**
- Instructor runs the script while students watch
- Class explores the 12 traces together in Phoenix
- Guided activities: Consistency → Robustness → Diversity
- Discussion questions to frame multi-agent behavior

**Part 2 (45-55 min): Individual Exercise**
- Existing handoff corruption diagnostic task
- Students apply what they learned from Part 1 traces
- Students diagnose their own handoff corruption scenario

### 3. **Updated Instructor Notes**
Detailed facilitation guide including:
- Timeline (30 min for demo, 45-55 min for exercise)
- What to point out in traces
- Tips for smooth classroom delivery
- Discussion questions

---

## How It Aligns with Your Goal

✅ **"Students run prompts along with me"**
- Script is runnable in class, everyone watches progress together
- 12 traces generated live in front of class

✅ **"See all the results and walk through them"**
- Results automatically appear in Phoenix
- Instructor can filter by scenario ("same_prompt", "variation", "different_prompt")
- Students examine prompts, tool calls, hallucinations together

✅ **"Students then do an exercise"**
- Part 2 is an individual handoff corruption diagnostic
- Students apply analysis techniques from Part 1 demo
- They create their own trace for analysis

---

## For Your Next Class

### Pre-Class Setup
1. Test the script once: `python generate_classroom_traces.py`
2. Ensure Flask, Phoenix, and Ollama are all running
3. Have Exercise 6 document open

### During Class (90 minutes total)
1. **Part 1 Demo (30 min)**:
   - Run the script in front of class (5-7 min)
   - Open Phoenix and walk through traces (20 min)
   - Discuss observations (5 min)

2. **Part 2 Exercise (45-55 min)**:
   - Students work individually
   - They run handoff corruption scenario
   - Compare baseline vs corrupted traces
   - Propose fixes in team debrief

---

## File Locations
- Script: `generate_classroom_traces.py` (root directory)
- Student Exercise: `docs/exercises/Exercise-6.md`
- Instructor Notes: `docs/exercises/Exercise-6-Instructor-Notes.md`
- Results: `classroom_traces_results.json` (generated after each run)

---

## Next Action

When you run the script before class, you'll see exactly what students will see. The script prints:
```
[PART 1] CONSISTENCY TESTING: Running same prompt 5 times
Run 1/5:
  → Running: What testing approaches...
  ✓ Success
...
[PART 2] ROBUSTNESS TESTING: Running 4 variations
...
[PART 3] DIVERSITY TESTING: Running 3 completely different prompts
...
SUMMARY: Total traces generated: 12
```

Then in Phoenix, you'll have 12 traces to walk through with students.
