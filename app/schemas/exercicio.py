"""Este módulo define os schemas pydantic para a entidade Exercicio"""
# pylint: disable=too-few-public-methods
from pydantic import BaseModel, ConfigDict


class ExercicioCreate(BaseModel):
    """Schema pydantic para a criação de um novo exercicio"""
    nome_exercicio: str
    descricao_exercicio: str
    num_repeticoes: int


class Exercicio(BaseModel):
    """Schema pydantic para a leitura/retorno de um exercicio (inclui o id do banco)"""
    id_exercicio: int
    nome_exercicio: str
    descricao_exercicio: str
    num_repeticoes: int


    # Permite converter direto do modelo SQLAlchemy -> Pydantic
    model_config = ConfigDict(from_attributes=True)
