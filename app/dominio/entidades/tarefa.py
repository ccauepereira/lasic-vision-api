from dataclasses import dataclass, field
from datetime import datetime, timezone
from uuid import UUID, uuid4

from app.dominio.entidades.resultado_analise_imagem import ResultadoAnaliseImagem
from app.dominio.enumeracoes import StatusTarefa
from app.dominio.excecoes import ErroRegraNegocio


def _agora_utc() -> datetime:
    return datetime.now(timezone.utc)


@dataclass
class Tarefa:
    """Entidade que controla o ciclo de vida de uma analise de imagem."""

    titulo: str
    descricao: str | None = None
    tarefa_id: UUID = field(default_factory=uuid4)
    responsavel: str | None = None
    status: StatusTarefa = field(default=StatusTarefa.PENDENTE, init=False)
    resultado_analise: ResultadoAnaliseImagem | None = None
    criado_em: datetime = field(default_factory=_agora_utc)
    atualizado_em: datetime = field(default_factory=_agora_utc)

    def __post_init__(self) -> None:
        self.titulo = self._normalizar_texto_obrigatorio(self.titulo, "titulo")
        self.descricao = self._normalizar_descricao(self.descricao)

        if self.resultado_analise is not None:
            raise ErroRegraNegocio(
                "Uma nova tarefa nao pode possuir resultado de analise."
            )

        if self.responsavel is not None:
            self.responsavel = self._normalizar_texto_obrigatorio(
                self.responsavel,
                "responsavel",
            )

        self.criado_em = self._em_utc(self.criado_em)
        self.atualizado_em = self._em_utc(self.atualizado_em)

    def atribuir_responsavel(self, responsavel: str) -> None:
        """Atribui ou altera o responsavel enquanto a tarefa esta pendente."""
        self._garantir_pendente("atribuir ou alterar o responsavel")
        self.responsavel = self._normalizar_texto_obrigatorio(
            responsavel,
            "responsavel",
        )
        self._atualizar_data()

    def iniciar(self) -> None:
        """Inicia a tarefa quando ja existe um responsavel atribuido."""
        self._garantir_pendente("iniciar a tarefa")

        if self.responsavel is None:
            raise ErroRegraNegocio(
                "A tarefa precisa de um responsavel antes de ser iniciada."
            )

        self.status = StatusTarefa.EM_ANDAMENTO
        self._atualizar_data()

    def registrar_resultado(self, resultado: ResultadoAnaliseImagem) -> None:
        """Registra o unico resultado permitido durante o andamento."""
        if self.status is not StatusTarefa.EM_ANDAMENTO:
            raise ErroRegraNegocio(
                "O resultado so pode ser registrado em uma tarefa em andamento."
            )

        if self.resultado_analise is not None:
            raise ErroRegraNegocio(
                "A tarefa ja possui um resultado de analise registrado."
            )

        self.resultado_analise = resultado
        self._atualizar_data()

    def concluir(self) -> None:
        """Conclui a tarefa quando o resultado de analise ja foi registrado."""
        if self.status is not StatusTarefa.EM_ANDAMENTO:
            raise ErroRegraNegocio(
                "Apenas tarefas em andamento podem ser concluidas."
            )

        if self.resultado_analise is None:
            raise ErroRegraNegocio(
                "A tarefa precisa de um resultado antes de ser concluida."
            )

        self.status = StatusTarefa.CONCLUIDA
        self._atualizar_data()

    def _garantir_pendente(self, acao: str) -> None:
        if self.status is not StatusTarefa.PENDENTE:
            raise ErroRegraNegocio(
                f"Nao e permitido {acao} quando a tarefa nao esta pendente."
            )

    def _atualizar_data(self) -> None:
        self.atualizado_em = _agora_utc()

    @staticmethod
    def _normalizar_texto_obrigatorio(valor: str, campo: str) -> str:
        valor_normalizado = valor.strip()
        if not valor_normalizado:
            raise ErroRegraNegocio(f"O campo {campo} nao pode ser vazio.")
        return valor_normalizado

    @staticmethod
    def _normalizar_descricao(descricao: str | None) -> str | None:
        if descricao is None:
            return None

        descricao_normalizada = descricao.strip()
        return descricao_normalizada or None

    @staticmethod
    def _em_utc(data: datetime) -> datetime:
        if data.tzinfo is None:
            return data.replace(tzinfo=timezone.utc)
        return data.astimezone(timezone.utc)
