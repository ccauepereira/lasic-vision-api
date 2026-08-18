from collections import deque

from tarefa import Tarefa


class Laboratorio:
    def __init__(self):
        self.tarefas = []
        self.tarefas_por_id = {}
        self.tags_cadastradas = set()
        self.fila_pendentes = deque()

    def cadastrar_tarefa(self, tarefa: Tarefa):
        if tarefa.tarefa_id in self.tarefas_por_id:
            raise ValueError(
                f"Tarefa com ID {tarefa.tarefa_id} ja cadastrada"
            )

        self.tarefas.append(tarefa)
        self.tarefas_por_id[tarefa.tarefa_id] = tarefa
        self.fila_pendentes.append(tarefa)
        self.tags_cadastradas.update(tarefa.tags)

    def buscar_tarefa(self, tarefa_id: int):
        tarefa = self.tarefas_por_id.get(tarefa_id)

        if tarefa is None:
            return "Tarefa nao encontrada"

        return tarefa

    def listar_tarefas(self):
        tarefas_formatadas = []

        for indice, tarefa in enumerate(self.tarefas, start=1):
            tarefas_formatadas.append(
                f"Tarefa {indice}\n{tarefa.resumo()}"
            )

        return tarefas_formatadas

    def gerar_relatorio(self):
        tarefas = self.listar_tarefas()

        if not tarefas:
            return "Nenhuma tarefa cadastrada"

        return "\n\n".join(tarefas)

    def atender_proxima_tarefa(self):
        if not self.fila_pendentes:
            return "Nenhuma tarefa pendente"

        tarefa = self.fila_pendentes.popleft()
        tarefa.iniciar()

        return tarefa

    def listar_tags(self):
        return sorted(self.tags_cadastradas)