# ADR-002: MCP-First + App-Native Orchestration

Date: 2026-04-25
Status: Accepted

## Decision
Use MCP as the LLM tool/resource interface boundary. Keep orchestration/workflow state in application services (not LangGraph in v1).

## Rationale
- Clear trust and contract boundary for LLM actions.
- Deterministic orchestration in core backend for safety and auditability.
- Minimize architecture complexity during v1.

## Consequences
- MCP contracts become first-class API surface.
- LangGraph remains optional and deferred until concrete durability/branching needs emerge.
