from packages.common import create_service_app
from packages.common.service_registry import SERVICE_NAMES

app = create_service_app("api")


@app.get("/services")
def services() -> dict[str, list[str]]:
    return {"services": SERVICE_NAMES}
