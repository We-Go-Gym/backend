"""Módulo para configuração do banco de dados e gerenciamento da sessão"""
# pylint: disable=import-error,unused-import,invalid-name

import os

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

# Chama a base de dados para testar tanto no deploy quanto no docker
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    os.getenv("DATABASE_URL_API", "mysql+pymysql://root:password@mysql:3306/wggdb")
)

# Correção da rota pro railway
if DATABASE_URL.startswith("mysql://"):
    DATABASE_URL = DATABASE_URL.replace("mysql://", "mysql+pymysql://")

engine = create_engine(DATABASE_URL, pool_pre_ping=True)

Base = declarative_base()
SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)

#Iniciar a sessão
def get_session():
    """Dependência do FastAPI para injetar uma sessão de banco de dados"""
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
