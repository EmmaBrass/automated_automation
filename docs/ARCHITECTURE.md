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
8. staged HIL validation + repair loops
9. full experiment execution with safety gates

## Runtime Stack
- Service architecture: FastAPI microservices.
- Robotics planning: ROS2 + MoveIt 2 (+ Task Constructor).
- Contract validation: JSON Schema + examples.
- Trace lineage: `x-trace-id`, `x-run-id`, `x-device-id`.

## Current Repo State
- Foundation is scaffolded (services, contracts, middleware, tests).
- Domain logic for protocol synthesis, layout optimization, build-manual generation, and HIL repair remains to be implemented.
