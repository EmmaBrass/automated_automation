# ADR-005: Web UI and CLI Execution Safety

Date: 2026-04-25
Status: Accepted

## Decision
Browser UI cannot execute shell commands directly. CLI execution occurs only in backend workers with allowlisted command profiles and constrained runtime policies.

## Rationale
- Enforce least privilege and reduce command-injection risk.
- Centralize execution auditing and failure handling.
- Provide deterministic traceability for all agent actions.

## Consequences
- Web app submits jobs; worker performs execution.
- Each execution is linked to run/trace IDs and persisted reports.
- Command policies (timeout/resources/profile) are mandatory.
