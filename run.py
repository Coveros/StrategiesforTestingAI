#!/usr/bin/env python3
"""
GenAI Testing Tutorial - RAG Chatbot Application
Entry point for running the Flask application
"""

import os
import sys
import subprocess

# Add the app directory to the Python path
sys.path.insert(0, os.path.dirname(__file__))

def format_pip_install_cmd() -> str:
    """Return a pip install command that targets the active interpreter."""
    return f'"{sys.executable}" -m pip install -r requirements.txt'


def get_project_venv_python() -> str | None:
    """Return project venv Python path when present, otherwise None."""
    base_dir = os.path.dirname(__file__)
    parent_dir = os.path.dirname(base_dir)
    if os.name == "nt":
        candidates = [
            os.path.join(base_dir, "training-env", "Scripts", "python.exe"),
            os.path.join(parent_dir, "training-env", "Scripts", "python.exe"),
        ]
    else:
        candidates = [
            os.path.join(base_dir, "training-env", "bin", "python"),
            os.path.join(parent_dir, "training-env", "bin", "python"),
        ]

    for candidate in candidates:
        if os.path.exists(candidate):
            return candidate

    return None


def maybe_relaunch_with_project_venv():
    """Relaunch this script with project venv Python when available."""
    # Avoid relaunch loops.
    if os.getenv("TESTING_AI_SKIP_VENV_REDIRECT") == "1":
        return

    venv_python = get_project_venv_python()
    if not venv_python:
        return

    current_python = os.path.abspath(sys.executable)
    if os.path.abspath(venv_python) == current_python:
        return

    print("🔁 Switching to project virtual environment interpreter...")
    env = os.environ.copy()
    env["TESTING_AI_SKIP_VENV_REDIRECT"] = "1"
    cmd = [venv_python, os.path.abspath(__file__), *sys.argv[1:]]
    rc = subprocess.call(cmd, env=env)
    sys.exit(rc)


if __name__ == '__main__':
    maybe_relaunch_with_project_venv()


try:
    from dotenv import load_dotenv
except ModuleNotFoundError as e:
    missing = getattr(e, "name", "unknown module")
    print("❌ Missing required Python dependency:")
    print(f"   - {missing}")
    print("\nInstall project dependencies with your current interpreter:")
    print(f"   {format_pip_install_cmd()}")

    venv_python = get_project_venv_python()
    if venv_python:
        print("\nOr run using the project virtual environment interpreter:")
        print(f"   \"{venv_python}\" -m pip install -r requirements.txt")
        print(f"   \"{venv_python}\" run.py")

    print("\nThen run this command again.")
    sys.exit(1)


# Load environment variables
load_dotenv()


# Import and run the Flask app
try:
    from app.main import app
except ModuleNotFoundError as e:
    missing = getattr(e, "name", "unknown module")
    print("❌ Missing required Python dependency:")
    print(f"   - {missing}")
    print("\nInstall project dependencies with your current interpreter:")
    print(f"   {format_pip_install_cmd()}")

    venv_python = get_project_venv_python()
    if venv_python:
        print("\nOr run using the project virtual environment interpreter:")
        print(f"   \"{venv_python}\" -m pip install -r requirements.txt")
        print(f"   \"{venv_python}\" run.py")

    print("\nThen run this command again.")
    sys.exit(1)

if __name__ == '__main__':
    # Validate required environment variables
    required_vars = ['COHERE_API_KEY']
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        print("❌ Missing required environment variables:")
        for var in missing_vars:
            print(f"   - {var}")
        print("\nPlease add your LLM API Key to the .env file.")
        sys.exit(1)
    
    print("🚀 Starting GenAI Testing Tutorial Application...")
    print(f"📚 Documents directory: {os.path.join(os.path.dirname(__file__), 'data', 'documents')}")
    print(f"🔧 Environment: {os.getenv('FLASK_ENV', 'development')}")
    print(f"🌐 Server will start on: http://localhost:{os.getenv('FLASK_PORT', 5000)}")
    print("\n" + "="*50)
    
    # Start the Flask application
    app.run(
        host='0.0.0.0',
        port=int(os.getenv('FLASK_PORT', 5000)),
        debug=os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    )