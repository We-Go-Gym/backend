"""Configurações e fixtures globais para os testes"""
# pylint: disable=redefined-outer-name, invalid-name, wrong-import-position
import os
from datetime import date
import pytest
from sqlalchemy import create_engine, StaticPool
from sqlalchemy.orm import sessionmaker
from sqlalchemy.schema import ColumnDefault
from starlette.testclient import TestClient

# Forçar as váriáveis de ambiente antes do app
os.environ["DATABASE_URL"] = "sqlite:///./test_temp.db"
os.environ["DATABASE_URL_APP"] = "sqlite:///./test_temp.db"

from app.main import app
from app.database import Base, get_session


SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    #  StaticPool para garantir que o FastAPI e o Pytest usem o mesmo banco em memória
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db_session():
    """
    Aplica o Patch no modelo IMC para funcionar no SQLite antes de criar tabelas.
    """

    imc_table = Base.metadata.tables.get("IMC")

    if imc_table is not None:
        coluna_data = imc_table.c.dt_calculo
        coluna_data.server_default = None

        # Adiciona  o defaul para a coluna data
        if coluna_data.default is None:
            coluna_data.default = ColumnDefault(date.today)


    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db_session):
    """
    Fornece o client para o teste, garante que a API use o banco em memória
    """

    def override_get_session():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_session] = override_get_session
    yield TestClient(app)
    app.dependency_overrides.clear()


# FIXTURES DE DADOS


@pytest.fixture(scope="function")
def aluno_cadastrado(client):
    """
    Cria um Aluno base para testes que precisam de um aluno que já exista.
    """
    response = client.post(
        "/Aluno/",
        json={
            "nome_aluno": "Aluno Padrão",
            "email": "aluno@email.com",
            "idade": 25,
            "peso_kg": 75.0,
            "altura": 1.75,
        },
    )
    assert response.status_code == 201
    return response.json()


@pytest.fixture(scope="function")
def treino_cadastrado(client, aluno_cadastrado):
    """
    Cria um Treino base, já associado a um 'aluno_cadastrado' para criar a dependência
    """

    aluno_id = aluno_cadastrado["id_aluno"]

    response = client.post(
        "/Treino/",
        json={
            "nome_treino": "Treino Fixture",
            "id_aluno": aluno_id,
            "descricao_treino": "Treino de teste",
            "categoria": "Geral",
            "num_series": 3,
        },
    )
    assert response.status_code == 201

    # Retorna o json do treino e o do aluno para o teste ter ambos
    return {"treino": response.json(), "aluno": aluno_cadastrado}


@pytest.fixture(scope="function")
def exercicio_cadastrado(client):
    """Cria um Exercício base no banco"""
    response = client.post(
        "/Exercicio/",
        json={
            "nome_exercicio": "Supino Reto ",
            "descricao_exercicio": "Exercício para peito no banco reto.",
            "num_repeticoes": 10,
        },
    )
    assert response.status_code == 201
    return response.json()


@pytest.fixture(scope="function")
def imc_cadastrado(client, aluno_cadastrado):
    """
    Cria um registro de IMC base depende de 'aluno_cadastrado'
    """
    aluno_id = aluno_cadastrado["id_aluno"]

    response = client.post("/Imc/", json={"id_aluno": aluno_id})
    assert response.status_code == 201
    assert response.json()["valor_imc"] == 24.49

    # Retorna o json do imc e o do aluno para os testes
    return {"imc": response.json(), "aluno": aluno_cadastrado}
