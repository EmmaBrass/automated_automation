# Repository Conventions

Date: April 25, 2026

## Documentation Conventions
- `docs/todo.md` is the primary product-plan source.
- `docs/implementation_plan.md` tracks ordered execution tasks and completion status.
- `docs/ARCHITECTURE.md` records current architecture summary.
- `docs/change_control.md` governs architecture/scope change process.
- ADRs live in `docs/adr/` and follow `ADR_TEMPLATE.md`.

## Contract Conventions
- All contract schemas live in `packages/contracts/schemas`.
- Each schema must have a matching example in `packages/contracts/examples`.
- Each schema must declare `x-contract-version` in SemVer format.
- Each schema must have a matching changelog file in `packages/contracts/changelog`.
- Contract changes must be validated with `scripts/validate_contracts.py`.

## Testing Conventions
- Unit tests in `tests/unit`.
- Integration tests in `tests/integration`.
- Hardware-in-loop tests in `tests/hardware_in_loop`.

## Traceability Conventions
- Propagate `x-trace-id`, `x-run-id`, `x-device-id` for API/service flows.
- Include run/trace linkage in generated artifacts and reports.

## Change Conventions
- Major architecture/scope changes require ADR updates.
- Keep docs and implementation changes in the same PR whenever possible.
