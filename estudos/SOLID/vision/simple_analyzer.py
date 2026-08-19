from domain.models import ResultadoAnaliseImagem
from domain.protocols import AnalisadorImagemProtocol
from domain.exceptions import RegraNegocioVioladaErro


class AnalisadorImagemSimples(AnalisadorImagemProtocol):
    EXTENSOES_VALIDAS = (".jpg", ".jpeg", ".png", ".bmp")

    def analisar(self, caminho_imagem: str) -> ResultadoAnaliseImagem:
        if not caminho_imagem.lower().endswith(self.EXTENSOES_VALIDAS):
            raise RegraNegocioVioladaErro(
                f"Extensão de arquivo inválida: '{caminho_imagem}'"
            )

        return ResultadoAnaliseImagem(
            qtd_objetos_detectados=5,
            taxa_confianca_media=0.975,
            detalhes="5 defeitos superficiais identificados na placa."
        )