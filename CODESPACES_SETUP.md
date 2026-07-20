# Codespaces Setup Guide for Personal GitHub Accounts

## Problem: Machine Size Constraints

Personal GitHub accounts have limited access to Codespaces machine sizes. To balance availability with performance:

- **Initial boot**: 2-core machine (free/standard tier for personal accounts)
- **Exercises require**: 4-core machine (for Ollama LLM inference to run without timeouts)

## Quick Start Steps

### 1. Create a Codespace
- Go to the repository on GitHub
- Click **"< > Code"** → **"Codespaces"** tab → **"Create codespace on main"**
- Wait for boot (you'll see "Setting up your codespace..." then a VS Code window opens)

### 2. Upgrade Machine Size (Required)
Once the Codespace starts and you see the VS Code editor:

1. Click your **profile icon** (bottom-left corner) or the **Codespaces menu**
2. Select **"Change machine type"**
3. Pick **4-core** from the list
4. Click **"Update machine"** or **"Upgrade"**
5. Wait ~2 minutes for rebuild

### 3. Start Ollama (After Upgrade)
Once the machine finishes upgrading, open a terminal in VS Code and run:

```bash
bash .devcontainer/start-ollama.sh
```

You'll see messages like:
```
✅ Detected 4 CPU cores. Proceeding with Ollama startup...
Pulling model llama3.2:1b... (this may take 1-2 minutes)
✅ Model llama3.2:1b is ready
✅ Ollama is ready! You can now:
   - Start the Flask app: python run.py
```

### 4. Start the Flask App
```bash
python run.py
```

Then visit http://localhost:5000 to access the exercises.

## Troubleshooting

### "500 Server Error: Internal Server Error for url: http://127.0.0.1:11434/api/generate"
**Cause**: Ollama not running or not enough CPU cores
**Fix**: Run `bash .devcontainer/start-ollama.sh` after upgrading to 4-core

### Post-start shows "⚠️ WARNING: Insufficient CPU cores"
**Cause**: Machine upgrade hasn't completed yet
**Fix**: Wait for the rebuild to finish, then run `bash .devcontainer/start-ollama.sh`

### "llama-server process has terminated: signal: terminated"
**Cause**: 2-core machine can't handle inference
**Fix**: Ensure you upgraded to 4-core and wait for rebuild to complete

## Cost Notes

- **2-core Codespace**: Free for personal accounts (limited hours)
- **4-core Codespace**: Billable (~$0.18/hour for GitHub account holders in supported regions)
  - You can pause/stop the Codespace to save compute time
  - Delete the Codespace when done with exercises

## Questions?

If you hit issues:
1. Check /tmp/ollama.log in the terminal
2. Verify you're on a 4-core machine: `grep -c ^processor /proc/cpuinfo`
3. Try restarting the post-start: `bash .devcontainer/post-start.sh`
