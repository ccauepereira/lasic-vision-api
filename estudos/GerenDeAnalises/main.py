from laboratorio import Laboratorio
from tarefa import Tarefa


def main():
    print("=== SISTEMA DE ANALISES DO LASIC ===\n")

    laboratorio = Laboratorio()

    tarefa_1 = Tarefa(1, "Analisar imagem X")
    tarefa_2 = Tarefa(2, "Validar imagem Y")
    tarefa_3 = Tarefa(3, "Registrar resultado Z")

    tarefa_1.atribuir_responsavel("  Cauê  ")
    tarefa_2.atribuir_responsavel("Ana")
    tarefa_3.atribuir_responsavel("João")

    tarefa_1.adicionar_tag("  Celula  ")
    tarefa_1.adicionar_tag("Microscopia")

    tarefa_2.adicionar_tag("ANALISE")
    tarefa_2.adicionar_tag("celula")

    tarefa_3.adicionar_tag("microscopia")
    tarefa_3.adicionar_tag("celula")

    tarefa_1.registrar_dado("arquivo", "imagem_x.png")
    tarefa_1.registrar_dado("largura", 1920)
    tarefa_1.registrar_dado("altura", 1080)

    tarefa_2.registrar_dado("arquivo", "imagem_y.tiff")
    tarefa_2.registrar_dado("largura", 3840)
    tarefa_2.registrar_dado("altura", 2160)

    tarefa_3.registrar_dado("arquivo", "resultado_z.png")
    tarefa_3.registrar_dado("formato", "RGB")

    laboratorio.cadastrar_tarefa(tarefa_1)
    laboratorio.cadastrar_tarefa(tarefa_2)
    laboratorio.cadastrar_tarefa(tarefa_3)

    print("--- RELATORIO INICIAL ---")
    print(laboratorio.gerar_relatorio())

    print("\n--- BUSCA DA TAREFA 2 ---")
    tarefa_encontrada = laboratorio.buscar_tarefa(2)

    if isinstance(tarefa_encontrada, Tarefa):
        print(tarefa_encontrada.resumo())
    else:
        print(tarefa_encontrada)

    print("\n--- ATENDIMENTO DA FILA ---")
    tarefa_atendida = laboratorio.atender_proxima_tarefa()

    if isinstance(tarefa_atendida, Tarefa):
        print(
            f"Tarefa atendida: {tarefa_atendida.tarefa_id}"
        )
        print(f"Novo status: {tarefa_atendida.status}")
    else:
        print(tarefa_atendida)

    print("\n--- CONCLUSAO DA TAREFA 1 ---")
    tarefa_1.concluir()
    print(tarefa_1.resumo())

    print("\n--- TAGS CADASTRADAS ---")
    print(laboratorio.listar_tags())

    print("\n--- BUSCA INEXISTENTE ---")
    print(laboratorio.buscar_tarefa(99))


if __name__ == "__main__":
    main()