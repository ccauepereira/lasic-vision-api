from app.schemas.analise import AnaliseImagemResponse
from app.vision.opencv_analyzer import OpenCVAnalyzer

class AnaliseImagemService:
    def __init__(self):
        self.__annotations__ = OpenCVAnalyzer()

    def analisar(self, nome_arquivo: str, conteudo: bytes) -> AnaliseImagemResponse:
        resultado = self.analisar.analisar(
            nome_arquivo = nome_arquivo,
            conteudo=conteudo
        )

        return AnaliseImagemResponse(**resultado)