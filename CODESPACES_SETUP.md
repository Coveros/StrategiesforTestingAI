# Codespaces Setup Guide for Personal GitHub Accounts

## Problem: Machine Size Constraints

Personal GitHub accounts have limited access to Codespaces machine sizes. To balance availability with performance:

- **Initial boot**: 2-core machine (free/standard tier for personal accounts)
- **Exercises require**: 4-core machine (for Ollama LLM inference to run without timeouts)

## Quick Start Steps

### 0. Configure Idle Timeout (Do This First!)
Before you start, set your Codespaces idle timeout to the maximum to avoid your machine stopping during class:

1. Go to https://github.com/settings/codespaces
2. Find the **"Idle timeout"** setting
3. Select **"240 minutes"** (4 hours - the maximum)
4. This ensures your Codespace won't stop during our lecture/exercise sessions

### 1. Create a Codespace
- Go to the repository on GitHub
- Click **"< > Code"** → **"Codespaces"** tab → **"Create codespace on main"**
- Wait for boot (you'll see "Setting up your codespace..." then a VS Code window opens)

### 2. Upgrade Machine Size (Required)
Once the Codespace has booted and VS Code is open:

1. Go to **https://github.com/codespaces** in a new browser tab
2. Click the **⋯ menu** next to your Codespace (e.g. "fictional-bassoon")
3. Select **"Change machine type"**
4. Select **4-core** from the list
5. You will see: *"Changes will take effect the next time your codespace restarts"*
6. Close the VS Code browser tab
7. Go back to **https://github.com/codespaces**
8. Click **⋯** next to your Codespace → **"Open in Browser"**
9. Wait ~2 minutes for it to restart and reconnect

### 3. Verify Everything Started
Once VS Code reconnects after the restart, open a terminal and confirm:

```bash
grep -c ^processor /proc/cpuinfo   # should return 4
ollama list                         # should show llama3.2:1b
```

The post-start script runs automatically on restart and handles Ollama startup and model pull. If `ollama list` shows the model, you're ready.

### 4. Start the Flask App
```bash
python run.py
```

Then visit http://localhost:5000 to access the exercises.

## Troubleshooting

### "500 Server Error: Internal Server Error for url: http://127.0.0.1:11434/api/generate"
**Cause**: Ollama not running or still on 2-core
**Fix**: Confirm you're on 4-core (`grep -c ^processor /proc/cpuinfo` returns 4), then run `bash .devcontainer/post-start.sh` to restart services

### Post-start shows "⚠️ WARNING: Insufficient CPU cores"
**Cause**: Machine upgrade hasn't taken effect yet
**Fix**: Close VS Code, go to https://github.com/codespaces, click ⋯ → Open in Browser to restart with the new machine size

### "llama-server process has terminated: signal: terminated"
**Cause**: Still running on 2-core machine
**Fix**: Complete the machine upgrade steps above — do not skip the restart

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
