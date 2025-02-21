from fastapi import FastAPI
from routes import home, alunos, exercicios, treinos

# FastAPI app instance
app = FastAPI()

# Rotas para Endpoints
app.include_router(home.router)
app.include_router(alunos.router)
app.include_router(exercicios.router)
app.include_router(treinos.router)
