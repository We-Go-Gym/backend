from sqlalchemy import Column, Integer, String, Float
from app.database import Base

# Estrutura da tabela Alunos
class Aluno(Base):
    __tablename__ = 'alunos'

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(256))
    email = Column(String(256), unique=True)
    idade = Column(Integer)
    peso_kg = Column(Float)
    altura = Column(Float)

