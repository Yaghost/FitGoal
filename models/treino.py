from odmantic import Model, Reference
from pydantic import BaseModel
from .aluno import Aluno
from .treino_exercicio_embedded import ExercicioTreinoEmbedded


class Treino(Model):
    nome: str
    dia_semana: str
    aluno: Aluno = Reference()
    exercicios: list[ExercicioTreinoEmbedded] = []


class TreinoInput(BaseModel):
    nome: str
    dia_semana: str
    exercicios: list[ExercicioTreinoEmbedded] = []
