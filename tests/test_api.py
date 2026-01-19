from fastapi.testclient import TestClient

from api import app

def _assert_ok(response):
    assert response.status_code == 200

def _check_context(response):
    assert "request" in response.context
    assert 'api' in response.context
    assert 'app' in response.context


def test_home():
    client = TestClient(app)
    response = client.get("/")
    _assert_ok(response)
    _check_context(response)
    assert response.template.name == 'index.html'
    assert "title" in response.context

def test_posters():
    client = TestClient(app)
    response = client.get("/posters")
    _assert_ok(response)
    _check_context(response)
    assert response.template.name == 'posters.html'
    assert 'files' in response.context
