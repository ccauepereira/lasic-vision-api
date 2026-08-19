from typing import Protocol

class Resumivel(Protocol):
    def resumo(self)->str:
        ...

def imprimir_resumo(objeto: Resumivel) -> None:
    print(objeto.resumo())