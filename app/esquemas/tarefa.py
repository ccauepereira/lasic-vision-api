from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, field_validator

from app.dominio.enumeracoes import StatusTarefa
from app.esquemas.analise_imagem import RespostaAnaliseImagem


class CriarTarefaRequisicao(BaseModel):
    """Define os dados aceitos para criar uma tarefa."""

    titulo: str
    descricao: str | None = None

    @field_validator("titulo")
    @classmethod
    def validar_titulo(cls, titulo: str) -> str:
        titulo_normalizado = titulo.strip()
        if not titulo_normalizado:
            raise ValueError("O titulo nao pode ser vazio.")
        return titulo_normalizado

    @field_validator("descricao")
    @classmethod
    def normalizar_descricao(cls, descricao: str | None) -> str | None:
        if descricao is None:
            return None

        descricao_normalizada = descricao.strip()
        return descricao_normalizada or None


class AtualizarResponsavelRequisicao(BaseModel):
    """Define os dados aceitos para atribuir um responsavel a uma tarefa."""

    responsavel: str

    @field_validator("responsavel")
    @classmethod
    def validar_responsavel(cls, responsavel: str) -> str:
        responsavel_normalizado = responsavel.strip()
        if not responsavel_normalizado:
            raise ValueError("O responsavel nao pode ser vazio.")
        return responsavel_normalizado


class RespostaTarefa(BaseModel):
    """Representa uma tarefa e seu resultado de analise, quando existente."""

    model_config = ConfigDict(from_attributes=True)

    tarefa_id: UUID
    titulo: str
    descricao: str | None
    responsavel: str | None
    status: StatusTarefa
    resultado_analise: RespostaAnaliseImagem | None = None
    criado_em: datetime
    atualizado_em: datetime
