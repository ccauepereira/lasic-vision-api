from typing import Dict, List, Optional
from domain.models import Tarefa
from domain.protocols import TarefaRepositoryProtocol

class TarefaRepositoryMemoria(TarefaRepositoryProtocol):
    def __init__(self) -> None:
        self._armazenamento: Dict[str, Tarefa] = {}

    def salvar(self, tarefa: Tarefa) -> Tarefa:
        self._armazenamento[tarefa.id] = tarefa
        return tarefa

    def buscar_por_id(self, tarefa_id: str) -> Optional[Tarefa]:
        return self._armazenamento.get(tarefa_id)

    def listar_todas(self) -> List[Tarefa]:
        return list(self._armazenamento.values())