"""Módulo que define as rotas da API para Exercícios"""
# pylint: disable=import-error
from typing import List

from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

from app.database import  get_session #Base, engine , SessionLocal ,
from app.models import Imc, Aluno
from app.schemas import Imc as ImcSchema, ImcCreate

#Base.metadata.create_all(engine)

router= APIRouter(prefix="/Imc", tags=["Imcs"])

@router.get("/", response_model=List[ImcSchema] )
def read_imc_list(session: Session = Depends(get_session)):
    """Retorna uma lista de todos os IMCs"""
    imc_list = session.query(Imc).all()
    return imc_list



@router.get("/{id_imc}", response_model=ImcSchema)
def read_imc(id_imc: int, session: Session = Depends(get_session)):
    """Retorna um imc específico pelo seu ID"""
    imc_db = session.query(Imc).get(id_imc)

    if not imc_db:
        raise HTTPException(
        status_code=404,
        detail=f"Registro de IMC com id {id_imc} não encontrado")

    return imc_db


@router.post("/", response_model=ImcSchema, status_code=status.HTTP_201_CREATED )
def create_imc(imc: ImcCreate, session: Session = Depends(get_session)):
    """Cria um novo imc no banco de dados"""
    aluno_db = session.query(Aluno).get(imc.id_aluno)

    # Avalia se o id do aluno existe para poder associar o imc ao aluno
    if not aluno_db:
        raise HTTPException(
        status_code=404,
        detail=f"Aluno com id {imc.id_aluno} não encontrado. Não é possível calcular o IMC.")

    # Verifica a alutra do aluno
    if aluno_db.altura == 0:
        raise HTTPException(
            status_code=400,
            detail="Altura do aluno não pode ser zero para calcular o IMC.")

    # Arredonda e calcula o IMC
    valor_imc = round(aluno_db.peso_kg / (aluno_db.altura ** 2), 2)

    imc_db = Imc(valor_imc=valor_imc, id_aluno= imc.id_aluno)
    session.add(imc_db)
    session.commit()
    session.refresh(imc_db)

    return imc_db


@router.delete("/{id_imc}" , status_code=status.HTTP_204_NO_CONTENT)
def delete_imc(id_imc: int ,session: Session = Depends(get_session) ):
    """Deleta os dados de um Imc na tabela IMC"""
    imc_db = session.query(Imc).get(id_imc)

    if imc_db :
        session.delete(imc_db)
        session.commit()
    else:
        raise HTTPException(
            status_code=404,
            detail=f"IMC com id: {id_imc} not found")
