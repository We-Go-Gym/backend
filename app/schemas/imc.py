"""Este módulo define os schemas pydantic para a entidade IMC"""
# pylint: disable=too-few-public-methods
from datetime import date
from pydantic import BaseModel, ConfigDict


class ImcCreate(BaseModel):
    """Schema pydantic para a criação de um novo IMC"""
    id_aluno: int

class Imc(BaseModel):
    """Schema pydantic para a leitura/retorno de um IMC (inclui o id do banco)"""
    id_imc: int
    valor_imc: float
    dt_calculo: date
    id_aluno: int

    # Permite converter do modelo SQLAlchemy -> Pydantic
    model_config = ConfigDict(from_attributes=True)
