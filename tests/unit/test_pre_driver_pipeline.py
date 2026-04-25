from fastapi.testclient import TestClient

from apps.api.main import app


def test_pre_driver_plan_and_manual_chat() -> None:
    client = TestClient(app)
    headers = {"x-trace-id": "trc_pre_driver", "x-run-id": "run_pre_driver", "x-device-id": "dev_ui"}

    create_response = client.post(
        "/v1/pre-driver/plan",
        json={
            "reaction": "synthesize paracetamol",
            "scale": "5 mmol",
            "objectives": ["purity >= 98%"],
        },
        headers=headers,
    )
    assert create_response.status_code == 200
    body = create_response.json()
    assert body["phase"] == "pre_driver"
    assert "driver_generation" in body["deferred_items"]
    assert len(body["build_manual"]) >= 1

    get_response = client.get("/v1/pre-driver/plan/run_pre_driver", headers=headers)
    assert get_response.status_code == 200
    get_body = get_response.json()
    assert get_body["run_id"] == "run_pre_driver"

    chat_response = client.post(
        "/v1/pre-driver/plan/run_pre_driver/manual-chat",
        json={"message": "I am confused about the wiring pin order", "step_id": "M2"},
        headers=headers,
    )
    assert chat_response.status_code == 200
    chat_body = chat_response.json()
    assert chat_body["status"] == "ok"
    assert chat_body["phase"] == "pre_driver_manual_assistance"
    assert len(chat_body["suggested_actions"]) >= 1
