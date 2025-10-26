from fastapi import FastAPI, status, HTTPException, Depends , APIRouter
from typing import List
from app.database import Base, engine , SessionLocal , get_session
from sqlalchemy.orm import Session
from app.models import Aluno
from app.schemas import Aluno as AlunoSchema, AlunoCreate, AlunoUpdate
from passlib.hash import pbkdf2_sha256
from passlib.context import CryptContext


chave_criptografada = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")
def criptografa_senha(senha: str) -> str:
    return chave_criptografada.hash(senha)


router = APIRouter(prefix="/Aluno",tags=["Alunos"])

#solicita lista de alunos
@router.get("/", response_model=List[AlunoSchema] )
def read_Alunos_list(session: Session = Depends(get_session)):
    Alunos_list = session.query(Aluno).all()
    return Alunos_list


@router.get("/{id_aluno}", response_model=AlunoSchema)
def read_aluno(id_aluno: int, session: Session = Depends(get_session)):
    aluno_db = session.query(Aluno).get(id_aluno)
    
    if not aluno_db:
        raise HTTPException(status_code=404, detail=f"Aluno com id {id_aluno} não encontrado")
        
    return aluno_db


#Cria um novo alunos
@router.post("/", response_model=AlunoSchema, status_code=status.HTTP_201_CREATED )
def create_aluno(aluno: AlunoCreate, session: Session = Depends(get_session)):
    senha_protegida= criptografa_senha(aluno.senha)
    aluno_db = Aluno(nome_aluno= aluno.nome_aluno, email=aluno.email, senha_hash=senha_protegida, idade=aluno.idade, peso_kg=aluno.peso_kg, altura=aluno.altura)
    session.add(aluno_db)
    session.commit()
    session.refresh(aluno_db)

    return aluno_db

#Atualiza oa alunos da tabela ALuno
@router.patch("/{id_aluno}", response_model=AlunoSchema)
def update_aluno(id_aluno: int, aluno_update: AlunoUpdate, session: Session = Depends(get_session)):
    aluno_db = session.query(Aluno).get(id_aluno)
    if not aluno_db:
            raise HTTPException(status_code=404, detail=f"Aluno com id {id_aluno} não encontrado")

    update_data = aluno_update.model_dump(exclude_unset=True)

        # Lógica especial para a senha
    if "senha" in update_data:
            # Pega a senha do dicionário, criptografa e salva
            senha_nova = update_data.pop("senha")
            if senha_nova: # Garante que a senha não é uma string vazia
                aluno_db.senha_hash = criptografa_senha(senha_nova)
                
        # Atualiza todos os outros campos que vieram no request
    for key, value in update_data.items():
            setattr(aluno_db, key, value)
                
    session.commit()
    session.refresh(aluno_db)
    return aluno_db

#Deleta deleta um aluno da tabela alunos
@router.delete("/{id_aluno}" , status_code=status.HTTP_204_NO_CONTENT)
def delete_book(id_aluno: int ,session: Session = Depends(get_session) ):
    aluno_db = session.query(Aluno).get(id_aluno)
    if aluno_db :
        session.delete(aluno_db)
        session.commit()
    else:
        raise HTTPException(status_code=404, detail=f"Aluno com id {id_aluno} não encontrado")
    return None

