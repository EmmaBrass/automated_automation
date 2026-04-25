# Contract Baseline (v1)

Date: April 25, 2026
Status: Active baseline for Epic 1 contract foundation.

## Purpose
Define the canonical contract surface and validation rules currently implemented in the repository.

## Current Canonical Contract Set
Backed by JSON Schemas in `packages/contracts/schemas/` with examples in `packages/contracts/examples/`:
- `protocol_step_graph`
- `capability_requirements`
- `layout_optimization_problem`
- `layout_solution`
- `build_manual`
- `driver_vlm_report`
- `agent_cli_execution_report`
- `twin_alignment_report`

Additional baseline contracts retained for adjacent integration work:
- `chem_intent_spec`
- `build_plan`
- `procurement_plan`
- `device_record`
- `embodiment_graph`
- `placement_ledger`
- `interop_gap_report`
- `adapter_cad_spec`
- `episode_report`
- `runtime_context`
- `artifact_ref`
- `sync_event_envelope`
- `driver_promotion_contract`
- `orchestration_binding_contract`

## Validation and Policy Enforcement
- Contract validation and policy checks: `scripts/validate_contracts.py`
- Unit coverage: `tests/unit/test_contract_examples.py`, `tests/unit/test_contract_models.py`, `tests/unit/test_contract_policy.py`
- Enforced rules:
  1. every schema has a matching example,
  2. every example has a matching schema,
  3. every schema validates its example,
  4. every schema declares `x-contract-version` in SemVer,
  5. every schema has a corresponding changelog entry for its current version.

## Versioning Rules
- Breaking schema change: MAJOR bump.
- Backward-compatible field/constraint expansion: MINOR bump.
- Docs/example-only or non-behavioral schema clarification: PATCH bump.
- Per-schema changelogs live in `packages/contracts/changelog/`.
- Template for new contract changelogs: `packages/contracts/changelog/TEMPLATE.md`.

## Related Docs
- [TODO Plan](/Users/emmabrass/Documents/Technopath/Technopath/automated-automation/docs/todo.md)
- [Implementation Plan](/Users/emmabrass/Documents/Technopath/Technopath/automated-automation/docs/implementation_plan.md)
- [Architecture](/Users/emmabrass/Documents/Technopath/Technopath/automated-automation/docs/ARCHITECTURE.md)

## v1 Integration Note
- LLM interactions should use MCP-exposed contracts/tools.
- LLM task execution should use coding-agent CLI commands (Codex CLI default) through a provider-swappable backend adapter.
- Workflow state transitions and execution orchestration remain in core application services for v1.
