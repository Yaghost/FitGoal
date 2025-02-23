from fastapi import APIRouter, HTTPException, Depends
from odmantic import ObjectId, AIOEngine
from database import get_engine
from models.aluno import Aluno
from typing import List
from services.alunos import get_alunos_sorted_by_nome, count_alunos, search_alunos_by_nome, get_media_peso_alunos

router = APIRouter(
    prefix="/alunos",
    tags=["Alunos"],
)

@router.post("/", response_model=Aluno)
async def create_aluno(aluno: Aluno, engine: AIOEngine = Depends(get_engine)) -> Aluno:
    await engine.save(aluno)
    return aluno

@router.get("/", response_model=list[Aluno])
async def get_all_alunos(engine: AIOEngine = Depends(get_engine)) -> list[Aluno]:
    return await engine.find(Aluno)


@router.put("/{aluno_id}", response_model=Aluno)
async def update_aluno(aluno_id: str, aluno_data: Aluno, engine: AIOEngine = Depends(get_engine)) -> Aluno:
    aluno = await engine.find_one(Aluno, Aluno.id == ObjectId(aluno_id))
    if not aluno:
        raise HTTPException(status_code=404, detail="Aluno not found")

    # Atualiza os dados do aluno
    aluno.nome = aluno_data.nome
    aluno.email = aluno_data.email
    aluno.telefone = aluno_data.telefone
    aluno.peso = aluno_data.peso
    aluno.altura = aluno_data.altura

    await engine.save(aluno)
    return aluno

@router.delete("/{aluno_id}")
async def delete_aluno(aluno_id: str, engine: AIOEngine = Depends(get_engine)) -> dict:
    aluno = await engine.find_one(Aluno, Aluno.id == ObjectId(aluno_id))
    if not aluno:
        raise HTTPException(status_code=404, detail="Aluno not found")

    await engine.delete(aluno)
    return {"message": "Aluno deleted"}

@router.get("/ordenados")
async def listar_alunos_ordenados(engine: AIOEngine = Depends(get_engine)):
    return await get_alunos_sorted_by_nome(engine)
    

@router.get("/count")
async def contar_alunos(engine: AIOEngine = Depends(get_engine)):
    total = await count_alunos(engine)
    return {"total_alunos": total}


@router.get("/media-peso", response_model=dict)
async def media_peso_alunos(engine: AIOEngine = Depends(get_engine)):
    result = await get_media_peso_alunos(engine)
    return result


@router.get("/buscar/{nome_parcial}", response_model=List[Aluno])
async def buscar_alunos(nome_parcial: str, engine: AIOEngine = Depends(get_engine)):
    return await search_alunos_by_nome(engine, nome_parcial)


@router.get("/{aluno_id}", response_model=Aluno)
async def get_aluno(aluno_id: str, engine: AIOEngine = Depends(get_engine)) -> Aluno:
    aluno = await engine.find_one(Aluno, Aluno.id == ObjectId(aluno_id))
    if not aluno:
        raise HTTPException(status_code=404, detail="Aluno not found")
    return aluno