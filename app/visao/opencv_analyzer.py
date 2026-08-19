from fastapi import HTTPException
import cv2
import numpy as np


class OpenCVAnalyzer:
    EXTENSOES_VALIDAS = (".jpg", ".jpeg", ".png", ".bmp")

    def analisar(self, nome_arquivo: str, conteudo: bytes) -> dict:
        self._validar_extensao(nome_arquivo)

        imagem = self._converter_bytes_para_imagem(conteudo)

        altura, largura, canais = imagem.shape
        imagem_cinza = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)

        brilho_medio = float(np.mean(imagem_cinza))
        contraste_medio = float(np.std(imagem_cinza))

        bordas = cv2.Canny(imagem_cinza, 100, 200)
        quantidade_bordas = int(np.count_nonzero(bordas))

        classificacao_brilho = self._classificar_brilho(brilho_medio)
        classificacao_contraste = self._classificar_contraste(contraste_medio)

        tags_automaticas = self._gerar_tags(
            largura=largura,
            altura=altura,
            brilho_medio=brilho_medio,
            contraste_medio=contraste_medio,
            quantidade_bordas=quantidade_bordas,
        )

        return {
            "arquivo": nome_arquivo,
            "largura": largura,
            "altura": altura,
            "modo_cor": f"BGR com {canais} canais",
            "brilho_medio": round(brilho_medio, 2),
            "contraste_medio": round(contraste_medio, 2),
            "quantidade_bordas": quantidade_bordas,
            "classificacao_brilho": classificacao_brilho,
            "classificacao_contraste": classificacao_contraste,
            "tags_automaticas": tags_automaticas,
        }

    def _validar_extensao(self, nome_arquivo: str) -> None:
        if not nome_arquivo.lower().endswith(self.EXTENSOES_VALIDAS):
            raise HTTPException(
                status_code=400,
                detail="Formato invalido. Envie .jpg, .jpeg, .png ou .bmp.",
            )

    def _converter_bytes_para_imagem(self, conteudo: bytes):
        imagem_array = np.frombuffer(conteudo, np.uint8)
        imagem = cv2.imdecode(imagem_array, cv2.IMREAD_COLOR)

        if imagem is None:
            raise HTTPException(
                status_code=400,
                detail="Nao foi possivel ler a imagem enviada.",
            )

        return imagem

    def _classificar_brilho(self, brilho_medio: float) -> str:
        if brilho_medio < 85:
            return "escura"

        if brilho_medio > 170:
            return "clara"

        return "normal"

    def _classificar_contraste(self, contraste_medio: float) -> str:
        if contraste_medio < 30:
            return "baixo_contraste"

        if contraste_medio > 80:
            return "alto_contraste"

        return "contraste_adequado"

    def _gerar_tags(
        self,
        largura: int,
        altura: int,
        brilho_medio: float,
        contraste_medio: float,
        quantidade_bordas: int,
    ) -> list[str]:
        tags = set()

        total_pixels = largura * altura

        if total_pixels >= 1920 * 1080:
            tags.add("alta_resolucao")
        else:
            tags.add("baixa_resolucao")

        tags.add(self._classificar_brilho(brilho_medio))
        tags.add(self._classificar_contraste(contraste_medio))

        if quantidade_bordas > 10000:
            tags.add("muitas_bordas")
        else:
            tags.add("poucas_bordas")

        return sorted(tags)