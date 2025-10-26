from fastapi import FastAPI, status, HTTPException, Depends, APIRouter    
from typing import List
from app.database import Base, engine , SessionLocal , get_session
from sqlalchemy.orm import Session
from app.models import Exercicio
from app.schemas import Exercicio as ExercicioSchema, ExercicioCreate


router = APIRouter(prefix="/Exercicio", tags=["Exercicios"])

#solicita lista de Exercícios
@router.get("/", response_model=List[ExercicioSchema] )
def read_exercicio_list(session: Session = Depends(get_session)):
    Exercicios_list = session.query(Exercicio).all()
    return Exercicios_list


# Solicita um exercicio especifico
@router.get("/{id_exercicio}", response_model=ExercicioSchema)
def read_exercicio(id_exercicio: int, session: Session = Depends(get_session)):
    
    exercicio_db = session.query(Exercicio).get(id_exercicio)
    if not exercicio_db:
        raise HTTPException(status_code=404, detail=f"Exercicio com id {id_exercicio} não encontrado")
    
    return exercicio_db



#Cria um novo Exercicio
@router.post("/", response_model=ExercicioSchema, status_code=status.HTTP_201_CREATED )
def create_exercicio(exercicio: ExercicioCreate, session: Session = Depends(get_session)):

    execicio_db = Exercicio(nome_exercicio =exercicio.nome_exercicio, descricao_exercicio=exercicio.descricao_exercicio, num_repeticoes=exercicio.num_repeticoes )
    session.add(execicio_db)
    session.commit()
    session.refresh(execicio_db)

    return execicio_db

#Atualiza os Exercicios da tabela EXERCICIO
@router.put("/{id_exercicio}", response_model=ExercicioSchema)
def update_exercicio(id_exercicio: int, exercicio: ExercicioCreate, session: Session = Depends(get_session)):
    exercicio_db = session.query(Exercicio).get(id_exercicio)

    if exercicio_db:
        exercicio_db.nome_exercicio = exercicio.nome_exercicio
        exercicio_db.descricao_exercicio = exercicio.descricao_exercicio
        exercicio_db.num_repeticoes = exercicio.num_repeticoes
        session.commit()
    else:
        raise HTTPException(status_code=404, detail=f"EXERCICIO com id {id_exercicio} não encontrado")

    return exercicio_db

#Deleta um exercício da Tabela EXERCICIO
@router.delete("/{id_exercicio}" , status_code=status.HTTP_204_NO_CONTENT)
def delete_exercicio(id_exercicio: int ,session: Session = Depends(get_session) ):
    exercicio_db = session.query(Exercicio).get(id_exercicio)
    if exercicio_db :
        session.delete(exercicio_db)
        session.commit()
    else:
        raise HTTPException(status_code=404, detail=f"Exercicio com id: {id_exercicio} não encontrado")
    return None

