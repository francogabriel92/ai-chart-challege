from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

# Integration tests for the chart creation endpoint
# These tests assume that the database is seeded with initial data
# and that the LLMService and ChartService are functioning correctly.
# In a real-world scenario, we would mock these services to isolate the tests.


def test_create_chart_success():
    payload = {"question": "Show me sales by day"}
    response = client.post("/charts/create", json=payload)
    assert response.status_code == 200
    data = response.json()
    # Check that the response contains the expected keys
    assert "chart" in data
    # Optionally, check that chart is a dict and has a layout
    assert isinstance(data["chart"], dict) or data["chart"] is None


def test_create_chart_invalid_question():
    # Example payload that should fail (empty question)
    payload = {"question": ""}
    response = client.post("/charts/create", json=payload)
    assert response.status_code == 400
    # Optionally, check error message
    data = response.json()
    assert "detail" in data
    assert data["detail"] == "Question must be between 10 and 200 characters long"


def test_create_chart_no_data():
    # Example payload that should return no data
    payload = {
        "question": "Show me sales for a november 2068"  # Assuming no data for this date
    }
    response = client.post("/charts/create", json=payload)
    assert response.status_code == 404
    # Optionally, check error message
    data = response.json()
    assert "detail" in data
    assert data["detail"] == "No data found for the query"

def test_create_chart_invalid_sql():
    # Example payload that should fail due to invalid SQL generation
    payload = {"question": "Create a delete query for all sales"}
    response = client.post("/charts/create", json=payload)
    assert response.status_code == 400
    # Optionally, check error message
    data = response.json()
    assert "detail" in data
    assert data["detail"] == "No valid query generated"