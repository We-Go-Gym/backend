from fastapi import FastAPI, status, HTTPException, Depends, APIRouter    
from typing import List
from app.database import Base, engine , SessionLocal , get_session
from sqlalchemy.orm import Session
from app.models import Treino, Aluno, Exercicio
from app.schemas import Treino as TreinoSchema, TreinoCreate, Exercicio as ExercicioSchema



router = APIRouter(prefix="/Treino", tags=["Treinos"])

#solicita lista de Treinos
@router.get("/", response_model=List[TreinoSchema] )
def read_Treinos_list(session: Session = Depends(get_session)):
    Treinos_list = session.query(Treino).all()
    return Treinos_list



@router.get("/{id_treino}", response_model=TreinoSchema)
def read_treino(id_treino: int, session: Session = Depends(get_session)):
    
    treino_db = session.query(Treino).get(id_treino)
    if not treino_db:
        raise HTTPException(status_code=404, detail=f"Treino com id {id_treino} não encontrado")
    
    return treino_db



#Cria um novo Treinos
@router.post("/", response_model=TreinoSchema, status_code=status.HTTP_201_CREATED )
def create_treino(treino: TreinoCreate, session: Session = Depends(get_session)):

    aluno_db = session.query(Aluno).get(treino.id_aluno)
    if not aluno_db:
        raise HTTPException(status_code=404, detail=f"Aluno com id {treino.id_aluno} não encontrado. Não é possível criar o treino.")

    treino_db = Treino(nome_treino =treino.nome_treino, descricao_treino=treino.descricao_treino, categoria= treino.categoria, num_series=treino.num_series,id_aluno=treino.id_aluno )
    session.add(treino_db)
    session.commit()
    session.refresh(treino_db)

    return treino_db

#Atualiza os Treinos da tabela TREINO
@router.put("/{id_treino}", response_model=TreinoSchema)
def update_treino(id_treino: int, treino: TreinoCreate, session: Session = Depends(get_session)):
    treino_db = session.query(Treino).get(id_treino)

    if treino_db:
        treino_db.nome_treino = treino.nome_treino
        treino_db.descricao_treino = treino.descricao_treino
        treino_db.categoria = treino.categoria
        treino_db.num_series = treino.num_series
        treino_db.id_aluno = treino.id_aluno
        session.commit()
    else:
        raise HTTPException(status_code=404, detail=f"Treino com id {id_treino} não encontrado")

    return treino_db

#Deleta deleta treino da Tabela TREINO
@router.delete("/{id_treino}" , status_code=status.HTTP_204_NO_CONTENT)
def delete_treino(id_treino: int ,session: Session = Depends(get_session) ):
    treino_db = session.query(Treino).get(id_treino)
    if treino_db :
        session.delete(treino_db)
        session.commit()
    else:
        raise HTTPException(status_code=404, detail=f"Treino com id: {id_treino} não encontrado")
    return None


# Rotas para a associação de treino e exercício N:M
# Rota para criar a associação
@router.post("/{id_treino}/exercicio/{id_exercicio}", response_model=TreinoSchema, tags=["Treinos"])
def adicionar_exercicio_ao_treino(
    id_treino: int, 
    id_exercicio: int, 
    session: Session = Depends(get_session)
):
    treino_db = session.query(Treino).get(id_treino)
    if not treino_db:
        raise HTTPException(status_code=404, detail=f"Treino com id {id_treino} não encontrado")

    exercicio_db = session.query(Exercicio).get(id_exercicio)
    if not exercicio_db:
        raise HTTPException(status_code=404, detail=f"Exercicio com id {id_exercicio} não encontrado")


    if exercicio_db not in treino_db.exercicios:
        treino_db.exercicios.append(exercicio_db)
        session.commit()
        session.refresh(treino_db)
    
    return treino_db


# Rota para REMOVER um exercício de um treino
@router.delete("/{id_treino}/exercicio/{id_exercicio}", status_code=status.HTTP_204_NO_CONTENT, tags=["Treinos"])
def remover_exercicio_do_treino(
    id_treino: int, 
    id_exercicio: int, 
    session: Session = Depends(get_session)
):
    treino_db = session.query(Treino).get(id_treino)
    if not treino_db:
        raise HTTPException(status_code=404, detail=f"Treino com id {id_treino} não encontrado")
        
    exercicio_db = session.query(Exercicio).get(id_exercicio)
    if not exercicio_db:
        raise HTTPException(status_code=404, detail=f"Exercicio com id {id_exercicio} não encontrado")

    if exercicio_db in treino_db.exercicios:
        treino_db.exercicios.remove(exercicio_db)
        session.commit()
    
    return None


# Rota para LISTAR todos os exercícios de um treino
@router.get("/{id_treino}/exercicios", response_model=List[ExercicioSchema], tags=["Treinos"])
def listar_exercicios_do_treino(id_treino: int, session: Session = Depends(get_session)):
    treino_db = session.query(Treino).get(id_treino)
    if not treino_db:
        raise HTTPException(status_code=404, detail=f"Treino com id {id_treino} não encontrado")
        
    return treino_db.exercicios