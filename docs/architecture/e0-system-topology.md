# Epic E0 System Topology (v1)

## Component Ownership
- Automated Automation (AA):
  - chemical intent -> protocol -> hardware/BOM
  - geometry/layout/build-manual planning
  - driver generation + VLM verification + promotion
- APC Platform:
  - workflow authoring/runtime
  - run operations UI and experiment tracking
  - results/database views and resource management

## Integration Model
- AA produces promoted orchestration-ready artifacts.
- APC consumes promoted artifacts through typed contracts.
- No direct cross-DB writes between AA and APC.

## Runtime Planes
- Control plane: AA API + workers + MCP facade + orchestration service.
- Orchestration plane: APC services and MCP servers.
- Data plane: Postgres (state), MinIO (artifacts), NATS (events).

## Web to CLI Flow
1. UI submits task request.
2. API persists job and emits event.
3. Worker executes CLI adapter in constrained environment.
4. Worker stores outputs/artifacts.
5. Status and reports are surfaced in UI/API.
