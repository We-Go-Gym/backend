from sqlalchemy import Column, Integer, String, Float, Table, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

# Associação entre treino e exercícios
treino_exercicio_associacao = Table('TREINO_POSSUI_EXERCICIO', Base.metadata,
    Column('id_treino', Integer, ForeignKey('TREINO.id_treino'), primary_key=True),
    Column('id_exercicio', Integer, ForeignKey('EXERCICIO.id_exercicio'), primary_key=True)
)

# Estrutura da tabela Exercicio
class Exercicio(Base):
    __tablename__ = 'EXERCICIO'

    id_exercicio = Column(Integer, primary_key=True, index=True)
    nome_exercicio = Column(String(256), nullable=False)
    descricao_exercicio = Column(String(256),nullable=False, unique=True)
    num_repeticoes = Column(Integer, nullable=False)

    
    treinos = relationship("Treino",secondary=treino_exercicio_associacao,back_populates="exercicios")