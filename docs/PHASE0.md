# Phase 0: Greenfield Baseline

## Completed
- Greenfield service skeletons created for: `api`, `chem_planner`, `procurement`, `discovery`, `placement`, `interop`, `cad`, `capability`, `synthesis`, `verification`, `orchestrator`.
- Baseline local infra manifest added at `infra/docker-compose.yml` (Postgres, MinIO, NATS).
- Canonical contracts established under `packages/contracts/schemas` with paired examples under `packages/contracts/examples`.
- Request context propagation implemented globally with headers:
  - `x-trace-id`
  - `x-run-id`
  - `x-device-id`
- Shared FastAPI app factory applies middleware so all services emit/propagate IDs consistently.
- Initial unit tests added for:
  - request-ID generation and propagation,
  - service `/run` endpoint skeleton behavior,
  - schema/example validation.

## Canonical Planning Location
All active planning markdown for this program is now maintained in:
- `automated-automation/docs/`

## Next (Phase 1)
- Implement typed request/response models per service contract.
- Add message bus topics and job envelope schema for async orchestration.
- Stand up a first end-to-end “intent -> plan -> dry-run verification report” flow.
- Add architecture ADR for MCP-first integration and app-native orchestration (LangGraph deferred).
