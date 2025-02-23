from odmantic import AIOEngine
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
    return await engine.find(
        Aluno, {"nome": {"$regex": f".*{nome_parcial}.*", "$options": "i"}}
    )


async def get_imc_by_id(engine: AIOEngine, aluno_id) -> dict:
    """
    Busca um aluno pelo id e calcula seu IMC (Índice de Massa Corporal).

    Args:
        engine (AIOEngine): Instância do banco de dados assíncrono.
        aluno_id: ID do aluno.

    Returns:
        dict: Um dicionário contendo o nome, e-mail, peso, altura e IMC do aluno.
              Retorna mensagem de erro se o aluno não for encontrado ou se faltar peso/altura.
    """
    aluno = await engine.find_one(Aluno, Aluno.id == aluno_id)

    if not aluno:
        return {"erro": "Aluno não encontrado."}

    if aluno.peso is None or aluno.altura is None:
        return {"erro": "Peso ou altura não cadastrados para este aluno."}

    imc = aluno.peso / (aluno.altura**2)

    return {"nome": aluno.nome, "imc": round(imc, 2)}


async def get_media_peso_alunos(engine: AIOEngine):
    """
    Calcula a média do peso dos alunos cadastrados.

    Args:
        engine (AIOEngine): Instância do banco de dados assíncrono.

    Returns:
        dict: Um dicionário contendo a média do peso dos alunos.
    """
    pipeline = [{"$group": {"_id": None, "media_peso": {"$avg": "$peso"}}}]

    result = await engine.database["aluno"].aggregate(pipeline).to_list(length=None)

    return {"media_peso": result[0]["media_peso"] if result else 0}
