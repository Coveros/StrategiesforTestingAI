# Codespaces Setup Guide for Personal GitHub Accounts

## Overview

Personal GitHub accounts can run these exercises on the **free 2-core machine**. The setup is optimized for this constraint:

- **Inference is slower** (~30 seconds per LLM request vs. ~3 seconds on 4-core)
- **But it works reliably** without timeouts or crashes
- **No upgrade needed** — boot and go

If you want faster responses, you can optionally upgrade to 4-core mid-session (instructions below).

## Quick Start Steps

### 1. Create a Codespace
- Go to the repository on GitHub
- Click **"< > Code"** → **"Codespaces"** tab → **"Create codespace on main"**
- Wait for boot (~2-3 minutes)
- VS Code will open automatically

### 2. Start the Flask App
Once VS Code is open, open a terminal and run:

```bash
python run.py
```

Then visit **http://localhost:5000** to access the exercises.

That's it. Ollama and the model start automatically in the background.

### 3. Verify Ollama is Ready (Optional)
```bash
ollama list        # should show llama3.2:1b
grep -c ^processor /proc/cpuinfo  # shows 2 (or 4 if you upgraded)
```

## Performance Notes

**On 2-core (free tier):**
- First LLM request: ~40-50 seconds (model loads)
- Subsequent requests: ~20-30 seconds each
- This is normal for CPU inference

**If responses are too slow:**
- Go to https://github.com/codespaces
- Click ⋯ next to your Codespace → **"Change machine type"** → select **4-core**
- Close VS Code, then open https://github.com/codespaces and click ⋯ → **"Open in Browser"**
- Wait ~2 minutes for restart
- Responses will be ~10x faster

## Troubleshooting

### "500 Server Error: Internal Server Error for url: http://127.0.0.1:11434/api/generate"
**Cause**: Ollama not running or timed out
**Fix**: Wait 30-60 seconds and try again. Inference on 2-core is slow. If it persists, check `/tmp/ollama.log`

### Responses are very slow (30+ seconds)
**Expected on 2-core.** This is normal for CPU inference. If unacceptable, upgrade to 4-core:
1. Go to https://github.com/codespaces
2. Click ⋯ → **"Change machine type"** → **4-core**
3. Close browser tab
4. Open https://github.com/codespaces → ⋯ → **"Open in Browser"**
5. Wait ~2 minutes for restart

### Ollama model won't download
**Cause**: Network or disk space
**Fix**: Run `ollama pull llama3.2:1b` in a fresh terminal. Check disk space: `df -h`

## Cost Notes

- **2-core Codespace**: Free for personal accounts (within monthly core-hour limits)
  - For a 3-day × 4-hour course: ~24 core-hours, well within the 120 free core-hours/month
- **4-core Codespace (optional upgrade)**: Billable (~$0.36/hour)
  - Only upgrade if you need faster responses
  - Only active while you're using it — auto-stops after 240 minutes idle

## Questions?

If you hit issues:
1. Check /tmp/ollama.log in the terminal
2. Verify you're on a 4-core machine: `grep -c ^processor /proc/cpuinfo`
3. Try restarting the post-start: `bash .devcontainer/post-start.sh`
