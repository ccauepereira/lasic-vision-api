from repositories.memory_repo import TarefaRepositoryMemoria
from vision.simple_analyzer import AnalisadorImagemSimples
from services.task_service import TarefaService
from domain.exceptions import RegraNegocioVioladaErro


def executar_fluxo() -> None:
    # 1. Injeção manual de dependências (Composition Root)
    repositorio = TarefaRepositoryMemoria()
    analisador = AnalisadorImagemSimples()
    servico = TarefaService(repository=repositorio, analisador=analisador)

    print("==================================================")
    print("      LASIC VISION API - TESTE DE DOMÍNIO         ")
    print("==================================================")

    # Passo 1: Criar tarefa
    tarefa = servico.criar_tarefa(
        nome="Inspeção Óptica de Solda - Lote A12",
        caminho_imagem="amostra_solda.png"
    )
    print(f"\n[1] Tarefa Criada:")
    print(f"    ID: {tarefa.id} | Nome: '{tarefa.nome}' | Status: {tarefa.status.value}")

    # Passo 2: Atribuir responsável
    tarefa = servico.atribuir_responsavel(tarefa.id, responsavel="Eng. Carlos Silva")
    print(f"\n[2] Responsável Atribuído:")
    print(f"    Responsável: {tarefa.responsavel}")

    # Passo 3: Iniciar
    tarefa = servico.iniciar_tarefa(tarefa.id)
    print(f"\n[3] Tarefa Iniciada:")
    print(f"    Status Atual: {tarefa.status.value}")

    # Passo 4: Registrar resultado de análise
    tarefa = servico.registrar_resultado_analise(tarefa.id)
    print(f"\n[4] Análise de Imagem Registrada:")
    if tarefa.resultado_analise:
        print(f"    Objetos Detectados: {tarefa.resultado_analise.qtd_objetos_detectados}")
        print(f"    Confiança Média: {tarefa.resultado_analise.taxa_confianca_media * 100:.1f}%")
        print(f"    Detalhes: {tarefa.resultado_analise.detalhes}")

    # Passo 5: Concluir
    tarefa = servico.concluir_tarefa(tarefa.id)
    print(f"\n[5] Tarefa Concluída com Sucesso:")
    print(f"    Status Final: {tarefa.status.value}")

    # Demonstração de proteção de regras de negócio
    print("\n--------------------------------------------------")
    print("Teste de Proteção de Regra: Tentar reiniciar tarefa concluída:")
    try:
        servico.iniciar_tarefa(tarefa.id)
    except RegraNegocioVioladaErro as erro:
        print(f"    [OK] Regra disparada com sucesso: {erro}")
    print("==================================================")


if __name__ == "__main__":
    executar_fluxo()