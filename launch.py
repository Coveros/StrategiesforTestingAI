#!/usr/bin/env python3
"""
Quick launcher for the current Exercise 1-9 curriculum.

This launcher exposes only the workflows used by the reconfigured course.
"""

import os
import sys
import subprocess


def get_preferred_python():
    """Return venv Python when available, otherwise current interpreter."""
    venv_python = r"c:\Users\jpayne\Documents\Training\Notebooks for ML classes\training-env\Scripts\python.exe"
    return venv_python if os.path.exists(venv_python) else sys.executable


def safe_input(prompt: str):
    """Read input safely; return None when stdin is unavailable."""
    try:
        return input(prompt)
    except EOFError:
        return None


def pause_for_user(prompt: str = "\nPress Enter to return to menu..."):
    """Pause only when interactive input is available."""
    if sys.stdin and sys.stdin.isatty():
        safe_input(prompt)

def show_menu():
    """Show main menu."""
    print("🧪 GenAI Testing Tutorial - Quick Launcher")
    print("=" * 60)
    print()
    print("1. 🧪 Run Regression Testing")
    print("   Test against gold standards with quality gates")
    print()
    print("2. 📊 Run Evaluation Framework")
    print("   Metric definitions used in Exercise 3")
    print()
    print("3. 🔍 Run Retrieval Experiment")
    print("   Optional tuning support for Exercise 4")
    print()
    print("4. 🚀 Start Flask Application")
    print("   Launch the chat interface")
    print()
    print("5. 🛡️ Run Section 7 NFR Quick-Run")
    print("   Generate Exercise 7 evidence artifacts")
    print()
    print("6. 🤖 Run Section 9 Agentic CI Suite")
    print("   Generate Exercise 9 gate artifacts")
    print()
    print("7. 📚 Open Documentation")
    print("   View comprehensive guides and documentation")
    print()
    print("0. Exit")
    print()

def run_regression_testing():
    """Launch regression testing."""
    print("🧪 Launching Regression Testing...")
    python_exec = get_preferred_python()
    
    if python_exec != sys.executable:
        print("Using training-env virtual environment with tf-keras...")
        try:
            subprocess.run([python_exec, "-m", "regression_testing.regression_testing"], check=True)
        except subprocess.CalledProcessError as e:
            print(f"❌ Error running regression tests: {e}")
    else:
        try:
            subprocess.run([python_exec, "-m", "regression_testing.regression_testing"], check=True)
        except subprocess.CalledProcessError as e:
            print(f"❌ Error running regression tests: {e}")
        except FileNotFoundError:
            print("❌ Python not found. Make sure Python is in your PATH.")

def run_evaluation_framework():
    """Run evaluation framework."""
    print("📊 Running Evaluation Framework...")
    python_exec = get_preferred_python()
    try:
        subprocess.run([python_exec, "tests/evaluation_framework.py"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running evaluation framework: {e}")
    except FileNotFoundError:
        print("❌ Python not found. Make sure Python is in your PATH.")

def run_retrieval_experiment():
    """Run optional retrieval tuning experiment used by Exercise 4."""
    print("🔍 Running Retrieval Experiment...")
    python_exec = get_preferred_python()
    try:
        subprocess.run([python_exec, "experiments/retrieval_experiments.py"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running retrieval experiment: {e}")
    except FileNotFoundError:
        print("❌ Python not found. Make sure Python is in your PATH.")

def start_flask_app():
    """Start the Flask application."""
    python_exec = get_preferred_python()

    if python_exec != sys.executable:
        print("Using training-env virtual environment...")

    print("🚀 Starting Flask Application...")
    print("The chat interface will be available at: http://localhost:5000")
    print("Press Ctrl+C to stop the server.")
    try:
        # Preflight dependency check so users get an actionable fix command.
        dependency_check = subprocess.run(
            [python_exec, "-c", "import flask, flask_cors"],
            capture_output=True,
            text=True,
        )

        if dependency_check.returncode != 0:
            print("❌ Missing required Flask dependencies for this Python environment.")
            print(f"Using Python: {python_exec}")
            print("Install dependencies with:")
            print(f"  \"{python_exec}\" -m pip install -r requirements.txt")
            return

        subprocess.run([python_exec, "run.py"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Error starting Flask app: {e}")
    except KeyboardInterrupt:
        print("\n🛑 Server stopped.")
    except FileNotFoundError:
        print("❌ Python not found. Make sure Python is in your PATH.")

def run_section7_quickrun():
    """Run Section 7 quick-run artifact generator."""
    print("🛡️ Running Section 7 NFR Quick-Run...")
    python_exec = get_preferred_python()
    try:
        subprocess.run([python_exec, "section7_nfr_quickrun.py"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running Section 7 quick-run: {e}")
    except FileNotFoundError:
        print("❌ Python not found. Make sure Python is in your PATH.")

def run_section9_suite():
    """Run Section 9 agentic CI suite artifact generator."""
    print("🤖 Running Section 9 Agentic CI Suite...")
    python_exec = get_preferred_python()
    try:
        subprocess.run([python_exec, "section9_agentic_test_suite.py"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running Section 9 suite: {e}")
    except FileNotFoundError:
        print("❌ Python not found. Make sure Python is in your PATH.")

def open_documentation():
    """Show documentation options."""
    print("📚 Available Documentation:")
    print()
    print("Main documentation files:")
    print("• README.md - Main project overview (this directory)")
    print("• docs/Exercise-1.md ... docs/Exercise-9.md - Student lab guides")
    print("• docs/Exercise-1-Instructor-Notes.md ... Exercise-9-Instructor-Notes.md")
    print("• docs/Section-Bridge-RAG-to-Agentic.md - Section transition deck text")
    print()
    print("Online documentation:")
    print("• Open any .md file in a text editor or markdown viewer")
    print("• Use VS Code or similar for best viewing experience")
    
    # Try to open main README
    doc_choice = (safe_input("Open main README.md? (y/n): ") or "n").strip().lower()
    if doc_choice == 'y':
        try:
            if os.name == 'nt':  # Windows
                os.startfile("README.md")
            elif os.name == 'posix':  # macOS and Linux
                subprocess.run(["open", "README.md"], check=True)
        except Exception as e:
            print(f"❌ Could not open README.md automatically: {e}")
            print("Please open README.md in your preferred text editor.")

def main():
    """Main launcher."""
    while True:
        show_menu()
        
        try:
            raw_choice = safe_input("Select option (0-7): ")
            if raw_choice is None:
                print("\n👋 Input stream closed. Exiting launcher.")
                break
            choice = raw_choice.strip()
            
            if choice == "0":
                print("👋 Happy testing! Remember to explore all the testing approaches!")
                break
            elif choice == "1":
                run_regression_testing()
            elif choice == "2":
                run_evaluation_framework()
            elif choice == "3":
                run_retrieval_experiment()
            elif choice == "4":
                start_flask_app()
            elif choice == "5":
                run_section7_quickrun()
            elif choice == "6":
                run_section9_suite()
            elif choice == "7":
                open_documentation()
            else:
                print("❌ Invalid choice. Please select 0-7.")
            
            if choice != "0" and choice != "6":  # Don't pause after Flask app
                pause_for_user("\nPress Enter to return to menu...")
                print("\n" + "="*80)
                
        except KeyboardInterrupt:
            print("\n\n👋 Launcher interrupted. Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {str(e)}")
            pause_for_user("Press Enter to continue...")

if __name__ == "__main__":
    # Change to script directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    print("🔧 GenAI Testing Tutorial Quick Launcher")
    print("Working directory:", os.getcwd())
    print()
    
    main()