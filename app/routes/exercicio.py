"""Módulo que define as rotas da API para Exercícios"""
# pylint: disable=import-error
from typing import List

from fastapi import  status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

from app.database import  get_session # Base, engine , SessionLocal ,
from app.models import Exercicio
from app.schemas import Exercicio as ExercicioSchema, ExercicioCreate


router = APIRouter(prefix="/Exercicio", tags=["Exercicios"])


@router.get("/", response_model=List[ExercicioSchema] )
def read_exercicio_list(session: Session = Depends(get_session)):
    """Retorna uma lista de todos os exercícios"""
    exercicios_list = session.query(Exercicio).all()
    return exercicios_list


@router.get("/{id_exercicio}", response_model=ExercicioSchema)
def read_exercicio(id_exercicio: int, session: Session = Depends(get_session)):
    """Retorna um aluno específico pelo seu ID"""
    exercicio_db = session.query(Exercicio).get(id_exercicio)

    if not exercicio_db:
        raise HTTPException(
        status_code=404,
        detail=f"Exercicio com id {id_exercicio} não encontrado")

    return exercicio_db



@router.post("/", response_model=ExercicioSchema, status_code=status.HTTP_201_CREATED )
def create_exercicio(exercicio: ExercicioCreate, session: Session = Depends(get_session)):
    """Cria um novo exercício no banco de dados."""

    exercicio_db = Exercicio(
        nome_exercicio =exercicio.nome_exercicio,
        descricao_exercicio=exercicio.descricao_exercicio,
        num_repeticoes=exercicio.num_repeticoes )

    session.add(exercicio_db)
    session.commit()
    session.refresh(exercicio_db)

    return exercicio_db

@router.put("/{id_exercicio}", response_model=ExercicioSchema)
def update_exercicio(
    id_exercicio: int,exercicio: ExercicioCreate,session: Session = Depends(get_session)):

    """Atualiza os dados de um exercício na tabela EXERCICIO"""
    exercicio_db = session.query(Exercicio).get(id_exercicio)

    if exercicio_db:
        exercicio_db.nome_exercicio = exercicio.nome_exercicio
        exercicio_db.descricao_exercicio = exercicio.descricao_exercicio
        exercicio_db.num_repeticoes = exercicio.num_repeticoes
        session.commit()
    else:
        raise HTTPException(
        status_code=404,
        detail=f"EXERCICIO com id {id_exercicio} não encontrado")

    return exercicio_db


@router.delete("/{id_exercicio}" , status_code=status.HTTP_204_NO_CONTENT)
def delete_exercicio(id_exercicio: int ,session: Session = Depends(get_session) ):
    """Deleta os dados de um exercício na tabela EXERCICIO"""
    exercicio_db = session.query(Exercicio).get(id_exercicio)

    if exercicio_db :
        session.delete(exercicio_db)
        session.commit()
    else:
        raise HTTPException(
        status_code=404,
        detail=f"Exercicio com id: {id_exercicio} não encontrado")
