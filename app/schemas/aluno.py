from pydantic import BaseModel, ConfigDict
from typing import List, Optional


# Classe para criação de um novo aluno
class AlunoCreate(BaseModel):
    nome_aluno: str
    email: str
    senha: str
    idade: int
    peso_kg: float
    altura: float


class AlunoUpdate(BaseModel):
    nome_aluno: Optional[str] = None
    email: Optional[str] = None
    senha: Optional[str] = None  # Senha em texto plano (opcional)
    idade: Optional[int] = None
    peso_kg: Optional[float] = None
    altura: Optional[float] = None

# Classe  de um aluno (inclui o id do banco)
class Aluno(BaseModel):
    id_aluno: int
    nome_aluno: str
    email: str
    idade: int
    peso_kg: float
    altura: float

    treinos: List['Treino'] = [] 
    historico_imc: List['Imc'] = []

    # Permite converter direto do modelo SQLAlchemy -> Pydantic
    model_config = ConfigDict(from_attributes=True)
