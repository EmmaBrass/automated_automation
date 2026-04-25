from importlib import import_module

import pytest
from fastapi.testclient import TestClient

from packages.common.service_registry import SERVICE_NAMES


@pytest.mark.parametrize("service_name", SERVICE_NAMES)
def test_service_run_endpoint(service_name: str) -> None:
    module = import_module(f"apps.{service_name}.main")
    client = TestClient(module.app)

    headers = {
        "x-trace-id": "trc_test",
        "x-run-id": "run_test",
        "x-device-id": "dev_test",
    }
    response = client.post("/run", json={"foo": 1, "bar": 2}, headers=headers)
    assert response.status_code == 200

    body = response.json()
    assert body["status"] == "accepted"
    assert body["service"] == service_name
    assert body["trace_id"] == "trc_test"
    assert body["run_id"] == "run_test"
    assert body["device_id"] == "dev_test"
    assert body["received_keys"] == ["bar", "foo"]
