#!/usr/bin/env bash
set -euo pipefail

MODEL="${OLLAMA_MODEL:-llama3.2:1b}"

python -c "import phoenix" >/dev/null 2>&1 || \
  echo "Warning: Arize Phoenix not available in this environment. Run: python -m pip install -r requirements.txt"

if command -v phoenix >/dev/null 2>&1; then
  if ! pgrep -f "phoenix.*serve" >/dev/null 2>&1; then
    echo "Starting Phoenix server on port 6006..."
    nohup phoenix serve --host 0.0.0.0 --port 6006 >/tmp/phoenix.log 2>&1 &
  fi
fi

if ! pgrep -f "ollama serve" >/dev/null 2>&1; then
  echo "Starting Ollama service..."
  nohup ollama serve >/tmp/ollama.log 2>&1 &
fi

for i in {1..30}; do
  if ollama list >/dev/null 2>&1; then
    break
  fi
  sleep 1
done

if ! ollama list | awk '{print $1}' | grep -qx "${MODEL}"; then
  echo "Model ${MODEL} not found locally; pulling now..."
  ollama pull "${MODEL}" || echo "Warning: model pull failed. Retry with: ollama pull ${MODEL}"
fi
