from dataclasses import dataclass, field

@dataclass
class Imagem:
    arquivo: str
    largura: int
    altura: int
    formato: str
    tags: set[str] = field(default_factory=set)
    caracteristicas: dict[str, float] = field(default_factory=dict)

    @classmethod
    def de_resolucao(cls, arquivo: str, resolucao: tuple[int, int], formato: str):
        largura, altura = resolucao
        return cls(arquivo, largura, altura, formato)

    @staticmethod
    def dimensoes_validas(largura: int, altura: int) -> bool:
        return largura > 0 and altura > 0

    @property
    def dimensoes(self) -> tuple[int, int]:
        return self.largura, self.altura

    @property
    def quantidade_pixels(self) -> int:
        return self.largura * self.altura

    def adicionar_tag(self, tag: str) -> None:
        if tag and tag.strip():
            self.tags.add(tag.strip().lower())

    def registrar_caracteristica(self, nome: str, valor: float) -> None:
        if nome and nome.strip():
            self.caracteristicas[nome.strip().lower()] = float(valor)

    def resumo(self) -> str:
        tags_str = ", ".join(sorted(self.tags)) if self.tags else "Nenhuma"
        return f"Imagem: {self.arquivo} | {self.largura}x{self.altura} | Tags: {tags_str}"

    def __str__(self) -> str:
        return f"Arquivo de Imagem {self.arquivo} ({self.largura}x{self.altura})"