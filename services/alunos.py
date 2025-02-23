from odmantic import AIOEngine, query
from models.aluno import Aluno
from typing import List


async def get_alunos_sorted_by_nome(engine: AIOEngine):
    """
    Retorna a lista de alunos ordenada pelo nome.

    Args:
        engine (AIOEngine): Instância do banco de dados assíncrono.

    Returns:
        List[Aluno]: Lista de objetos Aluno ordenados alfabeticamente pelo nome.
    """
    return await engine.find(Aluno, sort=Aluno.nome)


async def count_alunos(engine: AIOEngine):
    """
    Conta o número total de alunos cadastrados no banco de dados.

    Args:
        engine (AIOEngine): Instância do banco de dados assíncrono.

    Returns:
        int: O número total de alunos cadastrados.
    """
    return await engine.count(Aluno)
    

async def search_alunos_by_nome(engine: AIOEngine, nome_parcial: str) -> List[Aluno]:
    """
    Busca alunos cujo nome contém uma string parcial, ignorando maiúsculas e minúsculas.

    Args:
        engine (AIOEngine): Instância do banco de dados assíncrono.
        nome_parcial (str): Parte do nome do aluno para a busca.

    Returns:
        List[Aluno]: Lista de alunos que correspondem à pesquisa.
    """
    return await engine.find(Aluno, {"nome": {"$regex": f".*{nome_parcial}.*", "$options": "i"}})


async def get_media_peso_alunos(engine: AIOEngine):
    """
    Calcula a média do peso dos alunos cadastrados.

    Args:
        engine (AIOEngine): Instância do banco de dados assíncrono.

    Returns:
        dict: Um dicionário contendo a média do peso dos alunos.
    """
    pipeline = [
        {"$group": {"_id": None, "media_peso": {"$avg": "$peso"}}}
    ]
    
    result = await engine.database["aluno"].aggregate(pipeline).to_list(length=None)
    
    return {"media_peso": result[0]["media_peso"] if result else 0}