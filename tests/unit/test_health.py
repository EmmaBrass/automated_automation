from fastapi.testclient import TestClient

from apps.api.main import app


def test_health() -> None:
    client = TestClient(app)
    response = client.get("/health")
    assert response.status_code == 200

    body = response.json()
    assert body["status"] == "ok"
    assert body["service"] == "api"
    assert body["trace_id"].startswith("trc_")
    assert body["run_id"].startswith("run_")
    assert body["device_id"] == "dev_unknown"
