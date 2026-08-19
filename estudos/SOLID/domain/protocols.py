from typing import Optional, Protocol, List
from domain.models import Tarefa, ResultadoAnaliseImagem

class AnalisadorImagemProtocol(Protocol):
    def analisar(self, caminho_imagem: str) -> ResultadoAnaliseImagem:
        ...

class TarefaRepositoryProtocol(Protocol):
    def salvar(self, tarefa: Tarefa) -> Tarefa:
        ...

    def buscar_por_id(self, tarefa_id: str) -> Optional[Tarefa]:
        ...

    def listar_todas(self) -> List[Tarefa]:
        ...