from fastapi import APIRouter, HTTPException, Depends
from odmantic import ObjectId, AIOEngine
from database import get_engine
from typing import List
from models.treino import Treino, TreinoInput
from models.treino_exercicio_embedded import (
    ExercicioTreinoEmbedded,
    ExercicioTreinoInput,
)
from models.exercicio import Exercicio
from services.treinos import count_treinos_por_aluno, listar_treinos_por_dia
from models.aluno import Aluno

router = APIRouter(
    prefix="/treinos",
    tags=["Treinos"],
)

engine = get_engine()


@router.get("/", response_model=list[Treino])
async def get_all_treinos() -> list[Treino]:
    treinos = await engine.find(Treino)
    return treinos


@router.post("/{aluno_id}", response_model=Treino)
async def create_treino(aluno_id: str, treino_in: TreinoInput) -> Treino:
    aluno = await engine.find_one(Aluno, Aluno.id == ObjectId(aluno_id))
    if not aluno:
        raise HTTPException(status_code=404, detail="Aluno not found")
    treino = Treino(
        nome=treino_in.nome,
        dia_semana=treino_in.dia_semana,
        exercicios=treino_in.exercicios,
        aluno=aluno,
    )
    await engine.save(treino)
    return treino


@router.post("/{treino_id}/exercicios", response_model=Treino)
async def add_exercicio_to_treino(
    treino_id: str, exercicio_input: ExercicioTreinoInput
) -> Treino:
    treino = await engine.find_one(Treino, Treino.id == ObjectId(treino_id))
    if not treino:
        raise HTTPException(status_code=404, detail="Treino not found")

    exercicio = await engine.find_one(
        Exercicio, Exercicio.id == ObjectId(exercicio_input.exercicio_id)
    )
    if not exercicio:
        raise HTTPException(status_code=404, detail="Exercicio not found")

    novo_exercicio = ExercicioTreinoEmbedded(
        exercicio_id=exercicio_input.exercicio_id,
        nome=exercicio.nome,
        series=exercicio.series,
        repeticoes=exercicio.repeticoes,
    )

    treino.exercicios.append(novo_exercicio)
    await engine.save(treino)
    return treino


@router.put("/{treino_id}/{aluno_id}", response_model=Treino)
async def update_treino(
    treino_id: str, aluno_id: str, treino_in: TreinoInput
) -> Treino:
    treino = await engine.find_one(Treino, Treino.id == ObjectId(treino_id))
    if not treino:
        raise HTTPException(status_code=404, detail="Treino not found")
    aluno = await engine.find_one(Aluno, Aluno.id == ObjectId(aluno_id))
    if not aluno:
        raise HTTPException(status_code=404, detail="Aluno not found")
    treino.nome = treino_in.nome
    treino.dia_semana = treino_in.dia_semana
    treino.exercicios = treino_in.exercicios
    treino.aluno = aluno
    await engine.save(treino)
    return treino


@router.delete("/{treino_id}")
async def delete_treino(treino_id: str) -> dict:
    treino = await engine.find_one(Treino, Treino.id == ObjectId(treino_id))
    if not treino:
        raise HTTPException(status_code=404, detail="Treino not found")
    await engine.delete(treino)
    return {"message": "Treino deleted"}


@router.delete("/{treino_id}/exercicios/{exercicio_id}", response_model=Treino)
async def remove_exercicio_from_treino(treino_id: str, exercicio_id: str) -> Treino:
    treino = await engine.find_one(Treino, Treino.id == ObjectId(treino_id))
    if not treino:
        raise HTTPException(status_code=404, detail="Treino not found")

    exercicios_atualizados = [
        ex for ex in treino.exercicios if ex.exercicio_id != exercicio_id
    ]

    if len(exercicios_atualizados) == len(treino.exercicios):
        raise HTTPException(status_code=404, detail="Exercício not found in treino")

    treino.exercicios = exercicios_atualizados
    await engine.save(treino)
    return treino


@router.get("/treinos/{dia_da_semana}", response_model=List[Treino])
async def get_treinos_por_dia(dia_da_semana: str, engine: AIOEngine = Depends(get_engine)):
    return await listar_treinos_por_dia(engine, dia_da_semana)


@router.get("/{aluno_id}/contagem")
async def contar_treinos(aluno_id: str, engine: AIOEngine = Depends(get_engine)):
    return await count_treinos_por_aluno(engine, aluno_id)


@router.get("/{treino_id}", response_model=Treino)
async def get_treino(treino_id: str) -> Treino:
    treino = await engine.find_one(Treino, Treino.id == ObjectId(treino_id))
    if not treino:
        raise HTTPException(status_code=404, detail="Treino not found")
    return treino