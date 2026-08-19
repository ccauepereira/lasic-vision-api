from collections import deque
from excecoes import InspecaoError
from inspecao import Inspecao

class SistemaInspecao:
    def __init__(self):
        self.inspecoes = []
        self.inspecoes_por_id = {}
        self.fila_inspecoes = deque()
        self.defeitos_encontrados = set()

    def cadastrar_inspecao(self, inspecao: Inspecao) -> None:
        if inspecao.inspecao_id in self.inspecoes_por_id:
            raise InspecaoError(f"Erro: Inspeção com ID {inspecao.inspecao_id} já cadastrada.")
        
        self.inspecoes.append(inspecao)
        self.inspecoes_por_id[inspecao.inspecao_id] = inspecao
        self.fila_inspecoes.append(inspecao)
        self.defeitos_encontrados.update(inspecao.defeitos)

    def buscar_inspecao(self, inspecao_id: int) -> Inspecao:
        inspecao = self.inspecoes_por_id.get(inspecao_id)
        if not inspecao:
            raise InspecaoError(f"Erro: Inspeção ID {inspecao_id} não encontrada.")
        return inspecao

    def atender_proxima_inspecao(self) -> Inspecao:
        if not self.fila_inspecoes:
            raise InspecaoError("Nenhuma inspeção na fila.")
        inspecao = self.fila_inspecoes.popleft()
        inspecao.iniciar()
        return inspecao

    def executar_todas_as_analises(self) -> list[str]:
        return [insp.executar_analise() for insp in self.inspecoes]

    def listar_inspecoes(self) -> list[str]:
        return [f"Posição {i}: {insp.resumo()}" for i, insp in enumerate(self.inspecoes)]

    def gerar_relatorio(self) -> str:
        return "\n\n".join([insp.resumo() for insp in self.inspecoes])

    def listar_defeitos(self) -> list[str]:
        return sorted(self.defeitos_encontrados)
    
    def resumo(self) -> str:
        return f"Sistema de Inspeção contendo {len(self.inspecoes)} registros ativos."

    def __len__(self) -> int:
        return len(self.inspecoes)