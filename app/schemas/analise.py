from pydantic import BaseModel

class AnaliseImagemResponse(BaseModel):
    arquivo: str
    largura: int
    altura: int
    modo_cor: str
    brilho_medio: float
    contraste_medio: float
    quantidade_bordas: int
    classificacao_brilho: str
    classificacao_contraste: str
    tags_automaticas: list[str]