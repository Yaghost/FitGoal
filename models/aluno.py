from odmantic import Model
from typing import Optional

class Aluno(Model):
    nome: Optional[str]
    email: Optional[str]
    telefone: Optional[str]
    peso: Optional[float]
    altura: Optional[float]