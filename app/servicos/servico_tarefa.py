from uuid import UUID

from app.dominio.entidades.tarefa import Tarefa
from app.dominio.entidades.resultado_analise_imagem import (
    ResultadoAnaliseImagem,
)
from app.dominio.excecoes import ErroTarefaNaoEncontrada
from app.dominio.protocolos import (
    ProtocoloAnalisadorImagem,
    ProtocoloRepositorioTarefa,
)


class ServicoTarefa:
    """Coordena casos de uso de tarefas com dependencias injetadas."""

    def __init__(
        self,
        repositorio_tarefa: ProtocoloRepositorioTarefa,
        analisador_imagem: ProtocoloAnalisadorImagem,
    ) -> None:
        self._repositorio_tarefa = repositorio_tarefa
        self._analisador_imagem = analisador_imagem

    def criar_tarefa(
        self,
        titulo: str,
        descricao: str | None = None,
    ) -> Tarefa:
        tarefa = Tarefa(titulo=titulo, descricao=descricao)
        return self._repositorio_tarefa.salvar(tarefa)

    def listar_tarefas(self) -> list[Tarefa]:
        return self._repositorio_tarefa.listar_todas()

    def buscar_tarefa_por_id(self, tarefa_id: UUID) -> Tarefa:
        tarefa = self._repositorio_tarefa.buscar_por_id(tarefa_id)
        if tarefa is None:
            raise ErroTarefaNaoEncontrada(
                f"Tarefa com identificador {tarefa_id} nao encontrada."
            )
        return tarefa

    def atribuir_responsavel(
        self,
        tarefa_id: UUID,
        responsavel: str,
    ) -> Tarefa:
        tarefa = self.buscar_tarefa_por_id(tarefa_id)
        tarefa.atribuir_responsavel(responsavel)
        return self._repositorio_tarefa.salvar(tarefa)

    def iniciar_tarefa(self, tarefa_id: UUID) -> Tarefa:
        tarefa = self.buscar_tarefa_por_id(tarefa_id)
        tarefa.iniciar()
        return self._repositorio_tarefa.salvar(tarefa)

    def analisar_imagem(
        self,
        tarefa_id: UUID,
        nome_arquivo: str,
        conteudo: bytes,
    ) -> ResultadoAnaliseImagem:
        tarefa = self.buscar_tarefa_por_id(tarefa_id)
        resultado = self._analisador_imagem.analisar(nome_arquivo, conteudo)
        tarefa.registrar_resultado(resultado)
        self._repositorio_tarefa.salvar(tarefa)
        return resultado

    def concluir_tarefa(self, tarefa_id: UUID) -> Tarefa:
        tarefa = self.buscar_tarefa_por_id(tarefa_id)
        tarefa.concluir()
        return self._repositorio_tarefa.salvar(tarefa)
