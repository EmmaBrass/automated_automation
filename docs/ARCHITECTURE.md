# Architecture (Current)

Primary source of truth:
- `docs/todo.md`

## System Mission
Compile chemical intent into an executable, robot-operable laboratory workflow by co-synthesizing:
- protocol steps,
- hardware selection,
- workspace layout,
- build instructions,
- driver/orchestration software,
- and closed-loop verification.

## Core Pipeline
1. `chem_intent` -> `protocol_step_graph`
2. `protocol_step_graph` -> `capability_requirements`
3. `capability_requirements` -> `hardware_requirements` + `BOM`
4. geometry acquisition + digital twin construction
5. constrained layout optimization
6. human build manual generation
7. driver synthesis + orchestration integration
8. staged VLM-in-the-loop validation + repair loops
9. full experiment execution with safety gates

## Runtime Stack
- Service architecture: FastAPI microservices.
- LLM integration: MCP-based tool/resource interface.
- LLM execution backend: coding-agent CLI runner (Codex CLI default; provider-swappable adapter).
- LLM workflow state: owned by application orchestration (not LangGraph in v1).
- Robotics planning: ROS2 + MoveIt 2 (+ Task Constructor).
- Contract validation: JSON Schema + examples.
- Trace lineage: `x-trace-id`, `x-run-id`, `x-device-id`.

## Web App and CLI Execution Model
- Browser UI does not execute CLI commands directly.
- Web app submits jobs to backend worker services.
- Worker service executes whitelisted CLI commands in controlled subprocess environments.
- All CLI runs are logged with run/trace IDs and artifactized execution reports.

## Current Repo State
- Foundation is scaffolded (services, contracts, middleware, tests).
- Domain logic for protocol synthesis, layout optimization, build-manual generation, and VLM-in-the-loop repair remains to be implemented.


## Current Build Boundary (Pre-Driver)
Implemented scope ends at the human build manual and manual-assistance interface.

In-scope pipeline for now:
1. `chem_intent` -> `protocol_step_graph`
2. `protocol_step_graph` -> `capability_requirements`
3. `capability_requirements` -> `hardware_requirements` + `BOM`
4. layout notes / placement guidance
5. human build manual generation
6. manual clarification chat interface

Deferred pipeline components:
- driver synthesis
- firmware updates
- VLM-in-the-loop driver verification
- APC execution wiring
