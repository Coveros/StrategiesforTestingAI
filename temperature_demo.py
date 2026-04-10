#!/usr/bin/env python3
"""
Instructor demo script for temperature variability in the chatbot pipeline.

Runs the same prompt multiple times at high and low temperature so students
can compare stable core facts versus stylistic variability.
"""

import argparse
import os
import time
from dotenv import load_dotenv

from app.rag_pipeline import RAGPipeline


def run_demo(prompt: str, repeats: int, high_temp: float, low_temp: float, delay_seconds: float) -> None:
    load_dotenv()

    if not os.getenv("COHERE_API_KEY"):
        raise RuntimeError("COHERE_API_KEY is not set. Add it to .env before running this demo.")

    pipeline = RAGPipeline()

    print("\nTEMPERATURE DEMO")
    print("=" * 70)
    print(f"Prompt: {prompt}")
    print(f"Repeats per setting: {repeats}")
    print(f"High temperature: {high_temp}")
    print(f"Low temperature: {low_temp}")
    print(f"Inter-call delay (seconds): {delay_seconds}")
    print("=" * 70)

    for temp_label, temp_value in (("HIGH", high_temp), ("LOW", low_temp)):
        print(f"\n{temp_label} TEMPERATURE RUNS (temp={temp_value})")
        print("-" * 70)

        for i in range(1, repeats + 1):
            result = pipeline.query(prompt, temperature=temp_value)
            print(f"\nRun {i}/{repeats}")
            print(f"Total time: {result.get('total_time', 0):.2f}s")
            print(result.get("response", "<no response>"))

            if i < repeats and delay_seconds > 0:
                time.sleep(delay_seconds)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run an instructor temperature demo against the chatbot pipeline.")
    parser.add_argument(
        "--prompt",
        default="Suggest a 3-day itinerary for Tokyo.",
        help="Prompt to run repeatedly at different temperatures.",
    )
    parser.add_argument(
        "--repeats",
        type=int,
        default=5,
        help="Number of runs per temperature setting.",
    )
    parser.add_argument(
        "--high-temp",
        type=float,
        default=1.0,
        help="High temperature value.",
    )
    parser.add_argument(
        "--low-temp",
        type=float,
        default=0.0,
        help="Low temperature value.",
    )
    parser.add_argument(
        "--delay-seconds",
        type=float,
        default=7.0,
        help="Delay between calls to reduce rate-limit issues for trial keys.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    if args.repeats < 1:
        raise ValueError("--repeats must be >= 1")

    for label, value in (("high", args.high_temp), ("low", args.low_temp)):
        if value < 0.0 or value > 1.0:
            raise ValueError(f"--{label}-temp must be between 0.0 and 1.0")

    run_demo(
        prompt=args.prompt,
        repeats=args.repeats,
        high_temp=args.high_temp,
        low_temp=args.low_temp,
        delay_seconds=args.delay_seconds,
    )


if __name__ == "__main__":
    main()
