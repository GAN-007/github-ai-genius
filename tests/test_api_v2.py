from fastapi.testclient import TestClient

from github_ai_genius.api_v2 import app


def test_health_endpoint():
    client = TestClient(app)
    response = client.get('/health')
    assert response.status_code == 200
    assert response.json()['ok'] is True
