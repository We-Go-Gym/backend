from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from .exercicio import Exercicio

# Classe para criação de um novo treino
class TreinoCreate(BaseModel):
    nome_treino: str
    descricao_treino: str
    categoria: str
    num_series: int
    id_aluno: int 

# Classe para retornar os dados de um treino
class Treino(BaseModel):
    id_treino: int
    nome_treino: str
    descricao_treino: str
    categoria: str
    num_series: int
    id_aluno: int 

    exercicios: List[Exercicio] = []

    # Permite converter do modelo SQLAlchemy -> Pydantic
    model_config = ConfigDict(from_attributes=True)