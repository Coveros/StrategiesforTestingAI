#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

if [ -f .env ]; then
  # Export .env values when present; don't fail startup on malformed .env lines.
  set +e
  set -a
  # shellcheck disable=SC1091
  . ./.env
  ENV_LOAD_RC=$?
  set +a
  set -e
  if [ "${ENV_LOAD_RC}" -ne 0 ]; then
    echo "Warning: .env could not be fully parsed; continuing with defaults where needed."
  fi
fi

MODEL="${OLLAMA_MODEL:-llama3.2:1b}"

ensure_ollama_prerequisites() {
  if command -v zstd >/dev/null 2>&1; then
    return 0
  fi

  echo "Installing Ollama prerequisite: zstd"

  install_zstd_with_apt() {
    if command -v sudo >/dev/null 2>&1; then
      if sudo apt-get install -y zstd; then
        return 0
      fi

      # Retry with Debian base sources only to avoid broken third-party repo entries.
      if [ -f /etc/apt/sources.list.d/debian.sources ]; then
        sudo apt-get update -y \
          -o Dir::Etc::sourcelist=/etc/apt/sources.list.d/debian.sources \
          -o Dir::Etc::sourceparts=- && sudo apt-get install -y zstd
      elif [ -f /etc/apt/sources.list ]; then
        sudo apt-get update -y \
          -o Dir::Etc::sourcelist=/etc/apt/sources.list \
          -o Dir::Etc::sourceparts=- && sudo apt-get install -y zstd
      else
        return 1
      fi
    else
      if apt-get install -y zstd; then
        return 0
      fi

      if [ -f /etc/apt/sources.list.d/debian.sources ]; then
        apt-get update -y \
          -o Dir::Etc::sourcelist=/etc/apt/sources.list.d/debian.sources \
          -o Dir::Etc::sourceparts=- && apt-get install -y zstd
      elif [ -f /etc/apt/sources.list ]; then
        apt-get update -y \
          -o Dir::Etc::sourcelist=/etc/apt/sources.list \
          -o Dir::Etc::sourceparts=- && apt-get install -y zstd
      else
        return 1
      fi
    fi
  }

  if command -v apt-get >/dev/null 2>&1; then
    install_zstd_with_apt || {
      echo "Warning: failed to install zstd via apt-get (including Debian-only fallback)."
      return 1
    }
  else
    echo "Warning: apt-get not found; install zstd manually before installing Ollama."
    return 1
  fi

  command -v zstd >/dev/null 2>&1
}

ensure_ollama_installed() {
  if command -v ollama >/dev/null 2>&1; then
    return 0
  fi

  echo "Ollama is missing; attempting installation..."
  local install_rc=1
  if command -v curl >/dev/null 2>&1; then
    if command -v sudo >/dev/null 2>&1; then
      if curl -fsSL https://ollama.com/install.sh | sudo -E sh; then
        install_rc=0
      fi
    else
      if curl -fsSL https://ollama.com/install.sh | sh; then
        install_rc=0
      fi
    fi
  elif command -v wget >/dev/null 2>&1; then
    if command -v sudo >/dev/null 2>&1; then
      if wget -qO- https://ollama.com/install.sh | sudo -E sh; then
        install_rc=0
      fi
    else
      if wget -qO- https://ollama.com/install.sh | sh; then
        install_rc=0
      fi
    fi
  else
    echo "Warning: neither curl nor wget is available; cannot auto-install Ollama."
    return 1
  fi

  if [ "${install_rc}" -ne 0 ]; then
    echo "Warning: Ollama install script failed."
    echo "Hint: in Codespaces, verify sudo/network by running:"
    echo "  curl -fsSL https://ollama.com/install.sh | sudo -E sh"
    return 1
  fi

  if ! command -v ollama >/dev/null 2>&1 && [ -x /usr/local/bin/ollama ]; then
    export PATH="/usr/local/bin:${PATH}"
    if ! grep -q '/usr/local/bin' "${HOME}/.bashrc" 2>/dev/null; then
      echo 'export PATH="/usr/local/bin:${PATH}"' >> "${HOME}/.bashrc"
    fi
  fi

  if ! command -v ollama >/dev/null 2>&1 && [ -x /usr/bin/ollama ]; then
    export PATH="/usr/bin:${PATH}"
    if ! grep -q '/usr/bin' "${HOME}/.bashrc" 2>/dev/null; then
      echo 'export PATH="/usr/bin:${PATH}"' >> "${HOME}/.bashrc"
    fi
  fi

  command -v ollama >/dev/null 2>&1
}

start_ollama_if_needed() {
  if ! pgrep -f "ollama serve" >/dev/null 2>&1; then
    echo "Starting Ollama service..."
    nohup ollama serve >/tmp/ollama.log 2>&1 &
  fi
}

wait_for_ollama() {
  for i in {1..60}; do
    if ollama list >/dev/null 2>&1; then
      return 0
    fi
    sleep 1
  done
  return 1
}

print_startup_status() {
  local mlflow_cli="no"
  local mlflow_running="no"
  local ollama_cli="no"
  local ollama_running="no"
  local model_ready="no"

  if command -v mlflow >/dev/null 2>&1; then
    mlflow_cli="yes"
  fi

  if pgrep -f "mlflow server" >/dev/null 2>&1; then
    mlflow_running="yes"
  fi

  if command -v ollama >/dev/null 2>&1; then
    ollama_cli="yes"
    if pgrep -f "ollama serve" >/dev/null 2>&1; then
      ollama_running="yes"
    fi

    if ollama list 2>/dev/null | awk '{print $1}' | grep -qx "${MODEL}"; then
      model_ready="yes"
    fi
  fi

  echo ""
  echo "================ Boot Status ================="
  echo "MLflow CLI available  : ${mlflow_cli}"
  echo "MLflow running        : ${mlflow_running}"
  echo "Ollama CLI available  : ${ollama_cli}"
  echo "Ollama running        : ${ollama_running}"
  echo "Model (${MODEL}) ready : ${model_ready}"
  echo "Chat app URL          : http://localhost:5000"
  echo "MLflow URL            : http://localhost:5001"
  echo "Logs                  : /tmp/ollama.log, /tmp/mlflow.log"
  echo "=============================================="
}

wait_for_mlflow() {
  for i in {1..30}; do
    if curl -s -o /dev/null http://127.0.0.1:5001/health; then
      return 0
    fi
    sleep 1
  done
  return 1
}

python -c "import mlflow" >/dev/null 2>&1 || \
  echo "Warning: MLflow not available in this environment. Run: python -m pip install -r requirements.txt"

if command -v mlflow >/dev/null 2>&1; then
  if ! pgrep -f "mlflow server" >/dev/null 2>&1; then
    echo "Starting MLflow server on port 5001..."
    mkdir -p mlflow_data
    nohup mlflow server \
      --backend-store-uri sqlite:///mlflow_data/mlflow.db \
      --host 0.0.0.0 --port 5001 >/tmp/mlflow.log 2>&1 &
    wait_for_mlflow || echo "Warning: MLflow server did not become ready. See /tmp/mlflow.log"
  fi
else
  echo "Warning: mlflow CLI not found; MLflow auto-start skipped."
fi

if ensure_ollama_prerequisites && ensure_ollama_installed; then
  start_ollama_if_needed

  if wait_for_ollama; then
    if ! ollama list | awk '{print $1}' | grep -qx "${MODEL}"; then
      echo "Model ${MODEL} not found locally; pulling now..."
      ollama pull "${MODEL}" || echo "Warning: model pull failed. Retry with: ollama pull ${MODEL}"
    fi
    
    echo "Pre-warming model ${MODEL} into memory..."
    curl -s http://localhost:11434/api/generate -d "{\"model\": \"${MODEL}\", \"keep_alive\": -1}" > /dev/null 2>&1 || true
  else
    echo "Warning: Ollama service did not become ready. See /tmp/ollama.log"
  fi
else
  echo "Warning: Ollama prerequisite/install/start failed in post-start; demo app may not answer model requests yet."
fi

print_startup_status
