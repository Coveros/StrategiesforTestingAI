# Copilot Instructions: AppSec Demo Mode

## Primary objective

Provide agent-assisted application security analysis and remediation for in this repository.

## Required behavior

- Be evidence-driven. Every finding must cite exact file locations.
- Map each finding to a control in `docs/appsec-demo/appsec-baseline-standard.md`.
- Prioritize findings using a simple severity model: Critical, High, Medium, Low.
- Keep remediation outputs small and reviewable.
- Default to patch suggestions as diffs or snippets.
- If explicitly requested, apply runtime code changes in a controlled and reversible way.

## Guardrails

- Do not claim a vulnerability without concrete evidence in code.
- Do not claim a fix is complete without a validation checklist.
- Do not expose secrets or sensitive values in outputs.
- Prefer deterministic, repeatable analysis steps.
- For applied edits, list each changed file and provide rollback guidance.

## Output defaults

When asked for a security review:

1. Findings first, ordered by severity.
2. Evidence references (file and rationale) for each finding.
3. Standard mapping for each finding (control ID).
4. Patch suggestion with minimal blast radius.
5. Post-fix validation steps.