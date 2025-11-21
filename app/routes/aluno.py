"""Módulo que define as rotas da API para Alunos"""
# pylint: disable=import-error
from typing import List

from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session


from app.database import get_session
from app.models import Aluno
from app.schemas import Aluno as AlunoSchema, AlunoCreate, AlunoUpdate
from app.dependencies import get_aluno_atual

router = APIRouter(prefix="/Aluno", tags=["Alunos"])


@router.get("/me", response_model=AlunoSchema)
def read_my_profile(aluno_atual: Aluno = Depends(get_aluno_atual)):
    """
    Retorna todos os dados do aluno logado 
    O Token JWT é decodificado para achar o aluno pelo email.
    """
    return aluno_atual

@router.get("/", response_model=List[AlunoSchema])
def read_alunos_list(session: Session = Depends(get_session)):
    """Retorna uma lista de todos os alunos"""
    alunos_list = session.query(Aluno).all()
    return alunos_list


@router.get("/{id_aluno}", response_model=AlunoSchema)
def read_aluno(id_aluno: int, session: Session = Depends(get_session)):
    """Retorna um aluno específico pelo seu ID"""
    aluno_db = session.query(Aluno).get(id_aluno)

    if not aluno_db:
        raise HTTPException(
            status_code=404,
            detail=f"Aluno com id {id_aluno} não encontrado")

    return aluno_db


@router.post("/", response_model=AlunoSchema, status_code=status.HTTP_201_CREATED)
def create_aluno(aluno: AlunoCreate, session: Session = Depends(get_session)):
    """Cria um novo aluno no banco de dados (Apenas dados de perfil)"""


    aluno_db = Aluno(
        nome_aluno=aluno.nome_aluno,
        email=aluno.email,
        # senha_hash
        idade=aluno.idade,
        peso_kg=aluno.peso_kg,
        altura=aluno.altura
    )

    session.add(aluno_db)
    session.commit()
    session.refresh(aluno_db)

    return aluno_db


@router.patch("/{id_aluno}", response_model=AlunoSchema)
def update_aluno(id_aluno: int, aluno_update: AlunoUpdate, session: Session = Depends(get_session)):
    """Atualiza os dados de um aluno"""
    aluno_db = session.query(Aluno).get(id_aluno)

    if not aluno_db:
        raise HTTPException(
            status_code=404,
            detail=f"Aluno com id {id_aluno} não encontrado")

    update_data = aluno_update.model_dump(exclude_unset=True)


    for chave, valor in update_data.items():
        setattr(aluno_db, chave, valor)

    session.commit()
    session.refresh(aluno_db)
    return aluno_db


@router.delete("/{id_aluno}", status_code=status.HTTP_204_NO_CONTENT)
def delete_aluno(id_aluno: int, session: Session = Depends(get_session)):
    """Deleta os dados de um aluno do banco de dados"""
    aluno_db = session.query(Aluno).get(id_aluno)
    if aluno_db:
        session.delete(aluno_db)
        session.commit()
    else:
        raise HTTPException(
            status_code=404,
            detail=f"Aluno com id {id_aluno} não encontrado")
