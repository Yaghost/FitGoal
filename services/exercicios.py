from odmantic import AIOEngine, ObjectId
from models.exercicio import Exercicio
from models.treino import Treino
from models.aluno import Aluno


async def count_exercicios_by_grupo(engine: AIOEngine):
    """
    Conta a quantidade de exercícios agrupados por grupo muscular.

    Args:
        engine (AIOEngine): Instância do banco de dados assíncrono.

    Returns:
        dict: Um dicionário onde as chaves são os grupos musculares e os valores
              são a quantidade de exercícios em cada grupo.
    """
    pipeline = [{"$group": {"_id": "$grupo_muscular", "total_exercicios": {"$sum": 1}}}]

    result = await engine.database["exercicio"].aggregate(pipeline).to_list(length=None)

    return {grupo["_id"]: grupo["total_exercicios"] for grupo in result}


async def get_treinos_with_exercicios_by_aluno(engine: AIOEngine, aluno_id: str):
    """
    Recupera os treinos e exercícios de um aluno específico, incluindo o nome e ID do aluno.

    Parâmetros:
    - engine (AIOEngine): Motor de banco de dados assíncrono.
    - aluno_id (str): ID do aluno.

    Retorna:
    - List[Dict]: Lista de dicionários contendo o nome do aluno, ID do aluno, os treinos e seus exercícios.
    """
    aluno = await engine.find_one(Aluno, Aluno.id == ObjectId(aluno_id))
    if not aluno:
        return {"error": "Aluno não encontrado"}

    treinos = await engine.find(Treino)
    treinos_filtrados = [
        treino for treino in treinos if treino.aluno.id == ObjectId(aluno_id)
    ]

    result = []

    aluno_info = {"nome": aluno.nome, "id": str(aluno.id), "treinos": []}

    for treino in treinos_filtrados:
        # Criar o dicionário com os dados do treino
        treino_info = {
            "nome": treino.nome,
            "dia_semana": treino.dia_semana,
            "exercicios": [],
        }

        # Adicionar os exercícios ao treino
        for exercicio_embedded in treino.exercicios:
            exercicio = await engine.find_one(
                Exercicio, Exercicio.id == ObjectId(exercicio_embedded.exercicio_id)
            )
            if exercicio:
                treino_info["exercicios"].append(exercicio)

        aluno_info["treinos"].append(treino_info)

    result.append(aluno_info)
    return result
