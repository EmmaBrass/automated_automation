from __future__ import annotations

from typing import Literal
from uuid import uuid4

from pydantic import BaseModel, Field

from packages.common import create_service_app
from packages.common.request_context import current_ids
from packages.common.service_registry import SERVICE_NAMES

app = create_service_app("api")


class IntentRequest(BaseModel):
    reaction: str = Field(min_length=3)
    scale: str = Field(default="1 mmol")
    objectives: list[str] = Field(default_factory=list)


class BuildManualQuestion(BaseModel):
    message: str = Field(min_length=2)
    step_id: str | None = None


class BuildManualStep(BaseModel):
    step_id: str
    title: str
    instruction: str
    checks: list[str] = Field(default_factory=list)


class PreDriverPlan(BaseModel):
    run_id: str
    trace_id: str
    phase: Literal["pre_driver"] = "pre_driver"
    protocol_steps: list[str]
    capability_requirements: list[str]
    hardware_requirements: list[str]
    bom_items: list[str]
    layout_notes: list[str]
    build_manual: list[BuildManualStep]
    deferred_items: list[str]


RUN_STORE: dict[str, PreDriverPlan] = {}


def _derive_protocol_steps(intent: IntentRequest) -> list[str]:
    base = [
        f"Prepare reagents for {intent.reaction} at {intent.scale}",
        "Charge reactor and start stirring",
        "Control temperature profile",
        "Add reagents according to schedule",
        "Hold and monitor reaction completion",
        "Quench and perform workup transfer",
    ]
    if any("purity" in objective.lower() for objective in intent.objectives):
        base.append("Collect sample for purity analytics")
    return base


def _derive_capabilities(protocol_steps: list[str]) -> list[str]:
    mapping = {
        "Prepare reagents": "dispense_liquid",
        "Charge reactor": "reactor_loading",
        "stirring": "stir_control",
        "temperature": "heat_control",
        "Add reagents": "metered_addition",
        "monitor": "sensor_monitoring",
        "transfer": "robot_transfer",
        "sample": "sample_handling",
    }
    capabilities: set[str] = set()
    for step in protocol_steps:
        for token, capability in mapping.items():
            if token.lower() in step.lower():
                capabilities.add(capability)
    return sorted(capabilities)


def _hardware_for_capabilities(capabilities: list[str]) -> list[str]:
    hardware_map = {
        "dispense_liquid": "syringe_pump_module",
        "reactor_loading": "reactor_vial_station",
        "stir_control": "stirrer_hotplate",
        "heat_control": "heater_controller",
        "metered_addition": "valve_or_pump_channel",
        "sensor_monitoring": "temperature_or_camera_sensor",
        "robot_transfer": "robot_arm_with_gripper",
        "sample_handling": "sample_port_or_vial_tray",
    }
    return sorted({hardware_map[c] for c in capabilities if c in hardware_map})


def _build_manual(hardware: list[str]) -> list[BuildManualStep]:
    placement_list = ", ".join(hardware) if hardware else "required modules"
    return [
        BuildManualStep(
            step_id="M1",
            title="Place Modules",
            instruction=(
                "Place modules on the workspace board in the assigned slots from the layout output: "
                f"{placement_list}."
            ),
            checks=[
                "Each module sits flat and is mechanically secured",
                "Slot labels match the layout plan",
            ],
        ),
        BuildManualStep(
            step_id="M2",
            title="Connect Power And Data",
            instruction=(
                "Connect each module to approved power and data ports exactly as listed in the wiring table."
            ),
            checks=[
                "No unapproved cable adapters used",
                "Cable paths avoid robot workspace sweep",
            ],
        ),
        BuildManualStep(
            step_id="M3",
            title="Run Human Verification",
            instruction=(
                "Confirm each connection and placement against the visual checklist before enabling automation."
            ),
            checks=[
                "Photos captured for each module and connector",
                "All checklist items pass before continue",
            ],
        ),
    ]


def _assistant_answer(question: str, plan: PreDriverPlan, step_id: str | None) -> tuple[str, list[str]]:
    q = question.lower()
    if any(token in q for token in ["can't", "cannot", "stuck", "confused", "unclear"]):
        return (
            "Pause at the current step, mark it blocked, and request a human-approved alternate placement or connector path.",
            [
                "Attach one photo of the blocked area",
                "Describe what tool/connector is missing",
                "Request a revised instruction set",
            ],
        )
    if "pin" in q or "gpio" in q or "wire" in q:
        return (
            "Use the pin map from the wiring table and verify pin numbering orientation before power-on.",
            [
                "Check pin-1 marker on both sides",
                "Confirm voltage compatibility before connecting",
                "Record the final pin mapping in the checklist",
            ],
        )
    if "next" in q or "continue" in q:
        next_step = plan.build_manual[0].step_id if not step_id else None
        if step_id:
            ids = [s.step_id for s in plan.build_manual]
            if step_id in ids:
                idx = ids.index(step_id)
                if idx + 1 < len(ids):
                    next_step = ids[idx + 1]
        if next_step:
            return (
                f"Proceed to step {next_step} and complete all checks before moving forward.",
                ["Follow instruction text exactly", "Complete each checklist item"],
            )
    return (
        "Clarify the exact step and issue; I can provide a focused instruction rewrite for that specific build step.",
        ["Provide step ID", "Describe the mismatch", "Attach photo if available"],
    )


@app.get("/services")
def services() -> dict[str, list[str]]:
    return {"services": SERVICE_NAMES}


@app.post("/v1/pre-driver/plan", response_model=PreDriverPlan)
def create_pre_driver_plan(intent: IntentRequest) -> PreDriverPlan:
    ids = current_ids()
    run_id = ids.run_id if ids.run_id != "run_unknown" else f"run_{uuid4().hex[:10]}"
    protocol_steps = _derive_protocol_steps(intent)
    capabilities = _derive_capabilities(protocol_steps)
    hardware = _hardware_for_capabilities(capabilities)
    manual = _build_manual(hardware)

    plan = PreDriverPlan(
        run_id=run_id,
        trace_id=ids.trace_id,
        protocol_steps=protocol_steps,
        capability_requirements=capabilities,
        hardware_requirements=hardware,
        bom_items=[f"approved::{module}" for module in hardware],
        layout_notes=[
            "Place high-heat modules away from camera line-of-sight blockers",
            "Keep robot transfer corridor free of cables",
            "Reserve a safe maintenance zone at board edge",
        ],
        build_manual=manual,
        deferred_items=[
            "driver_generation",
            "device_firmware_flashing",
            "apc_orchestrator_execution",
        ],
    )
    RUN_STORE[run_id] = plan
    return plan


@app.get("/v1/pre-driver/plan/{run_id}", response_model=PreDriverPlan)
def get_pre_driver_plan(run_id: str) -> PreDriverPlan:
    if run_id not in RUN_STORE:
        return PreDriverPlan(
            run_id=run_id,
            trace_id=current_ids().trace_id,
            protocol_steps=[],
            capability_requirements=[],
            hardware_requirements=[],
            bom_items=[],
            layout_notes=[],
            build_manual=[],
            deferred_items=["plan_not_found"],
        )
    return RUN_STORE[run_id]


@app.post("/v1/pre-driver/plan/{run_id}/manual-chat")
def manual_chat(run_id: str, payload: BuildManualQuestion) -> dict[str, object]:
    ids = current_ids()
    plan = RUN_STORE.get(run_id)
    if not plan:
        return {
            "status": "error",
            "service": "api",
            "run_id": run_id,
            "trace_id": ids.trace_id,
            "message": "Plan not found. Create a pre-driver plan first.",
        }

    answer, actions = _assistant_answer(payload.message, plan, payload.step_id)
    selected_step = None
    if payload.step_id:
        selected_step = next((s.model_dump() for s in plan.build_manual if s.step_id == payload.step_id), None)

    return {
        "status": "ok",
        "service": "api",
        "run_id": run_id,
        "trace_id": ids.trace_id,
        "phase": "pre_driver_manual_assistance",
        "answer": answer,
        "suggested_actions": actions,
        "step": selected_step,
    }
