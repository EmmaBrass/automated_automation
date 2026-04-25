from fastapi.testclient import TestClient

from apps.api.main import app


def test_request_ids_are_generated() -> None:
    client = TestClient(app)
    response = client.get("/ids")
    assert response.status_code == 200

    body = response.json()
    assert body["trace_id"].startswith("trc_")
    assert body["run_id"].startswith("run_")
    assert body["device_id"] == "dev_unknown"

    assert response.headers["x-trace-id"] == body["trace_id"]
    assert response.headers["x-run-id"] == body["run_id"]
    assert response.headers["x-device-id"] == body["device_id"]


def test_request_ids_are_propagated_from_headers() -> None:
    client = TestClient(app)
    headers = {
        "x-trace-id": "trc_test_123",
        "x-run-id": "run_test_123",
        "x-device-id": "dev_test_123",
    }
    response = client.get("/ids", headers=headers)
    assert response.status_code == 200
    assert response.json() == {
        "trace_id": "trc_test_123",
        "run_id": "run_test_123",
        "device_id": "dev_test_123",
    }
