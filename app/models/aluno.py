"""Este módulo define o modelo de dados para o Aluno"""
# pylint: disable=too-few-public-methods
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship
from app.database import Base


class Aluno(Base):
    """Classe que representa um Aluno no banco de dados"""

    __tablename__ = 'ALUNO'

    id_aluno = Column(Integer, primary_key=True, index=True)
    nome_aluno = Column(String(256), nullable=False)
    email = Column(String(256),nullable=False, unique=True)
    #senha_hash = Column(String(256), nullable=False)
    idade = Column(Integer, nullable=False)
    peso_kg = Column(Float,nullable=False)
    altura = Column(Float,nullable=False)



    treinos = relationship(
        "Treino", 
        back_populates="aluno",
        cascade="all, delete-orphan")

    historico_imc = relationship(
        "Imc",
        back_populates="aluno",
        cascade="all, delete-orphan")
