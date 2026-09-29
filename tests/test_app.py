import pytest

from app.main import app, redis_client


@pytest.fixture
def client():
    app.config["TESTING"] = True

    with app.test_client() as client:
        yield client


def test_index(client):
    response = client.get("/")

    assert response.status_code == 200

    data = response.get_json()

    assert data["message"] == "DevOps Evaluation API"
    assert data["status"] == "running"


def test_health(client):
    response = client.get("/health")

    assert response.status_code == 200

    data = response.get_json()

    assert data["status"] == "healthy"
    assert data["redis"] == "connected"


def test_counter(client):
    redis_client.delete("request_counter")

    response1 = client.get("/counter")
    response2 = client.get("/counter")

    assert response1.status_code == 200
    assert response2.status_code == 200

    data1 = response1.get_json()
    data2 = response2.get_json()

    assert data1["counter"] == 1
    assert data2["counter"] == 2