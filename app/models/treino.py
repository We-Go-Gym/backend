from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
from .exercicio import treino_exercicio_associacao

# Estrutura da tabela Treino
class Treino(Base):
    __tablename__ = 'TREINO'

    id_treino = Column(Integer, primary_key=True, index=True)
    nome_treino = Column(String(256), nullable=False)
    descricao_treino = Column(String(256),nullable=False)
    categoria= Column(String(256), nullable=False)
    num_series = Column(Integer, nullable=False)
    id_aluno = Column(Integer, ForeignKey('ALUNO.id_aluno'), nullable=False)
    

    aluno = relationship("Aluno", back_populates="treinos")
    exercicios = relationship("Exercicio",secondary=treino_exercicio_associacao,back_populates="treinos")
