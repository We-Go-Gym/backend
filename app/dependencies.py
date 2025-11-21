"""Módulo de dependências e segurança da API de autenticação"""
import os
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from app.database import get_session
from app.models import Aluno

# Pega a chave secreta do ambiente
SECRET_KEY = os.getenv("AUTH_SECRET_KEY", "supersecret_dev_key_wgg")
ALGORITHM = "HS256"

# Aponta para a URL de login da API de Auth
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="http://localhost:8001/login")

def get_aluno_atual(token: str = Depends(oauth2_scheme), session: Session = Depends(get_session)):
    """Valida o token e retorna o aluno correspondente do banco de dados"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não foi possível validar as credenciais",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        # Tenta abrir o Token usando a chave secreta
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        # Lê o email dentro de sub
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception

    except JWTError as exc:
        raise credentials_exception from exc

    # Busca o aluno no banco pelo email
    aluno = session.query(Aluno).filter(Aluno.email == email).first()

    if aluno is None:
        # O token é válido, mas o aluno ainda não foi criado no banco principal
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Perfil de aluno não encontrado para este usuário."
        )

    return aluno
