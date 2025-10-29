"""Módulo de teste para os endpoints de Aluno"""
import pytest

# Testes de Caminho Feliz


def test_create_aluno(client):
    """Testa a criação de um novo aluno"""
    response = client.post(
        "/Aluno/",
        json={
            "nome_aluno": "Aluno Teste Create",
            "email": "create@email.com",
            "senha": "senha123",
            "idade": 30,
            "peso_kg": 80.0,
            "altura": 1.80,
        },
    )

    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "create@email.com"
    assert data["nome_aluno"] == "Aluno Teste Create"
    assert "id_aluno" in data


def test_read_aluno_by_id(client, aluno_cadastrado):
    """Testa a leitura  de um aluno que já existe, pede o aluno_cadastrado"""

    aluno_id = aluno_cadastrado["id_aluno"]
    response = client.get(f"/Aluno/{aluno_id}")

    assert response.status_code == 200
    data = response.json()
    assert data["id_aluno"] == aluno_id
    assert data["email"] == "aluno@email.com"


def test_update_aluno(client, aluno_cadastrado):
    """Testa a atualização  de um aluno que já existe"""

    aluno_id = aluno_cadastrado["id_aluno"]

    response = client.patch(
        f"/Aluno/{aluno_id}", json={"nome_aluno": "Aluno Nome Atualizado"}
    )

    assert response.status_code == 200
    data = response.json()
    assert data["nome_aluno"] == "Aluno Nome Atualizado"
    assert data["email"] == "aluno@email.com"


def test_delete_aluno(client, aluno_cadastrado):
    """Testa o delete  de um aluno e verifica se ele sumiu"""
    aluno_id = aluno_cadastrado["id_aluno"]

    response_delete = client.delete(f"/Aluno/{aluno_id}")
    assert response_delete.status_code in [200, 204]

    response_get = client.get(f"/Aluno/{aluno_id}")
    assert response_get.status_code == 404


# Testes de Caminho Triste


def test_read_aluno_nao_encontrado(client):
    """Testa obter um aluno com id inexistente"""

    response = client.get("/Aluno/99999")
    assert response.status_code == 404


def test_update_aluno_nao_encontrado(client):
    """Testa atualizar um aluno com id inexistente"""

    response = client.patch("/Aluno/99999", json={"nome_aluno": "Nome Fantasma"})
    assert response.status_code == 404


@pytest.mark.parametrize(
    "campo_faltante, json_payload",
    [
        (
            "nome_aluno",
            {
                # "nome_aluno": "Faltando",
                "email": "teste@email.com",
                "senha": "123",
                "idade": 20,
                "peso_kg": 70,
                "altura": 1.70,
            },
        ),
        (
            "email",
            {
                "nome_aluno": "Aluno",
                # "email": "faltando@email.com",
                "senha": "123",
                "idade": 20,
                "peso_kg": 70,
                "altura": 1.70,
            },
        ),
        (
            "senha",
            {
                "nome_aluno": "Aluno",
                "email": "teste@email.com",
                # "senha": "faltando",
                "idade": 20,
                "peso_kg": 70,
                "altura": 1.70,
            },
        ),
    ],
)
def test_create_aluno_erro_422_campos_faltantes(client, campo_faltante, json_payload):
    """Testa se a API retorna erro quando um campo é passado em branco ou tem o tipo errado"""
    response = client.post("/Aluno/", json=json_payload)
    assert response.status_code == 422

    data = response.json()
    assert data["detail"][0]["type"] == "missing"
    assert data["detail"][0]["loc"] == ["body", campo_faltante]
