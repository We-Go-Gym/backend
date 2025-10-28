"""Arquivo de inicialização do módulo schemas"""
from .aluno import Aluno, AlunoCreate, AlunoUpdate
from .treino import Treino, TreinoCreate
from .imc import Imc, ImcCreate
from .exercicio import Exercicio, ExercicioCreate

Aluno.model_rebuild()
