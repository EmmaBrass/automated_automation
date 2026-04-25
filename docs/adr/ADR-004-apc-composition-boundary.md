# ADR-004: APC Composition Boundary

Date: 2026-04-25
Status: Accepted

## Decision
`automated-automation` encloses `apc_platform` by composition. APC remains source-of-truth for workflow authoring/runtime operations.

## Rationale
- Prevent duplicate orchestration/runtime implementations.
- Preserve existing APC roadmap and UI investments.
- Keep AA focused on pre-runtime synthesis/integration tasks.

## Consequences
- AA outputs promoted artifacts/contracts that APC consumes.
- AA does not replicate APC run UI, workflow runtime, resource manager, or device console.
- Integration is contract-driven and versioned.
