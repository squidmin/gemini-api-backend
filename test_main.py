from fastapi.testclient import TestClient
import pytest
from unittest.mock import Mock

from main import app


@pytest.fixture
def client():
    with TestClient(app) as client:
        yield client


@pytest.fixture
def mock_get_api_key(mocker):
    mocker.patch("main.get_api_key", return_value="mock_api_key")


def test_list_models(client):
    response = client.get("/list-models/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)  # You could add more specific checks here based on expected model names


def test_generate_text_no_api_key(mocker, client):
    mocker.patch("main.get_api_key", return_value=None)  # Simulating failed API key retrieval
    response = client.get("/generate-text/?prompt=hello world")
    assert response.status_code == 400
    assert response.json() == {"detail": "Failed to retrieve API Key."}


def test_generate_text(client, mock_get_api_key, mocker):
    # Mock the GenerativeModel and its generate_content method
    mock_model = Mock()
    mock_content = Mock(text="Generated response for 'hello world'")
    mock_model.generate_content = Mock(return_value=mock_content)
    mocker.patch("google.generativeai.GenerativeModel", return_value=mock_model)

    response = client.get("/generate-text/?prompt=hello world")
    assert response.status_code == 200
    assert response.json() == {"generated_text": "Generated response for 'hello world'"}
