from fastapi.testclient import TestClient

from github_ai_genius.api_v2 import app


def test_health_endpoint():
    client = TestClient(app)
    response = client.get('/health')
    assert response.status_code == 200
    assert response.json()['ok'] is True
    assert response.json()['version'] == '1.1.0'


def test_repo_request_requires_non_empty_repository():
    client = TestClient(app)
    response = client.post('/repo/analyze', json={'repository': ''})
    assert response.status_code == 422


def test_score_endpoint_exists_and_validates_payload():
    client = TestClient(app)
    response = client.post('/repo/score', json={'repository': ''})
    assert response.status_code == 422
