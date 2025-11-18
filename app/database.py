"""Módulo para configuração do banco de dados e gerenciamento da sessão"""
# pylint: disable=import-error,unused-import,invalid-name

import os

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker


#OBS: Está no modo SQLITE para ativar o mysql para o docker comente a l-7 e descomente da 8 até a 17
#engine = create_engine("sqlite:///fastapidb.db")
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "password")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_NAME = os.getenv("DB_NAME", "wggdb")

# #Chama a base de dados
SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

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
