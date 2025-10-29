"""Módulo de teste para os endpoints de Imc"""
# pylint: disable=unused-argument

# Testes de Caminho Feliz


def test_create_imc_e_calculo(client, aluno_cadastrado):
    """Testa cálculo do imc associado a um aluno existente"""

    aluno_id = aluno_cadastrado["id_aluno"]

    response = client.post("/Imc/", json={"id_aluno": aluno_id})

    assert response.status_code == 201
    data = response.json()

    assert data["valor_imc"] == 24.49
    assert data["id_aluno"] == aluno_id


def test_read_imc_by_id(client, imc_cadastrado):
    """Testa a leitura  de um IMC que já existe"""

    imc_id = imc_cadastrado["imc"]["id_imc"]
    response = client.get(f"/Imc/{imc_id}")

    assert response.status_code == 200
    data = response.json()
    assert data["id_imc"] == imc_id
    assert data["valor_imc"] == 24.49


def test_read_imc_list(client, imc_cadastrado):
    """
    Testa a leitura de todos os IMCs"""

    response = client.get("/Imc/")

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert data[0]["valor_imc"] == 24.49


def test_delete_imc(client, imc_cadastrado):
    """Testa o delete de um IMC"""

    imc_id = imc_cadastrado["imc"]["id_imc"]

    response_delete = client.delete(f"/Imc/{imc_id}")
    assert response_delete.status_code == 204

    response_get = client.get(f"/Imc/{imc_id}")
    assert response_get.status_code == 404


# Testes de Caminho Triste


def test_read_imc_nao_encontrado(client):
    """Testa obter um imc com id inexistente"""

    response = client.get("/Imc/99999")
    assert response.status_code == 404


def test_delete_imc_nao_encontrado(client):
    """Testa o delete  de um imc com id inexistente"""
    response = client.delete("/Imc/99999")
    assert response.status_code == 404


def test_create_imc_erro_aluno_inexistente(client):
    """Testa criar um imcpara um id_aluno que não existe"""

    response = client.post("/Imc/", json={"id_aluno": 99999})
    assert response.status_code == 404
    assert "Aluno com id 99999 não encontrado" in response.json()["detail"]


def test_create_imc_erro_aluno_com_altura_zero(client):
    """Testa criar um imc para um aluno que tem altura 0"""

    response_aluno = client.post(
        "/Aluno/",
        json={
            "nome_aluno": "Aluno Altura Zero",
            "email": "zero@email.com",
            "senha": "123",
            "idade": 20,
            "peso_kg": 70,
            "altura": 0.0,
        },
    )
    assert response_aluno.status_code == 201
    aluno_invalido_id = response_aluno.json()["id_aluno"]

    response_imc = client.post("/Imc/", json={"id_aluno": aluno_invalido_id})

    assert response_imc.status_code == 400
    assert "Altura do aluno não pode ser zero" in response_imc.json()["detail"]
