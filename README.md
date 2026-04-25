# automated-automation

Greenfield repository for autonomous synthesis of robot-operable laboratory environments from chemical intent.

## Source of truth
- Current scope boundary: `docs/pre_driver_scope.md`
- Primary execution plan: `docs/todo.md`
- Current architecture summary: `docs/ARCHITECTURE.md`
- Repo audit vs plan: `docs/repo_todo_alignment.md`


## Current implementation boundary (April 2026)
The active build scope is intentionally capped at the pre-driver phase:
- `chemical intent -> protocol -> capability -> hardware/BOM -> layout notes -> human build manual`
- human clarification interface for build-manual questions

Deferred for later integration:
- driver generation and firmware updates
- APC orchestration execution integration
- VLM-in-the-loop driver testing/repair

See `docs/pre_driver_scope.md`.

## Current state
This repo is in scaffold phase:
- FastAPI service skeletons exist in `apps/`
- Domain package placeholders exist in `packages/`
- Initial JSON schemas/examples exist in `packages/contracts/`
- Request lineage middleware exists (`trace_id`, `run_id`, `device_id`)

Core domain functionality (protocol synthesis, layout optimization, build-manual generation, HIL repair loops, MoveIt integration) is not yet implemented.

## Repository layout
- `apps/` service entrypoints
- `packages/` domain modules and shared utilities
- `robotics/` ROS2/MoveIt integration area
- `edge-host/` edge runtime area
- `benchmarks/` test specs and topology fixtures
- `tests/` unit, integration, and hardware-in-loop tests
- `infra/` local infrastructure manifests
- `docs/` planning and architecture

## Quickstart
```bash
python -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
pytest -q
```
