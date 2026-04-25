# Contract Baseline (v0)

Date: April 25, 2026
Status: Transitional baseline. Source-of-truth contract backlog is `docs/todo.md` section 11.

## Purpose
Define the minimum artifact and validation baseline currently present in the repository while the new architecture is implemented.

## Current Implemented Contract Set
Backed by JSON Schemas in `packages/contracts/schemas/` with examples in `packages/contracts/examples/`:
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

## Validation
- Example/schema validation script: `scripts/validate_contracts.py`
- Unit coverage: `tests/unit/test_contract_examples.py`

## Gap vs Target
The following required artifacts are not implemented yet (see `docs/todo.md`):
- `protocol_step_graph`
- `capability_requirements`
- `layout_optimization_problem`
- `layout_solution`
- `build_manual`
- `driver_vlm_report`
- `agent_cli_execution_report`
- `twin_alignment_report`

## Rules (Current)
- Every new contract must have:
  1. a JSON Schema,
  2. a valid example payload,
  3. validation coverage in tests.
- Backward-incompatible contract changes require version bump in schema title and changelog note.

## Related Docs
- [TODO Plan](/Users/emmabrass/Documents/Technopath/Technopath/automated-automation/docs/todo.md)
- [Architecture](/Users/emmabrass/Documents/Technopath/Technopath/automated-automation/docs/ARCHITECTURE.md)
- [Repo Alignment Audit](/Users/emmabrass/Documents/Technopath/Technopath/automated-automation/docs/repo_todo_alignment.md)

## v1 Integration Note
- LLM interactions should use MCP-exposed contracts/tools.
- LLM task execution should use coding-agent CLI commands (Codex CLI default) through a provider-swappable backend adapter.
- Workflow state transitions and execution orchestration remain in core application services for v1.
- LangGraph is an optional later enhancement if durable branching/checkpointing becomes necessary.
