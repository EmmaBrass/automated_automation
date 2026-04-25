# Pre-Driver Scope (Current Build Boundary)

Date: April 25, 2026

## Active Scope
For the current implementation phase, `automated-automation` stops at:
1. Chemical intent intake.
2. Protocol-step planning.
3. Capability and hardware requirement mapping.
4. BOM generation from approved sources.
5. Workspace/layout notes.
6. Human build manual generation.
7. Human clarification interface for build-manual questions.

## Explicitly Deferred
- Driver generation.
- Firmware flashing.
- APC orchestration-runtime integration for execution.
- VLM-in-the-loop driver testing/repair.

## Interface Requirement (Human-in-the-loop)
The system must provide a conversational interface where the human can:
- ask clarification questions about any build step,
- report blockers (missing connector, unclear orientation, inaccessible slot),
- receive revised instructions/actions while preserving run and trace context.

## API Endpoints Implemented In This Phase
- `POST /v1/pre-driver/plan`
- `GET /v1/pre-driver/plan/{run_id}`
- `POST /v1/pre-driver/plan/{run_id}/manual-chat`

These endpoints define the first executable vertical slice before any driver-generation logic is added.
