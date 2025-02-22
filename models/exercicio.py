from odmantic import Model
from typing import Optional


class Exercicio(Model):
    nome: str
    grupo_muscular: str
    dificuldade: str
    series: int
    repeticoes: int
    descricao: Optional[str]
