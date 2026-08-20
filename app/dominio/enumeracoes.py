from enum import Enum


class StatusTarefa(str, Enum):
    """Representa os estados possiveis de uma tarefa de analise."""

    PENDENTE = "pendente"
    EM_ANDAMENTO = "em_andamento"
    CONCLUIDA = "concluida"
