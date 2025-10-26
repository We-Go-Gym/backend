from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship
from app.database import Base

# Estrutura da tabela Alunos
class Aluno(Base):
    __tablename__ = 'ALUNO'

    id_aluno = Column(Integer, primary_key=True, index=True)
    nome_aluno = Column(String(256), nullable=False)
    email = Column(String(256),nullable=False, unique=True)
    senha_hash = Column(String(256), nullable=False) # salva o hash da senha
    idade = Column(Integer, nullable=False)
    peso_kg = Column(Float,nullable=False)
    altura = Column(Float,nullable=False)



    treinos = relationship("Treino", back_populates="aluno", cascade="all, delete-orphan")
    historico_imc = relationship("Imc", back_populates="aluno", cascade="all, delete-orphan") 
