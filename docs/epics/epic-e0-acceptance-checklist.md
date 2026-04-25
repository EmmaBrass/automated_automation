# Epic E0 Acceptance Checklist

Date: 2026-04-25

## Architecture Decisions
- [x] ADR-001 Core infra baseline accepted.
- [x] ADR-002 MCP-first + app-native orchestration accepted.
- [x] ADR-003 Coding-agent CLI adapter accepted.
- [x] ADR-004 APC composition boundary accepted.
- [x] ADR-005 Web/CLI safety model accepted.

## Contracts
- [x] `artifact_ref` schema + example added.
- [x] `sync_event_envelope` schema + example added.
- [x] `agent_cli_execution_report` schema + example added.
- [x] `driver_promotion_contract` schema + example added.
- [x] `orchestration_binding_contract` schema + example added.

## Topology and Data Boundary
- [x] AA/APC ownership and integration sequence documented.
- [x] Separate DB boundary documented.
- [x] MinIO artifact reference policy documented.

## Validation
- [ ] Contract validation tests passing with new schemas/examples.
- [ ] Tabletop trace walkthrough completed and signed off.
