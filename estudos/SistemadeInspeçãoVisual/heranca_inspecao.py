from inspecao import Inspecao

class InspecaoCelular(Inspecao):
    def executar_analise(self) -> str:
        contornos = self.imagem.caracteristicas.get("quantidade_contornos", 0)
        return f"Análise celular executada. Contornos: {contornos}"

class InspecaoSuperficie(Inspecao):
    def executar_analise(self) -> str:
        brilho = self.imagem.caracteristicas.get("brilho", 0)
        contraste = self.imagem.caracteristicas.get("contraste", 0)
        return f"Análise de superfície executada. Brilho: {brilho}, Contraste: {contraste}"

class InspecaoDimensional(Inspecao):
    def executar_analise(self) -> str:
        w, h = self.imagem.dimensoes
        pixels = self.imagem.quantidade_pixels
        return f"Análise dimensional executada. Tamanho: {w}x{h} ({pixels} pixels)"