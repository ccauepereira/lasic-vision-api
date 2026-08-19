from imagem import Imagem
from heranca_inspecao import InspecaoCelular, InspecaoSuperficie, InspecaoDimensional
from sistema import SistemaInspecao
from excecoes import InspecaoError

def exibir_menu():
    print("\n" + "="*40)
    print("🏭 SISTEMA DE INSPEÇÃO VISUAL 2.0")
    print("="*40)
    print("1. Cadastrar nova Inspeção")
    print("2. Atender próxima inspeção da fila")
    print("3. Executar todas as análises (Polimorfismo)")
    print("4. Listar todas as inspeções cadastradas")
    print("5. Aprovar ou Reprovar inspeção")
    print("0. Sair do Sistema")
    print("="*40)

def main():
    sistema = SistemaInspecao()
    
    while True:
        exibir_menu()
        opcao = input("Escolha uma opção: ")
        
        try:
            if opcao == "1":
                print("\n--- PASSO 1: DADOS DA IMAGEM ---")
                arquivo = input("Nome do arquivo (ex: peca.png): ")
                largura = int(input("Largura (px): "))
                altura = int(input("Altura (px): "))
                formato = input("Formato (ex: RGB): ")
                
                # Usando o staticmethod para validar
                if not Imagem.dimensoes_validas(largura, altura):
                    print("❌ Erro: As dimensões devem ser maiores que zero.")
                    continue
                
                # Criando a imagem com classmethod
                imagem = Imagem.de_resolucao(arquivo, (largura, altura), formato)
                
                # Simulando a visão computacional pedindo os dados para o usuário
                print("\n--- PASSO 2: DADOS CAPTURADOS DA IMAGEM ---")
                imagem.registrar_caracteristica("quantidade_contornos", float(input("Quantidade de contornos detectados: ")))
                imagem.registrar_caracteristica("brilho", float(input("Nível de brilho (0-100): ")))
                imagem.registrar_caracteristica("contraste", float(input("Nível de contraste (0-100): ")))
                
                print("\n--- PASSO 3: DADOS DA INSPEÇÃO ---")
                id_insp = int(input("ID da Inspeção (número inteiro): "))
                componente = input("Nome do componente: ")
                tecnico = input("Nome do técnico responsável: ")
                
                print("\nQual o tipo de análise?")
                print("[1] Celular | [2] Superfície | [3] Dimensional")
                tipo = input("Digite 1, 2 ou 3: ")
                
                if tipo == "1":
                    inspecao = InspecaoCelular(id_insp, componente, imagem)
                elif tipo == "2":
                    inspecao = InspecaoSuperficie(id_insp, componente, imagem)
                elif tipo == "3":
                    inspecao = InspecaoDimensional(id_insp, componente, imagem)
                else:
                    print("❌ Tipo de inspeção inválido. Cadastro cancelado.")
                    continue
                
                # Atribuindo técnico via property
                inspecao.tecnico = tecnico
                
                # Cadastrando no sistema
                sistema.cadastrar_inspecao(inspecao)
                print(f"\n✅ Inspeção {id_insp} ({componente}) cadastrada com sucesso e adicionada à fila!")

            elif opcao == "2":
                print("\n--- ATENDENDO FILA ---")
                inspecao_atendida = sistema.atender_proxima_inspecao()
                print(f"✅ Inspeção ID {inspecao_atendida.inspecao_id} iniciada!")
                print(f"Status atual: {inspecao_atendida.status.upper()}")

            elif opcao == "3":
                print("\n--- EXECUTANDO ANÁLISES AUTOMÁTICAS ---")
                resultados = sistema.executar_todas_as_analises()
                if not resultados:
                    print("Nenhuma inspeção cadastrada no sistema.")
                else:
                    for res in resultados:
                        print(f"⚙️ {res}")

            elif opcao == "4":
                print("\n--- RELATÓRIO DE INSPEÇÕES ---")
                print(sistema.gerar_relatorio() if len(sistema) > 0 else "Sistema vazio.")

            elif opcao == "5":
                print("\n--- APROVAR / REPROVAR ---")
                id_busca = int(input("Digite o ID da inspeção que deseja avaliar: "))
                
                # Busca a inspeção, se não achar cai no except InspecaoError
                inspecao = sistema.buscar_inspecao(id_busca)
                
                print(f"Inspecao selecionada: {inspecao.componente} | Status: {inspecao.status}")
                decisao = input("Deseja (A)provar ou (R)eprovar? ").strip().upper()
                
                if decisao == "A":
                    inspecao.aprovar()
                    print(f"✅ Inspeção {id_busca} APROVADA.")
                elif decisao == "R":
                    inspecao.reprovar()
                    print(f"❌ Inspeção {id_busca} REPROVADA.")
                    
                    # Permite adicionar um defeito se for reprovada
                    motivo = input("Qual foi o defeito encontrado? ")
                    inspecao.registrar_defeito(motivo)
                else:
                    print("Opção inválida. Nenhuma alteração feita.")

            elif opcao == "0":
                print("\nDesligando sistema da fábrica... Até logo! 👋")
                break

            else:
                print("❌ Opção inválida. Tente novamente.")

        # Tratamento de Erros de Clean Code!
        except ValueError:
            print("\n❌ ERRO DE DIGITAÇÃO: Você digitou um texto onde o sistema esperava um número (ID, largura, altura, etc).")
        except InspecaoError as e:
            print(f"\n❌ ERRO DE REGRA DE NEGÓCIO: {e}")
        except Exception as e:
            print(f"\n❌ ERRO INESPERADO: {e}")

if __name__ == "__main__":
    main()