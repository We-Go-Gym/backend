from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey, func
from sqlalchemy.orm import relationship
from app.database import Base

# Estrutura da tabela IMC
class Imc(Base):
    __tablename__ = 'IMC'

    id_imc = Column(Integer, primary_key=True, index=True)
    valor_imc = Column(Float, nullable=False)
    dt_calculo = Column(Date, nullable=False, server_default=func.current_date())
    id_aluno = Column(Integer, ForeignKey('ALUNO.id_aluno'), nullable=False)


    aluno = relationship("Aluno", back_populates="historico_imc")