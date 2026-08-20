from typing import Protocol
from uuid import UUID

from app.dominio.entidades.resultado_analise_imagem import ResultadoAnaliseImagem
from app.dominio.entidades.tarefa import Tarefa


class ProtocoloRepositorioTarefa(Protocol):
    """Define o contrato de persistencia de tarefas do dominio."""

    def salvar(self, tarefa: Tarefa) -> Tarefa:
        ...

    def buscar_por_id(self, tarefa_id: UUID) -> Tarefa | None:
        ...

    def listar_todas(self) -> list[Tarefa]:
        ...


class ProtocoloAnalisadorImagem(Protocol):
    """Define o contrato para analise de conteudo de imagem."""

    def analisar(
        self,
        nome_arquivo: str,
        conteudo: bytes,
    ) -> ResultadoAnaliseImagem:
        ...
