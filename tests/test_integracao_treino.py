import pytest

# Testes de Caminho Feliz

def test_create_treino(client, aluno_cadastrado):
    """Testa a criação de um novo treino associado a um aluno existente"""

    aluno_id = aluno_cadastrado["id_aluno"]
    
    response = client.post(
        "/Treino/",
        json={
            "nome_treino": "Treino A - Peito",
            "id_aluno": aluno_id,
            "descricao_treino": "Foco em hipertrofia",
            "categoria": "Peito",
            "num_series": 4
        }
    )
    
    assert response.status_code == 201
    data = response.json()
    assert data["nome_treino"] == "Treino A - Peito"
    assert data["id_aluno"] == aluno_id
    assert data["categoria"] == "Peito"


def test_read_treino_by_id(client, treino_cadastrado):
    """ Testa a leitura de um treino que já existe, precisa de treino_cadastrado
    """

    treino_id = treino_cadastrado["treino"]["id_treino"]
    response = client.get(f"/Treino/{treino_id}")
    
    assert response.status_code == 200
    data = response.json()
    assert data["id_treino"] == treino_id
    assert data["nome_treino"] == "Treino Fixture"


def test_update_treino(client, treino_cadastrado):
    """Testa a atualização  de um treino que já existe"""

    treino_id = treino_cadastrado["treino"]["id_treino"]
    
    json_completo = {
        "nome_treino": "Treino ", 
        "id_aluno": treino_cadastrado["aluno"]["id_aluno"], 
        "descricao_treino": "Treino de teste criado por fixture", 
        "num_series": 3,
        "categoria": "Peito e Tríceps ATUALIZADO" 
    }

    response = client.put( 
        f"/Treino/{treino_id}",
        json=json_completo 
    )
    
    assert response.status_code == 200 
    assert response.json()["categoria"] == "Peito e Tríceps ATUALIZADO"


def test_delete_treino(client, treino_cadastrado):
    """Testa o delete de um treino e verifica se ele sumiu"""
    treino_id = treino_cadastrado["treino"]["id_treino"]

    response_delete = client.delete(f"/Treino/{treino_id}")
    assert response_delete.status_code in [200, 204]

    response_get = client.get(f"/Treino/{treino_id}")
    assert response_get.status_code == 404

# Testes de Caminho Triste

def test_read_treino_nao_encontrado(client):
    """Testa obter um treino com id inexistente"""

    response = client.get("/Treino/99999")
    assert response.status_code == 404


@pytest.mark.parametrize(
    "campo_faltante, json_payload",
    [
        ("descricao_treino", {
            "nome_treino": "Treino Incompleto",
            "id_aluno": 1, 
            # "descricao_treino": "Faltando",
            "categoria": "Geral",
            "num_series": 3
        }),
        ("categoria", {
            "nome_treino": "Treino Incompleto",
            "id_aluno": 1,
            "descricao_treino": "Descrição OK",
            # "categoria": "Faltando",
            "num_series": 3
        }),
    ]
)
def test_create_treino_erro_422_campos_faltantes(client, aluno_cadastrado, campo_faltante, json_payload):
    """ Testa se a API retorna erro quando um campo é passado em branco ou tem o tipo errado
    """

    json_payload["id_aluno"] = aluno_cadastrado["id_aluno"]
    
    response = client.post("/Treino/", json=json_payload)
    
    assert response.status_code == 422
    data = response.json()
    assert data["detail"][0]["type"] == "missing"
    assert data["detail"][0]["loc"] == ["body", campo_faltante]


def test_create_treino_aluno_inexistente(client):
    """Testa se a criação de treino falha se o id_aluno fornecido não existe no banco
    """
    
    response = client.post(
        "/Treino/",
        json={
            "nome_treino": "Treino Fantasma",
            "id_aluno": 99999, 
            "descricao_treino": "Descrição",
            "categoria": "Geral",
            "num_series": 3
        }
    )
    assert 400 <= response.status_code < 500
    