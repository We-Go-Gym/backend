"""Módulo de teste para os endpoints de Exercicio"""

import pytest

# Testes de Caminho Feliz


def test_create_exercicio(client):
    """Testa a criação de um novo exercicio"""
    response = client.post(
        "/Exercicio/",
        json={
            "nome_exercicio": "Agachamento Livre",
            "descricao_exercicio": "Agachar com a barra nas costas.",
            "num_repeticoes": 12,
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["nome_exercicio"] == "Agachamento Livre"
    assert data["num_repeticoes"] == 12


def test_read_exercicio_by_id(client, exercicio_cadastrado):
    """Testa a leitura de um exercício que já existe"""

    exercicio_id = exercicio_cadastrado["id_exercicio"]

    response = client.get(f"/Exercicio/{exercicio_id}")

    assert response.status_code == 200
    data = response.json()
    assert data["id_exercicio"] == exercicio_id
    assert data["nome_exercicio"] == "Supino Reto "


def test_update_exercicio_put(client, exercicio_cadastrado):
    """Testa a atualização  de um exercício que já existe"""

    exercicio_id = exercicio_cadastrado["id_exercicio"]

    json_completo_para_put = {
        "nome_exercicio": "Supino Reto ",
        "descricao_exercicio": "Exercício para peito no banco reto.",
        "num_repeticoes": 15,
    }

    response = client.put(f"/Exercicio/{exercicio_id}", json=json_completo_para_put)

    assert response.status_code == 200
    data = response.json()
    assert data["num_repeticoes"] == 15
    assert data["nome_exercicio"] == "Supino Reto "


def test_delete_exercicio(client, exercicio_cadastrado):
    """Testa o delete de um exercício"""

    exercicio_id = exercicio_cadastrado["id_exercicio"]

    response_delete = client.delete(f"/Exercicio/{exercicio_id}")
    assert response_delete.status_code == 204

    response_get = client.get(f"/Exercicio/{exercicio_id}")
    assert response_get.status_code == 404


# Testes de Caminho Triste


def test_read_exercicio_nao_encontrado(client):
    """Testa se o get para um id inexistente retorna erro"""
    response = client.get("/Exercicio/99999")
    assert response.status_code == 404
    assert "não encontrado" in response.json()["detail"]


@pytest.mark.parametrize(
    "json_invalido, campo_faltante",
    [
        (
            {
                # "nome_exercicio": "Faltando",
                "descricao_exercicio": "Desc",
                "num_repeticoes": 10,
            },
            "nome_exercicio",
        ),
        (
            {
                "nome_exercicio": "Teste",
                # "descricao_exercicio": "Faltando",
                "num_repeticoes": 10,
            },
            "descricao_exercicio",
        ),
        (
            {
                "nome_exercicio": "Teste",
                "descricao_exercicio": "Desc",
                "num_repeticoes": "dez",
            },
            "num_repeticoes",
        ),
    ],
)
def test_create_exercicio_erro_422(client, json_invalido, campo_faltante):
    """Testa se a API retorna erro quando um campo é passado em branco ou tem o tipo errado"""
    response = client.post("/Exercicio/", json=json_invalido)

    assert response.status_code == 422
    data = response.json()
    assert campo_faltante in data["detail"][0]["loc"]
