from fastapi import FastAPI, status, HTTPException, Depends    
from typing import List
from app.database import Base, engine , SessionLocal , get_session
from sqlalchemy.orm import Session
from app import models
from app import schemas

Base.metadata.create_all(engine)

app = FastAPI()


#CRUD de Cadastro de aluno

#Mensagem da aplicação
@app.get('/')
def welcome():
    return {'message': 'Inicializado aplicação FastAPI'}



#solicita lista de alunos
@app.get("/Aluno", response_model=List[schemas.Aluno] )
def read_Alunos_list(session: Session = Depends(get_session)):
    Alunos_list = session.query(models.Aluno).all()
    return Alunos_list


#Cria um novo alunos
@app.post("/Aluno", response_model=schemas.Aluno, status_code=status.HTTP_201_CREATED )
def create_aluno(aluno: schemas.AlunoCreate, session: Session = Depends(get_session)):
    aluno_db = models.Aluno(nome=aluno.nome, email=aluno.email, idade=aluno.idade, peso_kg=aluno.peso_kg, altura=aluno.altura)
    session.add(aluno_db)
    session.commit()
    session.refresh(aluno_db)

    return aluno_db

#Atualiza oa alunos da tabela ALuno
@app.put("/Aluno/{aluno_id}", response_model=schemas.Aluno)
def update_aluno(aluno_id: int, aluno: schemas.AlunoCreate, session: Session = Depends(get_session)):
    aluno_db = session.query(models.Aluno).get(aluno_id)

    if aluno_db:
        aluno_db.nome = aluno.nome
        aluno_db.email = aluno.email
        aluno_db.idade = aluno.idade
        aluno_db.peso_kg = aluno.peso_kg
        aluno_db.altura = aluno.altura
        session.commit()
    else:
        raise HTTPException(status_code=404, detail=f"Aluno com id {aluno_id} não encontrado")

    return aluno_db

#Deleta deleta um aluno da tabela alunos
@app.delete("/Aluno/{aluno_id}" , status_code=status.HTTP_204_NO_CONTENT)
def delete_book(aluno_id: int ,session: Session = Depends(get_session) ):
    aluno_db = session.query(models.Aluno).get(aluno_id)
    if aluno_db :
        session.delete(aluno_db)
        session.commit()
    else:
        raise HTTPException(status_code=404, detail=f"Task with id {aluno_id} not found")
    return None

