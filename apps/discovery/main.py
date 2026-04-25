from packages.common import create_service_app
from packages.common.request_context import current_ids

SERVICE_NAME = "discovery"
app = create_service_app(SERVICE_NAME)


@app.post("/run")
def run(payload: dict) -> dict[str, object]:
    ids = current_ids()
    return {
        "status": "accepted",
        "service": SERVICE_NAME,
        "trace_id": ids.trace_id,
        "run_id": ids.run_id,
        "device_id": ids.device_id,
        "received_keys": sorted(list(payload.keys())),
    }
