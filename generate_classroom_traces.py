#!/usr/bin/env python3
"""
Exercise 6: Classroom Demo - Generate Multi-Agent Traces for Analysis

This script generates 12 example traces that instructors and students can
run together to examine multi-agent trajectories in Phoenix.

Run this script alongside the instructor during the Exercise 6 classroom session,
then open Phoenix at http://localhost:6006 to walk through the results together.

Usage:
    python generate_classroom_traces.py

The script will:
1. Generate 5 traces with the SAME prompt (consistency testing)
2. Generate 4 traces with VARIATIONS of the same question (robustness testing)
3. Generate 3 traces with DIFFERENT questions (diversity/edge cases)

Total: 12 traces to examine and discuss in Phoenix
"""

import requests
import json
import time
import sys
from datetime import datetime
from typing import List, Tuple

# Configuration
FLASK_URL = "http://localhost:5000"
EXERCISE_NUMBER = 6
MODE = "agentic"
CREW_MODE = True

# Define trace scenarios
SAME_PROMPT_SCENARIOS = [
    "What testing approaches work best for large language models?",
]

VARIATION_SCENARIOS = [
    "What testing approaches work best for large language models?",
    "How do I test systems that use large language models?",
    "Compare different strategies for testing AI systems",
    "Why is testing AI-based systems challenging?",
]

DIFFERENT_PROMPT_SCENARIOS = [
    "Define hallucination in the context of LLMs",
    "Explain how retrieval-augmented generation reduces hallucination",
    "What metrics would you use to evaluate LLM reliability?",
]


def run_query(
    prompt: str,
    scenario_name: str,
    run_number: int = 1,
) -> dict:
    """
    Send a query to the Flask app and capture the response.
    
    Returns:
        Dictionary with response, timestamp, and metadata
    """
    try:
        print(f"  → Running: {prompt[:60]}...")
        
        response = requests.post(
            f"{FLASK_URL}/api/agent",
            json={
                "message": prompt,
                "exercise_number": EXERCISE_NUMBER,
                "mode": MODE,
                "crew_mode": CREW_MODE,
            },
            timeout=120,
        )
        
        if response.status_code != 200:
            print(f"    ✗ Failed (HTTP {response.status_code})")
            return None
        
        data = response.json()
        
        # Extract trace info if available
        trace_info = {
            "scenario": scenario_name,
            "prompt": prompt,
            "run_number": run_number,
            "timestamp": datetime.now().isoformat(),
            "status": "success",
            "response_preview": data.get("response", "")[:100],
        }
        
        # Capture agent execution metadata
        if "agent_execution" in data:
            exec_data = data["agent_execution"]
            trace_info["tools_called"] = exec_data.get("tools_called", [])
            trace_info["steps_count"] = exec_data.get("steps", 0)
            trace_info["handoff_count"] = exec_data.get("handoffs", 0)
        
        print(f"    ✓ Success")
        return trace_info
        
    except requests.ConnectionError:
        print(f"    ✗ Connection failed. Is Flask running on {FLASK_URL}?")
        return None
    except Exception as e:
        print(f"    ✗ Error: {e}")
        return None


def generate_traces() -> List[dict]:
    """
    Generate all 12 traces and collect results.
    """
    
    all_traces = []
    
    print("\n" + "=" * 70)
    print("Exercise 6: Multi-Agent Trajectory Analysis - Classroom Demo")
    print("=" * 70)
    
    # Part 1: Same Prompt (5 runs)
    print("\n[PART 1] CONSISTENCY TESTING: Running same prompt 5 times")
    print("-" * 70)
    for run in range(1, 6):
        print(f"\nRun {run}/5:")
        for prompt in SAME_PROMPT_SCENARIOS:
            trace = run_query(prompt, "same_prompt", run)
            if trace:
                all_traces.append(trace)
        time.sleep(1)  # Small delay between runs
    
    # Part 2: Variations (1 run each)
    print("\n[PART 2] ROBUSTNESS TESTING: Running 4 variations of the same question")
    print("-" * 70)
    for idx, prompt in enumerate(VARIATION_SCENARIOS, 1):
        print(f"\nVariation {idx}/4:")
        trace = run_query(prompt, "variation", idx)
        if trace:
            all_traces.append(trace)
        time.sleep(1)
    
    # Part 3: Different Prompts (1 run each)
    print("\n[PART 3] DIVERSITY TESTING: Running 3 completely different prompts")
    print("-" * 70)
    for idx, prompt in enumerate(DIFFERENT_PROMPT_SCENARIOS, 1):
        print(f"\nDifferent prompt {idx}/3:")
        trace = run_query(prompt, "different_prompt", idx)
        if trace:
            all_traces.append(trace)
        time.sleep(1)
    
    return all_traces


def save_results(traces: List[dict]) -> None:
    """
    Save trace results to a JSON file for reference.
    """
    
    output_file = "classroom_traces_results.json"
    results = {
        "generated_at": datetime.now().isoformat(),
        "total_traces": len(traces),
        "exercise": EXERCISE_NUMBER,
        "mode": MODE,
        "crew_mode": CREW_MODE,
        "traces": traces,
    }
    
    with open(output_file, "w") as f:
        json.dump(results, f, indent=2)
    
    print(f"\n✓ Results saved to {output_file}")


def print_summary(traces: List[dict]) -> None:
    """
    Print a summary of generated traces.
    """
    
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"Total traces generated: {len(traces)}")
    
    # Group by scenario
    scenarios = {}
    for trace in traces:
        scenario = trace.get("scenario")
        if scenario not in scenarios:
            scenarios[scenario] = []
        scenarios[scenario].append(trace)
    
    for scenario, trace_list in scenarios.items():
        print(f"\n{scenario.upper()}: {len(trace_list)} traces")
        for trace in trace_list:
            status = "✓" if trace.get("status") == "success" else "✗"
            prompt_preview = trace.get("prompt", "")[:50]
            print(f"  {status} {prompt_preview}...")
    
    print("\n" + "=" * 70)
    print("NEXT STEPS")
    print("=" * 70)
    print(f"1. Open Phoenix in your browser: http://localhost:6006")
    print(f"2. Click the 'Traces' tab")
    print(f"3. Review the {len(traces)} traces just generated")
    print(f"4. Compare traces across scenarios (consistency, robustness, edge cases)")
    print(f"5. Discuss with your instructor and teammates")
    print("\nKey Questions to Answer:")
    print("  • Which runs (same prompt) had different trajectories? Why?")
    print("  • How did agent behavior change across variations?")
    print("  • What edge cases or failures did we observe?")
    print("=" * 70 + "\n")


def main():
    """
    Main entry point.
    """
    
    print("\nStarting classroom trace generation...")
    print(f"Flask endpoint: {FLASK_URL}")
    print(f"Exercise: {EXERCISE_NUMBER}")
    print(f"Mode: {MODE} (crew={CREW_MODE})")
    
    # Check Flask is running
    try:
        response = requests.get(f"{FLASK_URL}/api/health", timeout=5)
        if response.status_code == 200:
            print("✓ Flask is running\n")
        else:
            print("✗ Flask returned unexpected status code\n")
            sys.exit(1)
    except requests.ConnectionError:
        print(f"✗ Cannot connect to Flask at {FLASK_URL}")
        print("   Start Flask with: python run.py")
        sys.exit(1)
    
    # Generate traces
    traces = generate_traces()
    
    # Save and summarize
    if traces:
        save_results(traces)
        print_summary(traces)
    else:
        print("\n✗ No traces were generated. Check Flask logs for errors.")
        sys.exit(1)


if __name__ == "__main__":
    main()
