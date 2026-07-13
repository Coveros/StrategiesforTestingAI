#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

python -m pip install -r requirements.txt

echo "Verifying Arize Phoenix installation..."
python -c "import phoenix" >/dev/null 2>&1 || {
  echo "Warning: Arize Phoenix import check failed. Retry with: python -m pip install -r requirements.txt"
}

if ! command -v ollama >/dev/null 2>&1; then
  echo "Installing Ollama..."
  curl -fsSL https://ollama.com/install.sh | sh
fi

MODEL="${OLLAMA_MODEL:-llama3.2:1b}"

echo "Starting Ollama service for initial model pull..."
nohup ollama serve >/tmp/ollama.log 2>&1 &

for i in {1..30}; do
  if ollama list >/dev/null 2>&1; then
    break
  fi
  sleep 1
done

echo "Ensuring model is present: ${MODEL}"
ollama pull "${MODEL}" || echo "Warning: model pull failed during post-create. You can retry with: ollama pull ${MODEL}"

echo "Devcontainer setup complete."
