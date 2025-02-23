from odmantic import AIOEngine
from bson import ObjectId
from models.treino import Treino
from models.aluno import Aluno


async def count_treinos_por_aluno(engine: AIOEngine, aluno_id: str):
    """
    Conta o número de treinos de um aluno específico.

    Args:
        engine (AIOEngine): Instância do banco de dados assíncrono.
        aluno_id (str): ID do aluno para contar os treinos.

    Returns:
        dict: Dicionário com o ID do aluno, nome e o total de treinos ou mensagem de erro.
    """
    try:
        aluno_obj_id = ObjectId(aluno_id)
    except Exception:
        return {"error": "ID do aluno inválido"}

    aluno = await engine.find_one(Aluno, Aluno.id == aluno_obj_id)
    if not aluno:
        return {"error": "Aluno não encontrado"}

    pipeline = [{"$match": {"aluno": aluno_obj_id}}, {"$count": "total_treinos"}]

    result = await engine.database["treino"].aggregate(pipeline).to_list(length=None)

    return {
        "aluno_id": aluno_id,
        "nome": aluno.nome,
        "total_treinos": result[0]["total_treinos"] if result else 0,
    }


async def listar_treinos_por_dia(engine: AIOEngine, dia_da_semana: str):
    """
    Lista os treinos de todos os alunos para um dia específico da semana.

    Args:
        engine (AIOEngine): Instância do banco de dados assíncrono.
        dia_da_semana (str): Nome do dia da semana (ex.: 'Segunda-feira', 'Terça-feira', etc.)

    Returns:
        List[Treino]: Lista de treinos que correspondem ao dia da semana.
    """
    # Aqui você pode usar o campo 'dia_da_semana' (por exemplo, 'Segunda-feira') para filtrar
    return await engine.find(Treino, Treino.dia_semana == dia_da_semana)
