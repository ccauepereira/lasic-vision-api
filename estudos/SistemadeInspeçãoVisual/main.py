from imagem import Imagem
from heranca_inspecao import InspecaoCelular, InspecaoSuperficie, InspecaoDimensional
from sistema import SistemaInspecao
from excecoes import InspecaoError
from protocolos import imprimir_resumo

def main():
    print("=== INICIANDO FÁBRICA 2.0 ===\n")

    try:
        # 1. Validar dimensões usando staticmethod
        if not Imagem.dimensoes_validas(1920, 1080):
            raise ValueError("Dimensões incorretas.")

        # 2. Criar as imagens usando classmethod
        img1 = Imagem.de_resolucao("componente_01.png", (1920, 1080), "RGB")
        img2 = Imagem.de_resolucao("componente_02.png", (3840, 2160), "RGB")
        img3 = Imagem.de_resolucao("componente_03.png", (1280, 720), "RGB")

        # 3. Adicionar tags (testando set: não deve repetir 'celula')
        img1.adicionar_tag("celula")
        img1.adicionar_tag("CELULA")
        img2.adicionar_tag("metal")
        img3.adicionar_tag("3d")

        # 4. Registrar características
        img1.registrar_caracteristica("brilho", 80)
        img1.registrar_caracteristica("contraste", 65)
        img1.registrar_caracteristica("quantidade_contornos", 12)

        img2.registrar_caracteristica("brilho", 55)
        img2.registrar_caracteristica("contraste", 90)
        img2.registrar_caracteristica("quantidade_contornos", 20)

        img3.registrar_caracteristica("brilho", 70)
        img3.registrar_caracteristica("contraste", 75)
        img3.registrar_caracteristica("quantidade_contornos", 8)

        # 5. Criar as inspeções
        insp1 = InspecaoCelular(1, "Placa de circuito", img1)
        insp2 = InspecaoSuperficie(2, "Componente metálico", img2)
        insp3 = InspecaoDimensional(3, "Peça impressa em 3D", img3)

        # 6. Atribuir técnicos e defeitos
        insp1.tecnico = "Cauê"
        insp1.registrar_defeito("ruido")
        insp1.registrar_defeito("mancha")

        insp2.tecnico = "Ana"
        insp2.registrar_defeito("fissura")

        insp3.tecnico = "João"
        insp3.registrar_defeito("deformacao")
        insp3.registrar_defeito("mancha")

        # 7. Cadastrar todas no sistema
        sistema = SistemaInspecao()
        sistema.cadastrar_inspecao(insp1)
        sistema.cadastrar_inspecao(insp2)
        sistema.cadastrar_inspecao(insp3)

        # 8 & 9. Imprimir resumo de uma Imagem e de uma Inspecao (Duck Typing)
        print("--- TESTE DE PROTOCOL (DUCK TYPING) ---")
        imprimir_resumo(img1)
        imprimir_resumo(insp1)
        imprimir_resumo(sistema)
        print("\n")

        # 11. Executar todas as análises usando polimorfismo
        print("--- TESTE DE POLIMORFISMO ---")
        resultados = sistema.executar_todas_as_analises()
        for res in resultados:
            print(res)
        print("\n")

        # 12, 13 & 14. Fila, Aprovar e Reprovar
        print("--- FLUXO DE FILA E STATUS ---")
        atendida = sistema.atender_proxima_inspecao()
        print(f"Atendida 1ª da fila: {atendida.componente} -> Novo Status: {atendida.status}")
        
        insp1.aprovar()
        insp2.reprovar()
        print(f"Status Final -> Insp1: {insp1.status} | Insp2: {insp2.status}\n")

        # 15. Buscar a inspeção de ID 2
        print("--- BUSCA POR ID ---")
        busca = sistema.buscar_inspecao(2)
        print(busca.resumo(), "\n")

        # 16. Ordenar as inspeções (usa __lt__)
        print("--- ORDENAÇÃO (ALFABÉTICA) ---")
        ordenadas = sorted(sistema.inspecoes)
        for ins in ordenadas:
            print(ins.componente)
        print("\n")

        # 17. Testar igualdade (usa __eq__)
        print(f"Teste de Igualdade (insp1 == insp1): {insp1 == insp1}")
        
        # 18. Mostrar len(sistema)
        print(f"Tamanho do sistema (len): {len(sistema)}\n")

        # 19. Listar todos os defeitos únicos
        print("--- DEFEITOS ÚNICOS ENCONTRADOS ---")
        print(sistema.listar_defeitos(), "\n")

        # 20. Gerar relatório final
        print("--- RELATÓRIO FINAL ---")
        print(sistema.gerar_relatorio())
        print("\n")

        # 21 & 22. Tentativas de erros para testar exceções
        print("--- TESTANDO EXCEÇÕES ---")
        try:
            sistema.cadastrar_inspecao(insp1)
        except InspecaoError as e:
            print(f"Falha ao cadastrar: {e}")

        try:
            insp3.status = "status_inventado"
        except InspecaoError as e:
            print(f"Falha de status: {e}")

    except Exception as e:
        print(f"ERRO CRÍTICO NÃO TRATADO: {e}")

if __name__ == "__main__":
    main()