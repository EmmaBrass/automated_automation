from __future__ import annotations

from fastapi import FastAPI, Request

from packages.common.request_context import (
    DEVICE_HEADER,
    RUN_HEADER,
    TRACE_HEADER,
    current_ids,
    ids_from_request,
    reset_request_ids,
    set_request_ids,
)


def create_service_app(service_name: str) -> FastAPI:
    app = FastAPI(title=f"automated-automation:{service_name}", version="0.1.0")

    @app.middleware("http")
    async def add_request_ids(request: Request, call_next):
        ids = ids_from_request(request)
        tokens = set_request_ids(ids)
        try:
            response = await call_next(request)
        finally:
            reset_request_ids(tokens)

        response.headers[TRACE_HEADER] = ids.trace_id
        response.headers[RUN_HEADER] = ids.run_id
        response.headers[DEVICE_HEADER] = ids.device_id
        return response

    @app.get("/health")
    def health() -> dict[str, str]:
        ids = current_ids()
        return {
            "status": "ok",
            "service": service_name,
            "trace_id": ids.trace_id,
            "run_id": ids.run_id,
            "device_id": ids.device_id,
        }

    @app.get("/ids")
    def ids() -> dict[str, str]:
        c = current_ids()
        return {"trace_id": c.trace_id, "run_id": c.run_id, "device_id": c.device_id}

    return app
