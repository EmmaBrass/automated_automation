from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


class ProtocolStep(BaseModel):
    step_id: str
    operation: str
    inputs: list[str] = Field(default_factory=list)
    outputs: list[str] = Field(default_factory=list)
    controls: dict[str, object] = Field(default_factory=dict)


class ProtocolStepGraph(BaseModel):
    protocol_id: str
    intent_id: str
    confidence: float = Field(ge=0, le=1)
    citations: list[str] = Field(default_factory=list)
    steps: list[ProtocolStep]


class CapabilityRequirement(BaseModel):
    capability_id: str
    capability_type: str
    required: bool
    constraints: dict[str, object] = Field(default_factory=dict)


class CapabilityRequirements(BaseModel):
    requirements_id: str
    protocol_id: str
    capabilities: list[CapabilityRequirement]


class DeviceSize(BaseModel):
    x_m: float = Field(gt=0)
    y_m: float = Field(gt=0)
    z_m: float = Field(gt=0)


class LayoutDevice(BaseModel):
    device_id: str
    size: DeviceSize


class WorkspaceBounds(BaseModel):
    width_m: float = Field(gt=0)
    depth_m: float = Field(gt=0)
    height_m: float = Field(gt=0)


class ObjectiveWeights(BaseModel):
    reachability: float = Field(ge=0)
    cable_safety: float = Field(ge=0)
    path_efficiency: float = Field(ge=0)
    maintainability: float = Field(ge=0)


class LayoutOptimizationProblem(BaseModel):
    problem_id: str
    run_id: str
    workspace: WorkspaceBounds
    devices: list[LayoutDevice]
    hard_constraints: list[str] = Field(default_factory=list)
    objective_weights: ObjectiveWeights


class DevicePose(BaseModel):
    x_m: float
    y_m: float
    z_m: float
    yaw_deg: float


class PlacementEntry(BaseModel):
    device_id: str
    pose: DevicePose


class LayoutSolution(BaseModel):
    solution_id: str
    problem_id: str
    status: Literal["feasible", "infeasible"]
    placements: list[PlacementEntry]
    objective_score: float | None = None
    rejection_reasons: list[str] = Field(default_factory=list)


class BuildManualStep(BaseModel):
    step_id: str
    title: str
    instruction: str
    checks: list[str] = Field(default_factory=list)


class BuildManual(BaseModel):
    manual_id: str
    run_id: str
    steps: list[BuildManualStep]


class AgentCliExecutionReport(BaseModel):
    execution_id: str
    provider: Literal["codex", "claude", "other"]
    task_type: str
    status: Literal["queued", "running", "succeeded", "failed", "timed_out", "canceled"]
    trace_id: str
    run_id: str
    command_profile: str | None = None
    workspace_ref: str | None = None
    started_at_utc: datetime
    ended_at_utc: datetime | None = None
    artifact_refs: list[str] = Field(default_factory=list)


class DriverVlmCheck(BaseModel):
    check_id: str
    command: str
    result: Literal["pass", "fail"]
    observation: str | None = None


class DriverVlmReport(BaseModel):
    report_id: str
    run_id: str
    device_type: str
    status: Literal["pass", "fail", "needs_repair"]
    checks: list[DriverVlmCheck]
    repair_actions: list[str] = Field(default_factory=list)


class DivergenceMetrics(BaseModel):
    pose_rmse_mm: float = Field(ge=0)
    max_deviation_mm: float = Field(ge=0)


class TwinAlignmentReport(BaseModel):
    report_id: str
    run_id: str
    alignment_status: Literal["aligned", "drift_detected"]
    divergence_metrics: DivergenceMetrics | None = None
    recalibration_required: bool | None = None
    checked_at_utc: datetime
