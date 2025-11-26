from fastapi.testclient import TestClient
from unittest.mock import MagicMock, patch
from app.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

@patch("app.api.get_agent")
def test_chat_endpoint_success(mock_get_agent):
    mock_agent_instance = MagicMock()
    
    mock_result = MagicMock()
    mock_result.message = "A resposta é 42."
    
    mock_agent_instance.return_value = mock_result
    
    mock_get_agent.return_value = mock_agent_instance

    payload = {"message": "Qual o sentido da vida?"}
    response = client.post("/chat", json=payload)

    assert response.status_code == 200
    assert response.json() == {"response": "A resposta é 42."}
    
    mock_agent_instance.assert_called_once_with("Qual o sentido da vida?")

@patch("app.api.get_agent")
def test_chat_endpoint_internal_error(mock_get_agent):
    mock_agent_instance = MagicMock()
    mock_agent_instance.side_effect = Exception("Ollama connection failed")
    mock_get_agent.return_value = mock_agent_instance

    payload = {"message": "Erro proposital"}
    response = client.post("/chat", json=payload)

    assert response.status_code == 500
    assert "Ollama connection failed" in response.json()["detail"]

def test_chat_endpoint_validation_error():
    response = client.post("/chat", json={"msg": "Ola"})
    assert response.status_code == 422