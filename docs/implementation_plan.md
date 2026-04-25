# Implementation Plan: Autonomous Synthesis of Robot-Operable Lab Environments

Date: April 25, 2026  
Primary spec: `docs/todo.md`  
Planning basis: current scaffold state in `docs/repo_todo_alignment.md`

## Scope Override (Current Sprint)
- Execute only pre-driver epics up to build-manual generation and human clarification UX.
- Do not implement driver generation, firmware flashing, or APC runtime integration in this sprint.

## 1. Delivery Strategy
- Build in strict dependency order.
- Ship one working vertical slice early (`intent -> protocol -> capability -> hardware -> BOM`).
- Keep all outputs contract-first (schema + example + tests) before service logic.
- Integrate robotics and VLM-in-the-loop driver validation only after planner outputs are stable.
- Use MCP for LLM-to-system tool integration; keep workflow state/orchestration in app services for v1.
- Use coding-agent CLI execution (Codex CLI default) behind a provider-swappable adapter.
- Defer LangGraph unless we hit concrete needs for durable branching/checkpointed LLM workflows.

## 2. Difficulty Scale
- `L` Low: straightforward engineering.
- `M` Medium: moderate design/implementation complexity.
- `H` High: significant algorithmic/system integration complexity.
- `VH` Very High: research-heavy, uncertainty-heavy, multi-system coupling.

## 3. Timeline Summary (Estimated)
1. Epic 0-1: 2 weeks
2. Epic 2: 2 weeks
3. Epic 3: 2 weeks
4. Epic 4: 3 weeks
5. Epic 5: 2 weeks
6. Epic 6: 2 weeks
7. Epic 7: 3 weeks
8. Epic 8: 3 weeks
9. Epic 9: 2 weeks
10. Epic 10: 2 weeks

Total: ~21 weeks (single-threaded baseline)

## 4. Ordered Epics and Tasks

## Epic 0: Program Baseline and Governance
Duration: 4 days  
Difficulty: `M`

1.0.1 Freeze v1 scope for first target reaction and acceptance criteria. (0.5 day, `M`)  
1.0.2 Define architecture decision record template and repo conventions. (0.5 day, `L`)  
1.0.2a Record ADR: MCP-first + app-native orchestration; LangGraph deferred in v1. (0.25 day, `L`)  
1.0.2b Record ADR: Codex CLI default with provider-swappable CLI adapter. (0.25 day, `L`)  
1.0.3 Create milestone board mapped to epics in this file. (0.5 day, `L`)  
1.0.4 Define estimation/risk review cadence (weekly). (0.5 day, `L`)  
1.0.5 Create verification checklist for each epic exit gate. (2 days, `M`)

Exit criteria:
- Milestones, acceptance gates, and change-control process are documented.

---

## Epic 1: Contracts and Typed Domain Models
Duration: 6 days  
Difficulty: `M`

1.1.1 Add schemas + examples for:
- `protocol_step_graph`
- `capability_requirements`
- `layout_optimization_problem`
- `layout_solution`
- `build_manual`
- `driver_vlm_report`
- `agent_cli_execution_report`
- `twin_alignment_report`
(3 days, `M`)

1.1.2 Add Python typed models for all new contracts in `packages/contracts`. (1.5 days, `M`)  
1.1.3 Extend contract validation tests for all new artifacts. (1 day, `L`)  
1.1.4 Add contract versioning policy + changelog template. (0.5 day, `L`)

Exit criteria:
- New contracts validate in CI with examples and tests passing.

---

## Epic 2: Chemical Intent -> Protocol Graph MVP
Duration: 2 weeks  
Difficulty: `H`

1.2.1 Define protocol ontology and step vocabulary. (2 days, `H`)  
1.2.2 Implement rule-based `chem_intent -> protocol_step_graph` baseline (no autonomous literature search yet). (4 days, `H`)  
1.2.3 Add confidence scoring and uncertainty escalation hooks. (2 days, `M`)  
1.2.4 Implement citation/reference slots in protocol outputs for future retrieval integration. (1 day, `M`)  
1.2.5 Add tests with 2-3 benchmark reaction intents (including paracetamol). (1 day, `M`)

Exit criteria:
- Deterministic protocol graph generated for target intents with confidence metadata.

---

## Epic 3: Capability Mapping and Hardware/BOM Planning
Duration: 2 weeks  
Difficulty: `H`

1.3.1 Implement `protocol_step_graph -> capability_requirements`. (3 days, `H`)  
1.3.2 Define approved hardware metadata schema (interfaces, limits, CAD presence, ports/cabling). (2 days, `M`)  
1.3.3 Implement `capability_requirements -> hardware_requirements`. (3 days, `H`)  
1.3.4 Implement constrained BOM generator (approved inventory + approved suppliers only). (1.5 days, `M`)  
1.3.5 Add BOM explainability output (why each module was selected). (0.5 day, `M`)

Exit criteria:
- For target protocol, system emits hardware plan + constrained BOM + rationale.

---

## Epic 4: Geometry Provenance and Device Modeling Pipeline
Duration: 3 weeks  
Difficulty: `VH`

1.4.1 Build device geometry provenance model (source CAD / scan / manual envelope). (2 days, `M`)  
1.4.2 Implement CAD ingestion validator (ports, envelopes, mounting points, cable exits). (3 days, `H`)  
1.4.3 Implement manual-dimensions fallback template + ingestion pipeline. (2 days, `M`)  
1.4.4 Implement 3D-scan ingest path (v1 basic) and mesh QA checks. (5 days, `VH`)  
1.4.5 Add geometry confidence scoring and escalation to human review. (2 days, `H`)  
1.4.6 Add contract outputs for geometry acquisition evidence. (1 day, `M`)

Exit criteria:
- Every BOM device has usable geometry with explicit provenance/confidence.

---

## Epic 5: Layout Optimization Engine (Mathematical Core)
Duration: 2 weeks  
Difficulty: `VH`

1.5.1 Formalize optimization variables and constraints in code. (2 days, `H`)  
1.5.2 Implement first solver pass: non-overlap + workspace bounds + cable-length constraints. (3 days, `VH`)  
1.5.3 Add robot reachability and collision-feasibility scoring (coarse). (3 days, `VH`)  
1.5.4 Implement weighted objective and deterministic seed behavior. (1 day, `H`)  
1.5.5 Emit explainable failure diagnostics for unsolved layouts. (1 day, `M`)

Exit criteria:
- Solver returns feasible layout or explicit reasoned rejection for target scenario.

---

## Epic 6: Build Manual Generation and Human Assembly Validation
Duration: 2 weeks  
Difficulty: `H`

1.6.1 Define `build_manual` schema for placement, wiring, and pin-level instructions. (1 day, `M`)  
1.6.2 Generate deterministic step-by-step build instructions from `layout_solution`. (3 days, `H`)  
1.6.3 Implement pin-mapping instruction generation (e.g., Raspberry Pi GPIO callouts). (2 days, `H`)  
1.6.4 Generate visual callouts from digital twin snapshots. (2 days, `H`)  
1.6.5 Implement post-step verification checklist prompts for human assembly. (1 day, `M`)  
1.6.6 Add assembly validation report artifact. (1 day, `M`)

Exit criteria:
- Human can assemble a valid setup solely from generated instructions.

---

## Epic 7: Driver Synthesis + VLM-in-the-Loop Validation/Repair
Duration: 3 weeks  
Difficulty: `VH`

1.7.1 Build technical documentation retrieval and parsing pipeline for selected hardware. (3 days, `H`)  
1.7.2 Generate first-pass driver skeletons using coding-agent CLI tasks with command schemas and hard safety limits. (3 days, `VH`)  
1.7.3 Integrate with orchestration backend for staged execution via MCP-exposed tools/contracts. (2 days, `H`)  
1.7.4 Implement bounded driver-test command ladder (safe primitive tests first). (2 days, `H`)  
1.7.5 Implement sensor/VLM physical-effect checks and mismatch classifier. (4 days, `VH`)  
1.7.6 Implement automatic repair proposals + re-test loop. (3 days, `VH`)  
1.7.7 Emit `driver_vlm_report`, `agent_cli_execution_report`, and repair lineage artifacts. (1 day, `M`)

Exit criteria:
- Drivers can be generated, validated, and repaired through bounded physical tests.

---

## Epic 8: MoveIt + Runtime Grasping Stack
Duration: 3 weeks  
Difficulty: `VH`

1.8.1 Integrate ROS2 + MoveIt 2 + Task Constructor baseline planning pipeline. (4 days, `VH`)  
1.8.2 Load digital twin geometry into planning scene and verify collision models. (2 days, `H`)  
1.8.3 Implement runtime visual pose correction before grasp/place. (3 days, `VH`)  
1.8.4 Implement v1 deterministic grasp templates + guarded motions. (3 days, `H`)  
1.8.5 Implement local replanning from corrected keyframes. (2 days, `VH`)  
1.8.6 Add grasp KPIs (success, regrasp rate, placement error). (1 day, `M`)

Exit criteria:
- Robot can execute planned transfer steps with runtime pose correction and measurable reliability.

---

## Epic 9: Digital Twin Alignment and Safety Runtime
Duration: 2 weeks  
Difficulty: `H`

1.9.1 Implement twin-to-reality alignment checks pre-run. (2 days, `H`)  
1.9.2 Implement drift estimator and recalibration triggers. (2 days, `H`)  
1.9.3 Implement risk-tiered execution gates and canary policy. (2 days, `H`)  
1.9.4 Implement global hard-limit enforcement (motion/temp/flow/etc.). (2 days, `H`)  
1.9.5 Implement safety halt + rollback integration across services. (2 days, `H`)

Exit criteria:
- Runtime enforces safety gates and handles drift/failure with controlled rollback.

---

## Epic 10: End-to-End Campaign and Reporting
Duration: 2 weeks  
Difficulty: `H`

1.10.1 Run full dry-runs from intent to build manual outputs. (2 days, `M`)  
1.10.2 Run integrated VLM-in-the-loop driver validation campaign for selected hardware set. (3 days, `H`)  
1.10.3 Execute target automated experiment campaign with safety-gated operation. (3 days, `H`)  
1.10.4 Produce report pack:
- success/failure summary,
- solver outcomes,
- driver repair outcomes,
- robot KPI outcomes,
- safety events and mitigations.
(2 days, `M`)

Exit criteria:
- One complete validated vertical demonstration for target intent.

## 5. Critical Path
Epic 1 -> Epic 2 -> Epic 3 -> Epic 4 -> Epic 5 -> Epic 6 -> Epic 7 -> Epic 8 -> Epic 9 -> Epic 10

## 6. Highest-Risk Areas
1. Geometry acquisition quality and scan-to-model reliability.
2. Layout optimization with realistic robot/cable constraints.
3. Driver synthesis correctness under sparse/ambiguous hardware docs.
4. Vision-in-the-loop physical-effect validation robustness.
5. MoveIt + runtime perception correction integration stability.

## 7. Recommended First Build Sprint (Next 10 working days)
1. Complete Epic 1 fully.
2. Deliver Epic 2 MVP for paracetamol intent.
3. Start Epic 3 with hardware metadata schema + capability mapper baseline.
