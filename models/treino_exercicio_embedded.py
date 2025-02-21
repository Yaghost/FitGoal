from odmantic import EmbeddedModel
from pydantic import BaseModel
from typing import Optional

class ExercicioTreinoEmbedded(EmbeddedModel):
    exercicio_id: str
    nome: Optional[str]
    series: int
    repeticoes: int

class ExercicioTreinoInput(BaseModel):
    exercicio_id: str