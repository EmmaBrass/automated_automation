# Repo-to-TODO Alignment Audit

Date: April 25, 2026
Reference plan: `docs/todo.md`

## Summary
The repository is a good scaffold baseline, but most core functionality in `todo.md` is not yet implemented.
v1 architecture stance: MCP-first LLM tool interface, app-native orchestration/state, LangGraph deferred unless required by concrete durability/branching needs.

Status legend:
- `implemented`: working code exists beyond stubs.
- `partial`: foundational structure exists.
- `missing`: no meaningful implementation yet.

## Alignment Matrix

1. North-Star workflow orchestration:
- status: `partial`
- existing: service skeletons in `apps/*`, request context middleware in `packages/common/*`
- gap: no true end-to-end state machine from intent to execution.

2. Protocol synthesis from chemical intent:
- status: `missing`
- existing: contract scaffold for `chem_intent_spec`, empty `chem_planner` module.
- gap: no protocol extraction, no literature retrieval, no confidence/citation model.

3. Capability and hardware mapping:
- status: `missing`
- existing: basic `build_plan`/`procurement_plan` schemas.
- gap: no ontology, no capability compiler, no hardware mapper.

4. CAD/geometry acquisition policy:
- status: `missing`
- existing: `adapter_cad_spec` schema scaffold.
- gap: no geometry provenance workflow, no scan/manual fallback pipeline.

5. Workspace layout optimization:
- status: `missing`
- existing: none beyond placeholders.
- gap: no optimization model, constraints, solver integration, or explainability outputs.

6. Human build-manual generation:
- status: `missing`
- existing: none.
- gap: no assembly instruction schema or rendering.

7. Driver synthesis + orchestration integration:
- status: `missing`
- existing: `synthesis`/`orchestrator` app stubs, legacy `run` endpoints.
- gap: no doc retrieval, no driver generation, no execution adapter integration.

8. Robot motion and grasping (MoveIt + vision):
- status: `missing`
- existing: empty `robotics/` directory.
- gap: no MoveIt integration, no grasp/perception layer.

9. Digital twin and reality alignment:
- status: `missing`
- existing: `embodiment_graph` schema scaffold.
- gap: no twin model, no alignment checks, no drift tracking.

10. Safety and assurance:
- status: `partial`
- existing: request-ID propagation, basic middleware.
- gap: no risk tiers, no canary policy engine, no safety limit enforcement.

11. Data contracts and artifacts:
- status: `partial`
- existing: initial schemas + examples + validation test harness.
- gap: missing new contracts in `todo.md` section 11 (`protocol_step_graph`, `layout_solution`, `build_manual`, etc.).

12. Milestones and immediate actions:
- status: `missing`
- existing: no executable milestone tracking artifacts.
- gap: no task board or milestone implementation sequence in code.

## Recommended Build Start Order (Code)
1. Implement canonical typed models for:
   - `protocol_step_graph`,
   - `capability_requirements`,
   - `layout_optimization_problem`,
   - `layout_solution`,
   - `build_manual`.
2. Build `chem_planner` MVP:
   - intent parse -> protocol step graph (rule-based v0).
3. Build capability mapper MVP:
   - protocol steps -> hardware classes -> BOM stub.
4. Build layout optimizer MVP:
   - 2D/3D non-overlap + reachability heuristic first.
5. Build human manual generator MVP:
   - deterministic instruction rendering from layout output.

## Cleanup Applied
- Removed overlapping legacy planning docs that conflicted with current source-of-truth planning.
- Retained scaffold + contract baseline files required for immediate implementation.
