from fastapi import APIRouter, HTTPException
from odmantic import ObjectId
from database import get_engine
from models.exercicio import Exercicio
from services.exercicios import (
    count_exercicios_by_grupo,
    get_treinos_with_exercicios_by_aluno,
)

router = APIRouter(
    prefix="/exercicios",
    tags=["Exercicios"],
)

engine = get_engine()


@router.get("/", response_model=list[Exercicio])
async def get_all_exercicios() -> list[Exercicio]:
    exercicios = await engine.find(Exercicio)
    return exercicios


@router.post("/", response_model=Exercicio)
async def create_exercicio(exercicio: Exercicio) -> Exercicio:
    await engine.save(exercicio)
    return exercicio


@router.put("/{exercicio_id}", response_model=Exercicio)
async def update_exercicio(exercicio_id: str, exercicio_data: Exercicio) -> Exercicio:
    exercicio = await engine.find_one(Exercicio, Exercicio.id == ObjectId(exercicio_id))
    if not exercicio:
        raise HTTPException(status_code=404, detail="Exercicio not found")
    exercicio.nome = exercicio_data.nome
    exercicio.grupo_muscular = exercicio_data.grupo_muscular
    exercicio.dificuldade = exercicio_data.dificuldade
    exercicio.series = exercicio_data.series
    exercicio.repeticoes = exercicio_data.repeticoes
    exercicio.descricao = exercicio_data.descricao
    await engine.save(exercicio)
    return exercicio


@router.delete("/{exercicio_id}")
async def delete_exercicio(exercicio_id: str) -> dict:
    exercicio = await engine.find_one(Exercicio, Exercicio.id == ObjectId(exercicio_id))
    if not exercicio:
        raise HTTPException(status_code=404, detail="Exercicio not found")
    await engine.delete(exercicio)
    return {"message": "Exercicio deleted"}


@router.get("/contagem-por-grupo", response_model=dict)
async def get_contagem_exercicios_por_grupo():
    result = await count_exercicios_by_grupo(engine)
    return result


@router.get("/{exercicio_id}", response_model=Exercicio)
async def get_exercicio(exercicio_id: str) -> Exercicio:
    exercicio = await engine.find_one(Exercicio, Exercicio.id == ObjectId(exercicio_id))
    if not exercicio:
        raise HTTPException(status_code=404, detail="Exercicio not found")
    return exercicio


@router.get("/treinos/aluno/{aluno_id}", response_model=list[dict])
async def get_treinos_with_exercicios_by_aluno_route(aluno_id: str):
    treinos_exercicios = await get_treinos_with_exercicios_by_aluno(engine, aluno_id)
    if not treinos_exercicios:
        raise HTTPException(
            status_code=404, detail="Nenhum treino encontrado para este aluno"
        )
    return treinos_exercicios
