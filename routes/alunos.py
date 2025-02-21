from fastapi import APIRouter, HTTPException
from odmantic import ObjectId
from database import get_engine
from models.aluno import Aluno

router = APIRouter(
    prefix="/alunos",
    tags=["Alunos"],
)

engine = get_engine()

@router.post("/", response_model=Aluno)
async def create_aluno(aluno: Aluno) -> Aluno:
    await engine.save(aluno)
    return aluno

@router.get("/", response_model=list[Aluno])
async def get_all_alunos() -> list[Aluno]:
    alunos = await engine.find(Aluno)
    return alunos

@router.get("/{aluno_id}", response_model=Aluno)
async def get_aluno(aluno_id: str) -> Aluno:
    aluno = await engine.find_one(Aluno, Aluno.id == ObjectId(aluno_id))
    if not aluno:
        raise HTTPException(status_code=404, detail="Aluno not found")
    return aluno

@router.put("/{aluno_id}", response_model=Aluno)
async def update_aluno(aluno_id: str, aluno_data: Aluno) -> Aluno:
    aluno = await engine.find_one(Aluno, Aluno.id == ObjectId(aluno_id))
    if not aluno:
        raise HTTPException(status_code=404, detail="Aluno not found")
    aluno.nome = aluno_data.nome
    aluno.email = aluno_data.email
    aluno.telefone = aluno_data.telefone
    aluno.peso = aluno_data.peso
    aluno.altura = aluno_data.altura
    await engine.save(aluno)
    return aluno

@router.delete("/{aluno_id}")
async def delete_aluno(aluno_id: str) -> dict:
    aluno = await engine.find_one(Aluno, Aluno.id == ObjectId(aluno_id))
    if not aluno:
        raise HTTPException(status_code=404, detail="Aluno not found")
    await engine.delete(aluno)
    return {"message": "Aluno deleted"}
