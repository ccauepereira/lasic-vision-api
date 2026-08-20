from uuid import UUID

from fastapi import APIRouter, Depends, File, UploadFile, status
from sqlalchemy.orm import Session

from app.banco.conexao import obter_sessao
from app.esquemas.analise_imagem import RespostaAnaliseImagem
from app.esquemas.tarefa import (
    AtualizarResponsavelRequisicao,
    CriarTarefaRequisicao,
    RespostaTarefa,
)
from app.repositorios.sqlite.repositorio_tarefa_sqlite import (
    RepositorioTarefaSQLite,
)
from app.servicos.servico_tarefa import ServicoTarefa
from app.visao.analisador_imagem_opencv import AnalisadorImagemOpenCV


router = APIRouter(prefix="/tarefas", tags=["Tarefas"])

RESPOSTAS_TAREFA_NAO_ENCONTRADA = {
    404: {"description": "Tarefa nao encontrada."},
}
RESPOSTAS_ERRO_REGRA_NEGOCIO = {
    404: {"description": "Tarefa nao encontrada."},
    409: {"description": "Regra de negocio violada."},
}
RESPOSTAS_ERRO_ANALISE_IMAGEM = {
    400: {"description": "Imagem invalida."},
    404: {"description": "Tarefa nao encontrada."},
    409: {"description": "Regra de negocio violada."},
}


def obter_servico_tarefa(
    sessao: Session = Depends(obter_sessao),
) -> ServicoTarefa:
    """Monta as dependencias de uma requisicao de tarefas."""
    return ServicoTarefa(
        repositorio_tarefa=RepositorioTarefaSQLite(sessao),
        analisador_imagem=AnalisadorImagemOpenCV(),
    )


@router.post(
    "",
    response_model=RespostaTarefa,
    status_code=status.HTTP_201_CREATED,
    summary="Cria uma tarefa",
    description="Registra uma nova tarefa de analise de imagem como pendente.",
    response_description="Tarefa criada.",
)
def criar_tarefa(
    requisicao: CriarTarefaRequisicao,
    servico_tarefa: ServicoTarefa = Depends(obter_servico_tarefa),
) -> RespostaTarefa:
    return servico_tarefa.criar_tarefa(
        titulo=requisicao.titulo,
        descricao=requisicao.descricao,
    )


@router.get(
    "",
    response_model=list[RespostaTarefa],
    summary="Lista as tarefas",
    description="Retorna as tarefas registradas em ordem de criacao.",
    response_description="Tarefas encontradas.",
)
def listar_tarefas(
    servico_tarefa: ServicoTarefa = Depends(obter_servico_tarefa),
) -> list[RespostaTarefa]:
    return servico_tarefa.listar_tarefas()


@router.get(
    "/{tarefa_id}",
    response_model=RespostaTarefa,
    summary="Busca uma tarefa",
    description="Retorna uma tarefa pelo seu identificador.",
    response_description="Tarefa encontrada.",
    responses=RESPOSTAS_TAREFA_NAO_ENCONTRADA,
)
def buscar_tarefa(
    tarefa_id: UUID,
    servico_tarefa: ServicoTarefa = Depends(obter_servico_tarefa),
) -> RespostaTarefa:
    return servico_tarefa.buscar_tarefa_por_id(tarefa_id)


@router.patch(
    "/{tarefa_id}/responsavel",
    response_model=RespostaTarefa,
    summary="Atribui um responsavel",
    description="Atribui ou altera o responsavel de uma tarefa pendente.",
    response_description="Tarefa atualizada.",
    responses=RESPOSTAS_ERRO_REGRA_NEGOCIO,
)
def atualizar_responsavel(
    tarefa_id: UUID,
    requisicao: AtualizarResponsavelRequisicao,
    servico_tarefa: ServicoTarefa = Depends(obter_servico_tarefa),
) -> RespostaTarefa:
    return servico_tarefa.atribuir_responsavel(
        tarefa_id=tarefa_id,
        responsavel=requisicao.responsavel,
    )


@router.post(
    "/{tarefa_id}/iniciar",
    response_model=RespostaTarefa,
    summary="Inicia uma tarefa",
    description="Inicia uma tarefa pendente que possui responsavel atribuido.",
    response_description="Tarefa iniciada.",
    responses=RESPOSTAS_ERRO_REGRA_NEGOCIO,
)
def iniciar_tarefa(
    tarefa_id: UUID,
    servico_tarefa: ServicoTarefa = Depends(obter_servico_tarefa),
) -> RespostaTarefa:
    return servico_tarefa.iniciar_tarefa(tarefa_id)


@router.post(
    "/{tarefa_id}/analises/imagem",
    response_model=RespostaAnaliseImagem,
    summary="Analisa uma imagem da tarefa",
    description=(
        "Envia uma imagem .jpg, .jpeg, .png ou .bmp para a tarefa em andamento."
    ),
    response_description="Resultado da analise de imagem.",
    responses=RESPOSTAS_ERRO_ANALISE_IMAGEM,
)
async def analisar_imagem(
    tarefa_id: UUID,
    arquivo: UploadFile = File(
        description="Arquivo de imagem nos formatos .jpg, .jpeg, .png ou .bmp."
    ),
    servico_tarefa: ServicoTarefa = Depends(obter_servico_tarefa),
) -> RespostaAnaliseImagem:
    return servico_tarefa.analisar_imagem(
        tarefa_id=tarefa_id,
        nome_arquivo=arquivo.filename or "",
        conteudo=await arquivo.read(),
    )


@router.post(
    "/{tarefa_id}/concluir",
    response_model=RespostaTarefa,
    summary="Conclui uma tarefa",
    description="Conclui uma tarefa em andamento que possui resultado de analise.",
    response_description="Tarefa concluida.",
    responses=RESPOSTAS_ERRO_REGRA_NEGOCIO,
)
def concluir_tarefa(
    tarefa_id: UUID,
    servico_tarefa: ServicoTarefa = Depends(obter_servico_tarefa),
) -> RespostaTarefa:
    return servico_tarefa.concluir_tarefa(tarefa_id)
