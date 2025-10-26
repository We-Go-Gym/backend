# Exporta as classes dos schemas/aluno.py
from .aluno import Aluno, AlunoCreate, AlunoUpdate
# Exporta as classes dos schemas/treino.py
from .treino import Treino, TreinoCreate

from .imc import Imc, ImcCreate

from .exercicio import Exercicio, ExercicioCreate

Aluno.model_rebuild()
