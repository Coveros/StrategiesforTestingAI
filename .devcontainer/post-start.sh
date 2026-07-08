#!/usr/bin/env bash
set -euo pipefail

MODEL="${OLLAMA_MODEL:-llama3.2:1b}"

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
