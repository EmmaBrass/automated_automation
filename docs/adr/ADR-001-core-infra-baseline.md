# ADR-001: Core Infra Baseline

Date: 2026-04-25
Status: Accepted

## Decision
Use Postgres + NATS JetStream + MinIO as the v1 core runtime baseline.

## Rationale
- Postgres for operational/queryable state.
- NATS for asynchronous orchestration events and job signaling.
- MinIO for immutable large artifacts and evidence payloads.

## Consequences
- Separate state from artifacts by design.
- Cross-service interactions are event-driven where latency tolerance permits.
- All artifact references must be persisted via typed artifact refs.
