import uuid
from typing import List
from domain.models import Tarefa
from domain.protocols import TarefaRepositoryProtocol, AnalisadorImagemProtocol
from domain.exceptions import TarefaNaoEncontradaErro


class TarefaService:
    def __init__(
        self,
        repository: TarefaRepositoryProtocol,
        analisador: AnalisadorImagemProtocol
    ) -> None:
        self.repository = repository
        self.analisador = analisador

    def criar_tarefa(self, nome: str, caminho_imagem: str) -> Tarefa:
        nova_tarefa = Tarefa(
            id=str(uuid.uuid4())[:8],
            nome=nome,
            caminho_imagem=caminho_imagem
        )
        return self.repository.salvar(nova_tarefa)

    def atribuir_responsavel(self, tarefa_id: str, responsavel: str) -> Tarefa:
        tarefa = self._obter_tarefa_existente(tarefa_id)
        tarefa.atribuir_responsavel(responsavel)
        return self.repository.salvar(tarefa)

    def iniciar_tarefa(self, tarefa_id: str) -> Tarefa:
        tarefa = self._obter_tarefa_existente(tarefa_id)
        tarefa.iniciar()
        return self.repository.salvar(tarefa)

    def registrar_resultado_analise(self, tarefa_id: str) -> Tarefa:
        tarefa = self._obter_tarefa_existente(tarefa_id)
        resultado = self.analisador.analisar(tarefa.caminho_imagem)
        tarefa.registrar_resultado(resultado)
        return self.repository.salvar(tarefa)

    def concluir_tarefa(self, tarefa_id: str) -> Tarefa:
        tarefa = self._obter_tarefa_existente(tarefa_id)
        tarefa.concluir()
        return self.repository.salvar(tarefa)

    def listar_tarefas(self) -> List[Tarefa]:
        return self.repository.listar_todas()

    def _obter_tarefa_existente(self, tarefa_id: str) -> Tarefa:
        tarefa = self.repository.buscar_por_id(tarefa_id)
        if not tarefa:
            raise TarefaNaoEncontradaErro(tarefa_id)
        return tarefa