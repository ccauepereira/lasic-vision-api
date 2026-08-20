from dataclasses import dataclass, field
from datetime import datetime, timezone


def _agora_utc() -> datetime:
    return datetime.now(timezone.utc)


@dataclass(frozen=True)
class ResultadoAnaliseImagem:
    """Value Object imutavel com os dados produzidos por uma analise."""

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
    tags_automaticas: tuple[str, ...] = field(default_factory=tuple)
    criado_em: datetime = field(default_factory=_agora_utc)

    def __post_init__(self) -> None:
        object.__setattr__(self, "tags_automaticas", tuple(self.tags_automaticas))

        if self.criado_em.tzinfo is None:
            object.__setattr__(
                self,
                "criado_em",
                self.criado_em.replace(tzinfo=timezone.utc),
            )
        else:
            object.__setattr__(
                self,
                "criado_em",
                self.criado_em.astimezone(timezone.utc),
            )
