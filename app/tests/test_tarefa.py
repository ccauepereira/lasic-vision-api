import pytest

from app.dominio.entidades.tarefa import Tarefa
from app.dominio.entidades.resultado_analise_imagem import ResultadoAnaliseImagem
from app.dominio.enumeracoes import StatusTarefa
from app.dominio.excecoes import ErroRegraNegocio


def criar_resultado_valido():
    return ResultadoAnaliseImagem(
        nome_arquivo="teste.png",
        largura=100,
        altura=100,
        formato="PNG",
        modo_cor="BGR",
        brilho_medio=1.5,
        contraste_medio=2.5,
        classificacao_brilho="escuro",
        classificacao_contraste="baixo_contraste",
        quantidade_bordas=10,
        tags_automaticas=("tag1", "tag2")
    )


def test_tarefa_nasce_pendente():
    tarefa = Tarefa(titulo="Nova Tarefa")
    assert tarefa.status == StatusTarefa.PENDENTE


def test_tarefa_nao_inicia_sem_responsavel():
    tarefa = Tarefa(titulo="Tarefa Sem Responsavel")
    with pytest.raises(ErroRegraNegocio, match="A tarefa precisa de um responsavel antes de ser iniciada."):
        tarefa.iniciar()


def test_tarefa_atribui_responsavel_enquanto_pendente():
    tarefa = Tarefa(titulo="Tarefa")
    tarefa.atribuir_responsavel("Joao")
    assert tarefa.responsavel == "Joao"
    assert tarefa.status == StatusTarefa.PENDENTE


def test_tarefa_inicia_com_responsavel():
    tarefa = Tarefa(titulo="Tarefa Iniciada")
    tarefa.atribuir_responsavel("Maria")
    tarefa.iniciar()
    assert tarefa.status == StatusTarefa.EM_ANDAMENTO


def test_tarefa_nao_conclui_sem_resultado():
    tarefa = Tarefa(titulo="Tarefa Sem Resultado")
    tarefa.atribuir_responsavel("Pedro")
    tarefa.iniciar()
    with pytest.raises(ErroRegraNegocio, match="A tarefa precisa de um resultado antes de ser concluida."):
        tarefa.concluir()


def test_tarefa_conclui_com_resultado():
    tarefa = Tarefa(titulo="Tarefa Completa")
    tarefa.atribuir_responsavel("Ana")
    tarefa.iniciar()
    
    resultado = criar_resultado_valido()
    tarefa.registrar_resultado(resultado)
    tarefa.concluir()
    
    assert tarefa.status == StatusTarefa.CONCLUIDA


def test_tarefa_concluida_nao_pode_ser_alterada():
    tarefa = Tarefa(titulo="Tarefa Finalizada")
    tarefa.atribuir_responsavel("Carlos")
    tarefa.iniciar()
    resultado = criar_resultado_valido()
    tarefa.registrar_resultado(resultado)
    tarefa.concluir()

    with pytest.raises(ErroRegraNegocio, match="Nao e permitido atribuir ou alterar o responsavel quando a tarefa nao esta pendente."):
        tarefa.atribuir_responsavel("Novo Responsavel")

    with pytest.raises(ErroRegraNegocio, match="Nao e permitido iniciar a tarefa quando a tarefa nao esta pendente."):
        tarefa.iniciar()

    with pytest.raises(ErroRegraNegocio, match="O resultado so pode ser registrado em uma tarefa em andamento."):
        tarefa.registrar_resultado(resultado)

    with pytest.raises(ErroRegraNegocio, match="Apenas tarefas em andamento podem ser concluidas."):
        tarefa.concluir()
