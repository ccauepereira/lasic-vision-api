class ErroDominio(Exception):
    pass

class TarefaNaoEncontradaErro(ErroDominio):
    def __init__(self, tarefa_id: str) -> None:
        super().__init__(f"Tarefa com id: '{tarefa_id}' não foi encontrada")

class RegraNegocioVioladaErro(ErroDominio):
    pass