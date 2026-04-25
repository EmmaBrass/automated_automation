# ADR-003: Coding-Agent CLI Adapter

Date: 2026-04-25
Status: Accepted

## Decision
Use Codex CLI as default LLM execution backend behind a provider-swappable CLI adapter (Codex now, Claude/etc later).

## Rationale
- Reuse mature commercial coding-agent capability.
- Avoid coupling orchestration logic to a specific provider command surface.
- Keep migration path open with minimal code churn.

## Consequences
- Worker services execute allowlisted CLI profiles only.
- All CLI executions produce typed execution reports and artifact refs.
- Provider-specific behavior is isolated in adapter implementations.
