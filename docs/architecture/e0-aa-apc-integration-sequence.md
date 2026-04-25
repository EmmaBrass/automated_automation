# Epic E0 AA -> APC Integration Sequence

## Driver Promotion and Binding
1. AA creates driver candidate using coding-agent CLI adapter.
2. AA runs bounded VLM-in-the-loop verification ladder.
3. AA writes `driver_promotion_contract` + artifact refs.
4. AA marks driver state `promoted` on pass.
5. APC fetches promoted contract and validates compatibility.
6. APC binds driver for workflow runtime usage.
7. If failures occur, APC/AA rollback to last known-good promoted version.

## Gate Rules
- APC must reject non-promoted or schema-incompatible drivers.
- AA must emit immutable evidence for every promotion.
