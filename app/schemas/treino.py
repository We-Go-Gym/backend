"""Este módulo define os schemas pydantic para a entidade Treino"""
# pylint: disable=too-few-public-methods
from typing import List
from pydantic import BaseModel, ConfigDict
from .exercicio import Exercicio

class TreinoCreate(BaseModel):
    """Schema pydantic para a criação de um novo treino"""
    nome_treino: str
    descricao_treino: str
    categoria: str
    num_series: int
    id_aluno: int

class Treino(BaseModel):
    """Schema pydantic para a leitura/retorno de um treino (inclui o id do banco)"""
    id_treino: int
    nome_treino: str
    descricao_treino: str
    categoria: str
    num_series: int
    id_aluno: int

    exercicios: List[Exercicio] = []

    # Permite converter do modelo SQLAlchemy -> Pydantic
    model_config = ConfigDict(from_attributes=True)
