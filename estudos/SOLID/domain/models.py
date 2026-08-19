from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional
from domain.exceptions import RegraNegocioVioladaErro

class StatusTarefa(str, Enum):
    CRIADA = "CRIADA"
    EM_ANDAMENTO = "EM_ANDAMENTO"
    CONCLUIDA = "CONCLUIDA"
    FALHA = "FALHA"

@dataclass(frozen=True)
class ResultadoAnaliseImagem:
    quant_objetos_detectados: int
    taxa_confianca_media: float
    detalhes: str
    processada_em: datetime = field(default_factory=datetime.utcnow)

@dataclass
class Tarefa:
    id: str
    nome: str
    caminho_imagem: str
    status: StatusTarefa = StatusTarefa.CRIADA
    responsavel: Optional[str] = None
    resultado_analise: Optional[ResultadoAnaliseImagem] = None
    criado_em: datetime = field(default_factory=datetime.utcnow)

    def atribuir_responsavel(self, responsavel: str) -> None:
        if not responsavel or not responsavel.strip():
            raise RegraNegocioVioladaErro("O responsável não pode ser vazio ou nulo.")
        self.responsavel = responsavel.strip()

    def iniciar(self) -> None:
        if self.status != StatusTarefa.CRIADA:
            raise RegraNegocioVioladaErro(
                f"Transição inválida: tarefa no status '{self.status.value}' não pode ser iniciada."
            )
        if not self.responsavel:
            raise RegraNegocioVioladaErro("A tarefa requer um responsável antes de ser iniciada.")
        self.status = StatusTarefa.EM_ANDAMENTO

    def registrar_resultado(self, resultado: ResultadoAnaliseImagem) -> None:
        if self.status != StatusTarefa.EM_ANDAMENTO:
            raise RegraNegocioVioladaErro(
                f"Não é possível registrar resultado em uma tarefa com status '{self.status.value}'."
            )
        self.resultado_analise = resultado

    def concluir(self) -> None:
        if self.status != StatusTarefa.EM_ANDAMENTO:
            raise RegraNegocioVioladaErro(
                f"Transição inválida: tarefa no status '{self.status.value}' não pode ser concluída."
            )
        if self.resultado_analise is None:
            raise RegraNegocioVioladaErro(
                "A tarefa não pode ser concluída sem um resultado de análise previamente registrado."
            )
        self.status = StatusTarefa.CONCLUIDA