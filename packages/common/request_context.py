from __future__ import annotations

from contextvars import ContextVar, Token
from dataclasses import dataclass
from uuid import uuid4

from fastapi import Request

TRACE_HEADER = "x-trace-id"
RUN_HEADER = "x-run-id"
DEVICE_HEADER = "x-device-id"

_trace_id_ctx: ContextVar[str | None] = ContextVar("trace_id", default=None)
_run_id_ctx: ContextVar[str | None] = ContextVar("run_id", default=None)
_device_id_ctx: ContextVar[str | None] = ContextVar("device_id", default=None)


@dataclass(frozen=True)
class RequestIDs:
    trace_id: str
    run_id: str
    device_id: str


def _new_id(prefix: str) -> str:
    return f"{prefix}_{uuid4().hex[:12]}"


def ids_from_request(request: Request) -> RequestIDs:
    trace_id = request.headers.get(TRACE_HEADER, "").strip() or _new_id("trc")
    run_id = request.headers.get(RUN_HEADER, "").strip() or _new_id("run")
    device_id = request.headers.get(DEVICE_HEADER, "").strip() or "dev_unknown"
    return RequestIDs(trace_id=trace_id, run_id=run_id, device_id=device_id)


def set_request_ids(ids: RequestIDs) -> tuple[Token[str | None], Token[str | None], Token[str | None]]:
    trace_token = _trace_id_ctx.set(ids.trace_id)
    run_token = _run_id_ctx.set(ids.run_id)
    device_token = _device_id_ctx.set(ids.device_id)
    return trace_token, run_token, device_token


def reset_request_ids(
    tokens: tuple[Token[str | None], Token[str | None], Token[str | None]],
) -> None:
    trace_token, run_token, device_token = tokens
    _trace_id_ctx.reset(trace_token)
    _run_id_ctx.reset(run_token)
    _device_id_ctx.reset(device_token)


def current_ids() -> RequestIDs:
    return RequestIDs(
        trace_id=_trace_id_ctx.get() or "",
        run_id=_run_id_ctx.get() or "",
        device_id=_device_id_ctx.get() or "",
    )
