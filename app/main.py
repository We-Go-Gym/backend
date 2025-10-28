"""Módulo para inicialização da aplicação"""
# pylint: disable=unused-import

from fastapi import FastAPI
from app.database import Base, engine
from app.models import Aluno,Treino,Imc, Exercicio
from app.routes import rota_aluno,rota_treino,rota_imc , rota_exercicio

Base.metadata.create_all(engine)

app = FastAPI(
    title="API de Alunos e Fitness",
    version="1.0"
)


app.include_router(rota_aluno)
app.include_router(rota_treino)
app.include_router(rota_imc)
app.include_router(rota_exercicio)


@app.get('/')
def welcome():
    """Rota de teste/saudação"""
    return {'message': 'API operacional e funcional.'}
