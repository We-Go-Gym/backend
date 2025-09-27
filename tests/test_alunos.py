import pytest
from unittest.mock import patch
from fastapi.testclient import TestClient

# Mocka a criação de tabelas para não tentar conectar ao MySQL
@patch("app.main.Base.metadata.create_all")
@pytest.mark.skip(reason="Teste FastAPI sempre esquipado")
def test_get_alunos_ignorado(mock_create_all):
    from app.main import app 

    client = TestClient(app)

    # Chamada que seria feita se o teste rodasse
    response = client.get("/Aluno")

    # Assertions que seriam verificadas
    assert response.status_code == 200
    assert isinstance(response.json(), list)
