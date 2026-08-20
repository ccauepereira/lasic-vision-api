class ErroRegraNegocio(ValueError):
    """Indica que uma regra de negocio do dominio foi violada."""

    def __init__(self, mensagem: str = "Regra de negocio violada.") -> None:
        super().__init__(mensagem)


class ErroTarefaNaoEncontrada(LookupError):
    """Indica que uma tarefa nao foi localizada."""

    def __init__(self, mensagem: str = "Tarefa nao encontrada.") -> None:
        super().__init__(mensagem)


class ErroImagemInvalida(ValueError):
    """Indica que uma imagem nao atende aos requisitos de analise."""

    def __init__(self, mensagem: str = "Imagem invalida.") -> None:
        super().__init__(mensagem)
