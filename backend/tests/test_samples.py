from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_list_samples_returns_three_items() -> None:
    response = client.get("/api/samples")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3


def test_list_samples_has_correct_ids() -> None:
    response = client.get("/api/samples")
    ids = {s["id"] for s in response.json()}
    assert ids == {"sample_passport", "sample_utility_bill", "sample_pay_stub"}


def test_list_samples_fields_present() -> None:
    response = client.get("/api/samples")
    for sample in response.json():
        assert "id" in sample
        assert "name" in sample
        assert "type" in sample
        assert "description" in sample
