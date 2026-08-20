from datetime import datetime

from pydantic import BaseModel, ConfigDict


class RespostaAnaliseImagem(BaseModel):
    """Representa os dados de analise retornados pela API."""

    model_config = ConfigDict(from_attributes=True)

    nome_arquivo: str
    largura: int
    altura: int
    formato: str
    modo_cor: str
    brilho_medio: float
    contraste_medio: float
    classificacao_brilho: str
    classificacao_contraste: str
    quantidade_bordas: int
    tags_automaticas: list[str]
    criado_em: datetime
