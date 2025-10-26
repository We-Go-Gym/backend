from pydantic import BaseModel, ConfigDict
from datetime import date 
from typing import Optional

# Classe para criar um novo IMC
class ImcCreate(BaseModel):
    id_aluno: int 

# Classe para devolver os dados do IMC
class Imc(BaseModel):
    id_imc: int
    valor_imc: float
    dt_calculo: date
    id_aluno: int 

    # Permite converter do modelo SQLAlchemy -> Pydantic
    model_config = ConfigDict(from_attributes=True)
    
    
