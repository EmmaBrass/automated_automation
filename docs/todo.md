# TODO: Autonomous Synthesis of Robot-Operable Laboratory Environments from Chemical Intent

Date: April 25, 2026
Status: New primary execution plan (supersedes earlier v1 framing where they conflict)

## 0. LLM Architecture Stance (v1 Lock)
- [ ] Use MCP as the tool/resource interface layer for LLM interaction with system capabilities.
- [ ] Keep workflow orchestration/state in the core application backend (service state machine + DB + event bus), not in LangGraph.
- [ ] Start with one general-purpose LLM worker/client plus optional specialist helpers only when needed.
- [ ] Defer LangGraph to post-v1 unless we hit concrete requirements for durable branching/checkpointed LLM workflow execution.

## 1. North-Star Workflow (End-to-End)
1. Human enters chemical intent (example: synthesize paracetamol, target scale, purity/analytics requirements).
2. System translates intent into an executable protocol step graph.
3. System maps protocol steps to required capabilities (heat, stir, dose liquid/solid, transfer, sample, analyze).
4. System maps required capabilities to concrete hardware modules and control/software requirements.
5. System generates BOM from:
   - owned approved inventory, and/or
   - approved suppliers with machine-readable specs + CAD.
6. System builds a digital twin of the candidate workspace.
7. System solves layout optimization (geometry, cabling, robot accessibility, task flow).
8. System generates a human build manual (IKEA-style) for exact placement + wiring + pin-level connections.
9. Human assembles exactly as specified.
10. System generates/adapts drivers and orchestration workflow.
11. System runs staged validation (software logs + sensor/video feedback).
12. System repairs code/configuration until verification criteria pass.
13. System executes full automated experiment with safety gates.

## 2. Protocol Synthesis from Chemical Intent
- [ ] Define protocol source strategy (hybrid recommended):
  - curated internal protocol library,
  - literature retrieval and extraction,
  - optional human-confirmed protocol selection when uncertainty is high.
- [ ] Implement `chem_intent -> protocol_step_graph` with confidence + citations.
- [ ] Capture process envelope: temperatures, times, stoichiometry, addition rates, hold/mix constraints, sampling points, QC checkpoints.
- [ ] Define uncertainty/escalation rule: when protocol confidence is below threshold, require human approval.
- [ ] Find and evaluate Princeton/Nature-style precedent systems for intent-to-protocol translation and include in related-work notes.

## 3. Capability and Hardware Mapping
- [ ] Implement `protocol_step_graph -> capability_requirements` compiler.
- [ ] Implement `capability_requirements -> hardware_requirements` mapper with scale/range constraints.
- [ ] Define approved hardware schema:
  - functional capabilities,
  - control interfaces,
  - power/data ports,
  - calibration requirements,
  - physical envelope + CAD metadata.
- [ ] Build BOM generator with two constrained sources only:
  - approved in-lab inventory,
  - approved suppliers exposing CAD + interface specs.

## 4. CAD, Geometry, and Dimension Acquisition Policy
- [ ] Enforce geometry provenance for every device in BOM:
  - source CAD (preferred),
  - scanned CAD (fallback),
  - manually measured geometric envelope (last-resort v1 fallback).
- [ ] Define CAD completeness checks (ports, clearances, mounting points, cable exits).
- [ ] Implement 3D scanning intake path for owned devices lacking CAD.
- [ ] Define scan-to-model QA metrics (dimensional error thresholds, alignment confidence).
- [ ] Keep human measurement fallback path for v1 continuity when scan pipeline is unavailable.

## 5. Workspace Layout Optimization (Core Mathematical Layer)
- [ ] Formalize optimization variables:
  - device poses,
  - cable routing assignments,
  - robot interaction waypoints,
  - service/maintenance clearances.
- [ ] Formalize constraints:
  - no 3D overlap,
  - workspace boundary containment,
  - cable length + bend constraints,
  - port accessibility,
  - robot reachability and collision-free approach paths,
  - required robot transfer paths between workflow-critical devices.
- [ ] Formalize objective function (weighted multi-objective):
  - maximize robot task feasibility,
  - minimize cable complexity/risk,
  - minimize transfer path length/time,
  - maximize safety clearances,
  - maximize maintainability.
- [ ] Implement solver pipeline and deterministic reproducibility for same inputs.
- [ ] Emit explainable constraint report for rejected layouts.

## 6. Human Build Manual Generation
- [ ] Generate stepwise assembly instructions from solved layout:
  - exact placement coordinates/orientation,
  - mounting steps,
  - cable connections,
  - pin-level wiring instructions (example: Raspberry Pi GPIO mapping),
  - validation checkpoints per build step.
- [ ] Add visual artifacts: annotated snapshots from digital twin + callouts.
- [ ] Add automatic assembly verification prompts (camera checks after each major step).

## 7. Driver Synthesis and Orchestration Integration
- [ ] Integrate with existing orchestration engine as execution backend.
- [ ] Implement documentation retrieval pipeline for each selected hardware module.
- [ ] Generate first-pass drivers with strict command schema + safety limits.
- [ ] Build HIL validation harness:
  - send bounded test commands,
  - verify observed physical effect via sensors/VLM,
  - classify mismatch,
  - patch driver/configuration.
- [ ] Enforce staged command ramp-up (safe primitives first, then complex actions).

## 8. Robot Motion and Grasping Stack (MoveIt + Vision)
- [ ] Lock baseline stack:
  - ROS2 + MoveIt 2 for planning/collision checking,
  - MoveIt Task Constructor for multi-step manipulation tasks,
  - digital-twin-derived nominal keyframes.
- [ ] Add perception correction layer at runtime:
  - visual pose update before grasp/placement,
  - local replanning from corrected pose.
- [ ] Recommended v1 grasping strategy (highest reliability first):
  - constrained fixtures + standardized grasp zones where possible,
  - fiducials or known geometry for robust pose correction,
  - guarded motions with force/torque thresholds.
- [ ] Recommended v2 strategy (more general grasping):
  - depth-based 6D pose + learned grasp proposal,
  - confidence gating + fallback to deterministic grasp templates.
- [ ] Define grasp quality metrics:
  - grasp success rate,
  - regrasp frequency,
  - placement error,
  - recovery success after perception drift.

## 9. Digital Twin and Reality Alignment
- [ ] Build unified world model containing:
  - workspace geometry,
  - device geometry,
  - cable routes,
  - robot model/kinematics.
- [ ] Implement twin-to-reality alignment checks before execution.
- [ ] Maintain runtime state estimator to update object/device pose drift.
- [ ] Log twin divergence metrics and trigger recalibration when thresholds are exceeded.

## 10. Safety and Assurance
- [ ] Define action risk tiers and permission gates.
- [ ] Require canary validation before full workflow execution.
- [ ] Add hard limits for movement, temperature, pressure, flow, and dosage.
- [ ] Implement emergency stop and rollback semantics across all services.
- [ ] Add immutable trace lineage (`trace_id`, `run_id`, `device_id`) for every action.

## 11. Data Contracts and Artifacts (Extend Existing Schemas)
- [ ] Add/extend artifacts:
  - `protocol_step_graph.json`,
  - `capability_requirements.json`,
  - `layout_optimization_problem.json`,
  - `layout_solution.json`,
  - `build_manual.json` + rendered instruction package,
  - `driver_hil_report.json`,
  - `twin_alignment_report.json`.
- [ ] Version all artifacts and require validation in CI.

## 12. Milestones
- [ ] M0: Intent -> protocol -> capability compiler (offline).
- [ ] M1: Capability -> hardware -> BOM with CAD/geometry provenance checks.
- [ ] M2: Layout optimizer + explainable solver output.
- [ ] M3: Human build manual generation + assembly verification loop.
- [ ] M4: Driver synthesis + bounded HIL validation loop.
- [ ] M5: MoveIt-driven experiment execution with visual correction and grasping.
- [ ] M6: End-to-end paracetamol demonstration with QC endpoint reporting.

## 13. Immediate Next Actions (This Week)
- [ ] Write ADR: `MCP-first, app-native orchestration, LangGraph deferred`.
- [ ] Freeze problem statement and success metrics for first target reaction.
- [ ] Define protocol and capability ontology (v0).
- [ ] Draft layout optimization mathematical formulation (variables/constraints/objective).
- [ ] Define build-manual schema and rendering format.
- [ ] Define driver HIL test ladder and safety envelope for first 2-3 devices.
- [ ] Select and benchmark v1 grasp pipeline (deterministic + visual correction).

## 14. Literature Seeds to Integrate
- [ ] Verify the exact Princeton paper you referenced and map its method into the protocol synthesis module.
- [ ] Read and extract implementation-relevant details from:
  - Ruan et al., *An automatic end-to-end chemical synthesis development platform powered by large language models* (Nature Communications, 2024): https://doi.org/10.1038/s41467-024-54457-x
  - Vaucher et al., *Inferring experimental procedures from text-based representations of chemical reactions* (Nature Communications, 2021): https://doi.org/10.1038/s41467-021-22951-1
  - *Collective intelligence for AI-assisted chemical synthesis* (Nature, 2026): https://doi.org/10.1038/s41586-026-10131-4
- [ ] Build a comparison table: inputs, outputs, protocol representation, hardware integration depth, autonomy level, and failure modes.
