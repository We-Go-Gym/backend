from pydantic import BaseModel, ConfigDict
from typing import List, Optional
#from .treino import Treino


# Classe para criação de um novo exercicio
class ExercicioCreate(BaseModel):
    nome_exercicio: str
    descricao_exercicio: str
    num_repeticoes: int


# Classe  de um exercicio (inclui o id do banco)
class Exercicio(BaseModel):
    id_exercicio: int
    nome_exercicio: str
    descricao_exercicio: str
    num_repeticoes: int
    


    # Permite converter direto do modelo SQLAlchemy -> Pydantic
    model_config = ConfigDict(from_attributes=True)
