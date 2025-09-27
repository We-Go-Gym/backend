from pydantic import BaseModel, ConfigDict

# Classe para criação de um novo aluno
class AlunoCreate(BaseModel):
    nome: str
    email: str
    idade: int
    peso_kg: float
    altura: float

# Classe  de um aluno (inclui o id do banco)
class Aluno(BaseModel):
    id: int
    nome: str
    email: str
    idade: int
    peso_kg: float
    altura: float

    # Permite converter direto do modelo SQLAlchemy -> Pydantic
    model_config = ConfigDict(from_attributes=True)
