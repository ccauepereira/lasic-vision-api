from pathlib import Path

import cv2
import numpy as np

from app.dominio.entidades.resultado_analise_imagem import (
    ResultadoAnaliseImagem,
)
from app.dominio.excecoes import ErroImagemInvalida
from app.dominio.protocolos import ProtocoloAnalisadorImagem


class AnalisadorImagemOpenCV(ProtocoloAnalisadorImagem):
    """Extrai metricas objetivas de uma imagem usando OpenCV e NumPy."""

    EXTENSOES_PERMITIDAS = frozenset({".jpg", ".jpeg", ".png", ".bmp"})

    def analisar(
        self,
        nome_arquivo: str,
        conteudo: bytes,
    ) -> ResultadoAnaliseImagem:
        extensao = self._validar_arquivo(nome_arquivo, conteudo)
        imagem = self._decodificar_imagem(conteudo)
        altura, largura = imagem.shape[:2]
        imagem_cinza, modo_cor = self._converter_para_cinza(imagem)

        brilho_medio = float(np.mean(imagem_cinza))
        contraste_medio = float(np.std(imagem_cinza))
        bordas = cv2.Canny(imagem_cinza, 100, 200)
        quantidade_bordas = int(np.count_nonzero(bordas))
        classificacao_brilho = self._classificar_brilho(brilho_medio)
        classificacao_contraste = self._classificar_contraste(contraste_medio)

        return ResultadoAnaliseImagem(
            nome_arquivo=nome_arquivo,
            largura=largura,
            altura=altura,
            formato=extensao.removeprefix(".").upper(),
            modo_cor=modo_cor,
            brilho_medio=round(brilho_medio, 2),
            contraste_medio=round(contraste_medio, 2),
            classificacao_brilho=classificacao_brilho,
            classificacao_contraste=classificacao_contraste,
            quantidade_bordas=quantidade_bordas,
            tags_automaticas=tuple(
                self._gerar_tags(
                    largura=largura,
                    altura=altura,
                    classificacao_brilho=classificacao_brilho,
                    classificacao_contraste=classificacao_contraste,
                    quantidade_bordas=quantidade_bordas,
                )
            ),
        )

    def _validar_arquivo(self, nome_arquivo: str, conteudo: bytes) -> str:
        extensao = Path(nome_arquivo).suffix.lower()
        if extensao not in self.EXTENSOES_PERMITIDAS:
            raise ErroImagemInvalida(
                "Formato invalido. Envie uma imagem .jpg, .jpeg, .png ou .bmp."
            )

        if not conteudo:
            raise ErroImagemInvalida("O arquivo de imagem esta vazio.")

        return extensao

    @staticmethod
    def _decodificar_imagem(conteudo: bytes) -> np.ndarray:
        imagem = cv2.imdecode(
            np.frombuffer(conteudo, dtype=np.uint8),
            cv2.IMREAD_UNCHANGED,
        )
        if imagem is None:
            raise ErroImagemInvalida("Nao foi possivel ler a imagem enviada.")
        return imagem

    @staticmethod
    def _converter_para_cinza(imagem: np.ndarray) -> tuple[np.ndarray, str]:
        if imagem.ndim == 2:
            return imagem, "tons_de_cinza"

        quantidade_canais = imagem.shape[2]
        if quantidade_canais == 3:
            return cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY), "BGR"
        if quantidade_canais == 4:
            return cv2.cvtColor(imagem, cv2.COLOR_BGRA2GRAY), "BGRA"

        raise ErroImagemInvalida("A imagem possui um modo de cor nao suportado.")

    @staticmethod
    def _classificar_brilho(brilho_medio: float) -> str:
        if brilho_medio < 85:
            return "escura"
        if brilho_medio > 170:
            return "clara"
        return "normal"

    @staticmethod
    def _classificar_contraste(contraste_medio: float) -> str:
        if contraste_medio < 30:
            return "baixo_contraste"
        if contraste_medio > 80:
            return "alto_contraste"
        return "contraste_adequado"

    @staticmethod
    def _gerar_tags(
        largura: int,
        altura: int,
        classificacao_brilho: str,
        classificacao_contraste: str,
        quantidade_bordas: int,
    ) -> list[str]:
        tags = {
            "alta_resolucao" if largura * altura >= 1920 * 1080 else "baixa_resolucao",
            classificacao_brilho,
            classificacao_contraste,
            "muitas_bordas" if quantidade_bordas > 10000 else "poucas_bordas",
        }
        return sorted(tags)
