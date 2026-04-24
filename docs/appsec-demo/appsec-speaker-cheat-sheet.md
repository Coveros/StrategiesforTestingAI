# AppSec Speaker Cheat Sheet

Use this during the live runtime remediation segment.

## Demo Narrative in One Line

Start with concrete findings, apply minimal hardening edits live, validate against baseline controls, and roll back safely.

## Fast Agenda Cues

1. Find and rank risks.
2. Apply targeted edits only.
3. Re-check control coverage.
4. Show rollback confidence.

## Mapping: Patch to Control

- P-001 -> AS-05: CORS hardening
- P-002 -> AS-03: reset token helper
- P-003 -> AS-03: reset endpoint auth check
- P-004 -> AS-05: secure debug default
- P-005 -> AS-01: prompt safety hardening

## Talking Points by Patch

### P-001 CORS hardening in app/main.py

Before:

- API accepts cross-origin requests from any origin.
- Risk: browser-based abuse and broad cross-site exposure.

After:

- CORS is scoped to configured trusted origins for API paths.
- Risk reduction: narrows browser origin surface and enforces environment policy.

Say this:

- "This is a one-location hardening edit with high impact and low blast radius."

### P-002 Reset token helper in app/main.py

Before:

- Reset path has no reusable auth helper for privileged reset calls.
- Risk: no central gate for sensitive reset operations.

After:

- Adds a token validation helper based on RESET_API_TOKEN.
- Risk reduction: introduces an explicit privilege gate.

Say this:

- "We made authentication explicit and reusable so future privileged routes can reuse the same guard."

### P-003 Reset endpoint token check in app/main.py

Before:

- Reset endpoint processes requests without token enforcement.
- Risk: unauthorized state mutation.

After:

- Endpoint blocks invalid or missing token with 401 when token is configured.
- Risk reduction: converts an open state-changing endpoint into a guarded one.

Say this:

- "This is the behavioral guardrail: unauthorized requests now fail closed."

### P-004 Debug default hardening in app/main.py

Before:

- Debug default is true if environment is not set.
- Risk: accidental debug exposure in non-dev scenarios.

After:

- Debug default is false; debug must be explicitly enabled.
- Risk reduction: safer default posture.

Say this:

- "Secure defaults matter because configuration drift is common."

### P-005 Prompt safety hardening in app/rag_pipeline.py

Before:

- User query interpolates directly into prompt body.
- Risk: easier prompt-injection influence and control confusion.

After:

- Adds simple query sanitization and explicit safety rules in prompt preamble.
- Risk reduction: clearer instruction hierarchy and reduced injection surface.

Say this:

- "This is not perfect prevention, but it meaningfully raises resilience with minimal code change."

## Live Prompt Script

Use these prompts in order.

1. "[Agent selected: AppSec Triage Agent] Run /vulnerability-discovery for app and static/js, top 5 findings, and map each to docs/appsec-demo/appsec-baseline-standard.md."
2. "[Agent selected: Remediation Coach Agent] Run /runtime-remediation in apply mode for F-001, F-002, F-003, and F-004. Apply minimal reversible edits and list changed files."
3. "[Agent selected: Remediation Coach Agent] Run /remediation-validation against docs/appsec-demo/appsec-baseline-standard.md and report unresolved risk."
4. "[Agent selected: Remediation Coach Agent] Provide rollback commands and rollback reasoning for all changed files."

Invocation rule for live talks:

- Always explicitly select the agent in the agent picker before sending prompts.
- If your client supports explicit syntax (`@AgentName` or slash invocations), prefer that over name-only phrasing.

## Scripted Command Flow

1. python appsec_runtime_remediation_demo.py --mode assess
2. python appsec_runtime_remediation_demo.py --mode apply
3. python appsec_runtime_remediation_demo.py --mode assess
4. python appsec_runtime_remediation_demo.py --mode rollback
5. python appsec_runtime_remediation_demo.py --mode assess

## If Demo Output Varies

- Anchor to control mapping, not exact wording.
- Emphasize evidence-backed findings and minimal diffs.
- Fall back to scripted mode if interactive agent output drifts.

## Q and A Backup Answers

- Why allow runtime edits?
  - To demonstrate end-to-end secure coding acceleration plus human-governed rollback.
- Is this a full security audit?
  - No. This is a targeted, evidence-driven hardening workflow.
- Why keep patches small?
  - Smaller edits are easier to review, safer to ship, and easier to roll back.
