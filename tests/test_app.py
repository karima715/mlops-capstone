from fastapi.testclient import TestClient
from app import app

client = TestClient(app)


def test_root():
    r = client.get("/")
    assert r.status_code == 200
    assert "status" in r.json()


def test_predict_ok():
    r = client.post("/predict", json={"area": 1000})
    assert r.status_code == 200
    j = r.json()
    assert "prediction" in j
    assert isinstance(j["prediction"], (float, int))
