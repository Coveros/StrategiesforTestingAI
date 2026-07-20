#!/usr/bin/env bash
# Helper script to manually start Ollama and pull the model.
# Run this AFTER upgrading your Codespace machine to 4-core.

set -euo pipefail

cd "$(dirname "$0")/.."

if [ -f .env ]; then
  set +e
  set -a
  . ./.env
  ENV_LOAD_RC=$?
  set +a
  set -e
  if [ "${ENV_LOAD_RC}" -ne 0 ]; then
    echo "Warning: .env could not be fully parsed; continuing with defaults where needed."
  fi
fi

MODEL="${OLLAMA_MODEL:-llama3.2:1b}"

# Check CPU count
AVAILABLE_CPUS=$(grep -c ^processor /proc/cpuinfo 2>/dev/null || sysctl -n hw.logicalcpu 2>/dev/null || echo "1")
REQUIRED_CPUS=4

if [ "${AVAILABLE_CPUS}" -lt "${REQUIRED_CPUS}" ]; then
  echo "❌ Error: Still only ${AVAILABLE_CPUS} CPU core(s) available."
  echo ""
  echo "Please upgrade your Codespace machine to 4-core first:"
  echo "1. Go to https://github.com/codespaces"
  echo "2. Click ⋯ next to this Codespace → 'Change machine type'"
  echo "3. Select 4-core → 'Update machine'"
  echo "4. Wait for rebuild (~2 minutes)"
  echo "5. Then re-run this script"
  exit 1
fi

echo "✅ Detected ${AVAILABLE_CPUS} CPU cores. Proceeding with Ollama startup..."

# Source helper functions from post-start.sh
source .devcontainer/post-start.sh

ensure_ollama_prerequisites() {
  if command -v zstd >/dev/null 2>&1; then
    return 0
  fi
  echo "Installing Ollama prerequisite: zstd"
  sudo apt-get update && sudo apt-get install -y zstd
}

ensure_ollama_installed() {
  if command -v ollama >/dev/null 2>&1; then
    return 0
  fi
  echo "Installing Ollama..."
  curl -fsSL https://ollama.com/install.sh | sudo -E sh
}

start_ollama_if_needed() {
  if ! pgrep -f "ollama serve" >/dev/null 2>&1; then
    echo "Starting Ollama service..."
    nohup ollama serve >/tmp/ollama.log 2>&1 &
  fi
}

wait_for_ollama() {
  echo "Waiting for Ollama to start (up to 60 seconds)..."
  for i in {1..60}; do
    if ollama list >/dev/null 2>&1; then
      echo "✅ Ollama is ready"
      return 0
    fi
    echo -n "."
    sleep 1
  done
  echo ""
  return 1
}

# Execute the startup sequence
if ensure_ollama_prerequisites && ensure_ollama_installed; then
  start_ollama_if_needed

  if wait_for_ollama; then
    if ! ollama list | awk '{print $1}' | grep -qx "${MODEL}"; then
      echo ""
      echo "Pulling model ${MODEL}... (this may take 1-2 minutes)"
      if ollama pull "${MODEL}"; then
        echo "✅ Model ${MODEL} is ready"
      else
        echo "❌ Model pull failed. Retry with: ollama pull ${MODEL}"
        exit 1
      fi
    else
      echo "✅ Model ${MODEL} is already loaded"
    fi
    echo ""
    echo "=========================================="
    echo "✅ Ollama is ready! You can now:"
    echo "   - Start the Flask app: python run.py"
    echo "   - Access it at http://localhost:5000"
    echo "=========================================="
  else
    echo "❌ Ollama service did not become ready. Check /tmp/ollama.log"
    exit 1
  fi
else
  echo "❌ Ollama setup failed. See errors above."
  exit 1
fi
