# Codespaces Setup Guide for Personal GitHub Accounts

## Overview

Personal GitHub accounts can run these exercises on the **free 2-core machine**. The setup is optimized for this constraint:

- **Inference is slower** (~30 seconds per LLM request vs. ~3 seconds on 4-core)
- **But it works reliably** without timeouts or crashes
- **No upgrade needed** — boot and go

This guide intentionally stays on the free-machine profile: 2 CPUs, 4 GB RAM,
and 32 GB storage. Do not change the machine size for this demo.

## Quick Start Steps

### 1. Create a Codespace
- Go to the repository on GitHub
- Click **"< > Code"** → **"Codespaces"** tab → **"Create codespace on main"**
- Wait for boot (~2-3 minutes)
- VS Code will open automatically

### 2. Start the Flask App
Once VS Code is open, confirm the workspace interpreter is `.venv` and run:

```bash
python run.py
```

Then visit **http://localhost:5000** to access the exercises.

Ollama and the model start automatically in the background. Startup warmup is
disabled to avoid loading the embedding model and Ollama twice on the 2-core
machine. The first real request may take 30-60 seconds while CPU inference
loads; later requests should be faster.

### 3. Verify Ollama is Ready (Optional)
```bash
ollama list        # should show llama3.2:1b
  grep -c ^processor /proc/cpuinfo  # should show 2
```

## Performance Notes

**On 2-core (free tier):**
- First LLM request: ~40-50 seconds (model loads)
- Subsequent requests: ~20-30 seconds each
- This is normal for CPU inference

If responses are slow, wait for the first model load to finish and avoid sending
parallel requests. The application serializes local inference to protect the
4 GB memory limit.

## Troubleshooting

### "500 Server Error: Internal Server Error for url: http://127.0.0.1:11434/api/generate"
**Cause**: Ollama not running or timed out
**Fix**: Wait 30-60 seconds and try again. Inference on 2-core is slow. If it persists, check `/tmp/ollama.log`

### Responses are very slow (30+ seconds)
**Expected on 2-core.** This is normal for CPU inference. Avoid parallel requests
and allow the first request to finish loading the model.

### Ollama model won't download
**Cause**: Network or disk space
**Fix**: Run `ollama pull llama3.2:1b` in a fresh terminal. Check disk space: `df -h`

## Cost Notes

- **2-core Codespace**: Free for personal accounts (within monthly core-hour limits)
  - For a 3-day × 4-hour course: ~24 core-hours, well within the 120 free core-hours/month
- The demo targets the free 2-core, 4 GB, 32 GB Codespace profile.

## Questions?

If you hit issues:
1. Check /tmp/ollama.log in the terminal
2. Verify you're on a 2-core machine: `grep -c ^processor /proc/cpuinfo`
3. Try restarting the post-start: `bash .devcontainer/post-start.sh`
4. MLflow tracing is optional; the chat app remains usable when port 5001 is unavailable.
