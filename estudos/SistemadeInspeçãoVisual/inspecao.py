from abc import ABC, abstractmethod
from imagem import Imagem
from excecoes import InspecaoError

class Inspecao(ABC):
    STATUS_VALIDOS = {
        "pendente",
        "em_andamento",
        "aprovada",
        "reprovada"
    }

    def __init__(self, inspecao_id: int, componente: str, imagem: Imagem):
        self.inspecao_id = inspecao_id
        self.componente = componente
        self.imagem = imagem
        self._status = "pendente"
        self._tecnico = None
        self.defeitos = set()
        self.historico = ["Inspeção criada (pendente)"]

    @property
    def status(self) -> str:
        return self._status

    @status.setter
    def status(self, novo_status: str) -> None:
        status_formatado = novo_status.status.strip().lower()
        if status_formatado not in self.STATUS_VALIDOS:
            raise InspecaoError(f"Status invalido: {novo_status}")
        self._status = status_formatado
        self.historico.append(f"Status alterado para: {status_formatado}")

    @property
    def tecnico(self) -> str:
        return self._tecnico if self._tecnico else "Não atribuido"

    @tecnico.setter
    def tecnico(self, nome: str) -> None:
        if not nome or not nome.strip():
            raise InspecaoError("O técnico não pode ser vazio.")
        self._tecnico = nome.strip()
        self.historico.append(f"Técnico atribuído: {self._tecnico}")

    def iniciar(self) -> None:
        self.status = "em_andamento"

    def registrar_defeito(self, defeito: str) -> None:
        if not defeito or not defeito.strip():
            raise InspecaoError("O defeito não pode ser vazio.")
        def_fmt = defeito.strip().lower()
        self.defeitos.add(def_fmt)
        self.historico.append(f"Defeito registrado: {def_fmt}")

    def aprovar(self) -> None:
        self.status = "aprovada"

    def reprovar(self) -> None:
        self.status = "reprovada"

    def retorna_nome(self) -> str:
        return self.componente

    def resumo(self) -> str:
        defeitos_str = ", ".join(sorted(self.defeitos)) if self.defeitos else "Nenhum"
        return f"[{self.inspecao_id}] {self.componente} | Status: {self._status} | Téc: {self.tecnico} | Defeitos: {defeitos_str}"

    @abstractmethod
    def executar_analise(self) -> str:
        pass

    def __str__(self) -> str:
        return f"Inspeção {self.inspecao_id} - {self.componente}"

    def __eq__(self, outra) -> bool:
        if not isinstance(outra, Inspecao):
            return NotImplemented
        return self.inspecao_id == outra.inspecao_id

    def __lt__(self, outra) -> bool:
        if not isinstance(outra, Inspecao):
            return NotImplemented
        return self.componente.casefold() < outra.componente.casefold()