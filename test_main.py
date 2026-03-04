from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_search_api_format():
    response = client.get("/api/search?q=test")
    assert response.status_code == 200
    data = response.json()
    assert "query" in data
    assert "results" in data
    assert isinstance(data["results"], list)