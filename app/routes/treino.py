"""Módulo que define as rotas da API para Treinos"""
# pylint: disable=import-error
from typing import List

from fastapi import  status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

from app.database import  get_session #Base, engine , SessionLocal ,
from app.models import Treino, Aluno, Exercicio
from app.schemas import Treino as TreinoSchema, TreinoCreate, Exercicio as ExercicioSchema

router = APIRouter(prefix="/Treino", tags=["Treinos"])


@router.get("/", response_model=List[TreinoSchema] )
def read_treinos_list(session: Session = Depends(get_session)):
    """Retorna uma lista de todos os treinos"""
    treinos_list = session.query(Treino).all()
    return treinos_list


@router.get("/{id_treino}", response_model=TreinoSchema)
def read_treino(id_treino: int, session: Session = Depends(get_session)):
    """Retorna um treino específico pelo seu ID"""
    treino_db = session.query(Treino).get(id_treino)

    if not treino_db:
        raise HTTPException(
        status_code=404,
        detail=f"Treino com id {id_treino} não encontrado")

    return treino_db


@router.post("/", response_model=TreinoSchema, status_code=status.HTTP_201_CREATED )
def create_treino(treino: TreinoCreate, session: Session = Depends(get_session)):
    """Cria um novo treino no banco de dados."""
    aluno_db = session.query(Aluno).get(treino.id_aluno)

    # Avalia se o id do aluno existe para poder associar o treino ao aluno
    if not aluno_db:
        raise HTTPException(
        status_code=404,
        detail=f"Aluno com id {treino.id_aluno} não encontrado. Não é possível criar o treino.")


    treino_db = Treino(
        nome_treino =treino.nome_treino,
        descricao_treino=treino.descricao_treino,
        categoria= treino.categoria,
        num_series=treino.num_series,id_aluno=treino.id_aluno )

    session.add(treino_db)
    session.commit()
    session.refresh(treino_db)

    return treino_db


@router.put("/{id_treino}", response_model=TreinoSchema)
def update_treino(id_treino: int, treino: TreinoCreate, session: Session = Depends(get_session)):
    """Atualiza os dados de um treino na tabela TREINO"""
    treino_db = session.query(Treino).get(id_treino)

    if treino_db:
        treino_db.nome_treino = treino.nome_treino
        treino_db.descricao_treino = treino.descricao_treino
        treino_db.categoria = treino.categoria
        treino_db.num_series = treino.num_series
        treino_db.id_aluno = treino.id_aluno
        session.commit()
    else:
        raise HTTPException(
        status_code=404,
        detail=f"Treino com id {id_treino} não encontrado")

    return treino_db


@router.delete("/{id_treino}" , status_code=status.HTTP_204_NO_CONTENT)
def delete_treino(id_treino: int ,session: Session = Depends(get_session) ):
    """Deleta os dados de um treino na tabela TREINO"""
    treino_db = session.query(Treino).get(id_treino)

    if treino_db :
        session.delete(treino_db)
        session.commit()
    else:
        raise HTTPException(
        status_code=404,
        detail=f"Treino com id: {id_treino} não encontrado")


# Rotas para a associação de treino e exercício N:M

@router.get("/{id_treino}/exercicios", response_model=List[ExercicioSchema], tags=["Treinos"])
def listar_exercicios_do_treino(id_treino: int, session: Session = Depends(get_session)):
    """Retorna uma lista de todos os exercícios daquele treino"""
    treino_db = session.query(Treino).get(id_treino)

    if not treino_db:
        raise HTTPException(
        status_code=404,
        detail=f"Treino com id {id_treino} não encontrado")

    return treino_db.exercicios


@router.post("/{id_treino}/exercicio/{id_exercicio}", response_model=TreinoSchema, tags=["Treinos"])
def adicionar_exercicio_ao_treino(
    id_treino: int, id_exercicio: int, session: Session = Depends(get_session)):

    """Associa um exercício a um treino"""
    treino_db = session.query(Treino).get(id_treino)

    # Avalia se o id do treino existe para fazer a associação
    if not treino_db:
        raise HTTPException(
        status_code=404,
        detail=f"Treino com id {id_treino} não encontrado")

    exercicio_db = session.query(Exercicio).get(id_exercicio)

    # Avalia se o id do exercício existe pra associação
    if not exercicio_db:
        raise HTTPException(
        status_code=404,
        detail=f"Exercicio com id: {id_exercicio} não encontrado  ")


    if exercicio_db not in treino_db.exercicios:
        treino_db.exercicios.append(exercicio_db)
        session.commit()
        session.refresh(treino_db)

    return treino_db


@router.delete("/{id_treino}/exercicio/{id_exercicio}",
               status_code=status.HTTP_204_NO_CONTENT,
               tags=["Treinos"])

def remover_exercicio_do_treino(
    id_treino: int, id_exercicio: int, session: Session = Depends(get_session)):

    """Remove um exercício de um treino"""
    treino_db = session.query(Treino).get(id_treino)

    # Avalia se o id do treino existe para a remoção
    if not treino_db:
        raise HTTPException(
        status_code=404,
        detail=f"Treino com id: {id_treino} não encontrado")

    exercicio_db = session.query(Exercicio).get(id_exercicio)

    # Avalia se o id do exercício existe para a remoção
    if not exercicio_db:
        raise HTTPException(
        status_code=404,
        detail=f"Exercicio com id: {id_exercicio} não encontrado")

    if exercicio_db in treino_db.exercicios:
        treino_db.exercicios.remove(exercicio_db)
        session.commit()
