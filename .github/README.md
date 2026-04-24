# Custom Agent Assets for AppSec Demo

This folder contains reusable GitHub Copilot customization assets for a 1-hour AppSec talk.

## What is included

- `copilot-instructions.md`: Workspace-level defaults for AppSec demo behavior.
- `instructions/appsec-demo.instructions.md`: Task and file-scoped instructions for security analysis and remediation suggestions.
- `agents/appsec-triage.agent.md`: Custom agent focused on evidence-based vulnerability triage.
- `agents/remediation-coach.agent.md`: Custom agent focused on minimal, reviewable patch suggestions.
- `skills/vulnerability-discovery/SKILL.md`: Structured discovery workflow.
- `skills/secure-patch-suggestion/SKILL.md`: Patch suggestion workflow.
- `skills/remediation-validation/SKILL.md`: Post-fix validation workflow.
- `skills/runtime-remediation/SKILL.md`: Controlled live code-edit workflow for demo apply mode.

## Intended use

1. Run analysis with `AppSec Triage Agent`.
2. Produce patch suggestions with `Remediation Coach Agent`.
3. Optionally switch to apply mode for runtime edits with `runtime-remediation`.
4. Re-check findings against the baseline standard in `docs/appsec-demo/appsec-baseline-standard.md`.

Best practice for demos:

- Explicitly select the target custom agent before each prompt.
- Explicitly invoke skills (`/vulnerability-discovery`, `/secure-patch-suggestion`, `/runtime-remediation`, `/remediation-validation`) instead of relying on implicit routing.

Scripted option for live runtime edits:

- `python appsec_runtime_remediation_demo.py --mode assess`
- `python appsec_runtime_remediation_demo.py --mode apply`
- `python appsec_runtime_remediation_demo.py --mode rollback`

Speaker support:

- `docs/appsec-demo/appsec-speaker-cheat-sheet.md`

## Notes

- These assets are demo-oriented and intentionally lightweight.
- Default behavior is suggestion-only remediation.
- Apply mode is supported when explicitly requested, with reversible-edit and rollback guidance.
