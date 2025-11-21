"""Este módulo define os schemas pydantic para a entidade Aluno"""
# pylint: disable=too-few-public-methods
from typing import List, Optional
from pydantic import BaseModel, ConfigDict


class AlunoCreate(BaseModel):
    """Schema pydantic para a criação de um novo aluno"""
    nome_aluno: str
    email: str
    #senha: str
    idade: int
    peso_kg: float
    altura: float


class AlunoUpdate(BaseModel):
    """Schema pydantic para a atualização de um aluno existente"""
    nome_aluno: Optional[str] = None
    email: Optional[str] = None
    #senha: Optional[str] = None
    idade: Optional[int] = None
    peso_kg: Optional[float] = None
    altura: Optional[float] = None

class Aluno(BaseModel):
    """Schema pydantic para a leitura/retorno de um aluno (inclui o id do banco)"""
    id_aluno: int
    nome_aluno: str
    email: str
    idade: int
    peso_kg: float
    altura: float

    treinos: List['Treino'] = []
    historico_imc: List['Imc'] = []

    # Permite converter direto do modelo SQLAlchemy -> pydantic
    model_config = ConfigDict(from_attributes=True)
