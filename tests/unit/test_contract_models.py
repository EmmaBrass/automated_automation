import json
from pathlib import Path

import pytest
from pydantic import ValidationError

from packages.contracts import (
    AgentCliExecutionReport,
    BuildManual,
    CapabilityRequirements,
    DriverVlmReport,
    LayoutOptimizationProblem,
    LayoutSolution,
    ProtocolStepGraph,
    TwinAlignmentReport,
)

ROOT = Path(__file__).resolve().parents[2]
EXAMPLES = ROOT / "packages" / "contracts" / "examples"

MODEL_BY_BASE = {
    "protocol_step_graph": ProtocolStepGraph,
    "capability_requirements": CapabilityRequirements,
    "layout_optimization_problem": LayoutOptimizationProblem,
    "layout_solution": LayoutSolution,
    "build_manual": BuildManual,
    "agent_cli_execution_report": AgentCliExecutionReport,
    "driver_vlm_report": DriverVlmReport,
    "twin_alignment_report": TwinAlignmentReport,
}


@pytest.mark.parametrize("base,model", sorted(MODEL_BY_BASE.items()))
def test_contract_model_accepts_example(base: str, model: type) -> None:
    payload = json.loads((EXAMPLES / f"{base}.json").read_text(encoding="utf-8"))
    obj = model.model_validate(payload)
    assert obj is not None


@pytest.mark.parametrize("base,model", sorted(MODEL_BY_BASE.items()))
def test_contract_model_rejects_invalid_payload(base: str, model: type) -> None:
    payload = json.loads((EXAMPLES / f"{base}.json").read_text(encoding="utf-8"))

    # Remove the first required field in a stable way to trigger validation failure.
    first_key = next(iter(payload))
    payload.pop(first_key)

    with pytest.raises(ValidationError):
        model.model_validate(payload)
