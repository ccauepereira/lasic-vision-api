import pytest
from uuid import uuid4

from app.dominio.entidades.resultado_analise_imagem import ResultadoAnaliseImagem
from app.dominio.enumeracoes import StatusTarefa
from app.dominio.excecoes import ErroTarefaNaoEncontrada
from app.repositorios.sqlite.repositorio_tarefa_sqlite import RepositorioTarefaSQLite
from app.servicos.servico_tarefa import ServicoTarefa
from app.dominio.protocolos import ProtocoloAnalisadorImagem


class AnalisadorFalso(ProtocoloAnalisadorImagem):
    def analisar(self, nome_arquivo: str, conteudo: bytes) -> ResultadoAnaliseImagem:
        return ResultadoAnaliseImagem(
            nome_arquivo=nome_arquivo,
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


@pytest.fixture
def servico_tarefa(sessao):
    repositorio = RepositorioTarefaSQLite(sessao)
    analisador = AnalisadorFalso()
    return ServicoTarefa(repositorio_tarefa=repositorio, analisador_imagem=analisador)


def test_servico_cria_e_busca_tarefa(servico_tarefa):
    tarefa_criada = servico_tarefa.criar_tarefa(titulo="Tarefa Inicial")
    
    tarefa_buscada = servico_tarefa.buscar_tarefa_por_id(tarefa_criada.tarefa_id)
    
    assert tarefa_buscada.tarefa_id == tarefa_criada.tarefa_id
    assert tarefa_buscada.titulo == "Tarefa Inicial"
    assert tarefa_buscada.status == StatusTarefa.PENDENTE


def test_servico_tarefa_inexistente_gera_erro(servico_tarefa):
    id_falso = uuid4()
    with pytest.raises(ErroTarefaNaoEncontrada, match=f"Tarefa com identificador {id_falso} nao encontrada."):
        servico_tarefa.buscar_tarefa_por_id(id_falso)


def test_servico_atribui_responsavel(servico_tarefa):
    tarefa = servico_tarefa.criar_tarefa(titulo="Tarefa Sem Dono")
    
    tarefa_atualizada = servico_tarefa.atribuir_responsavel(tarefa.tarefa_id, "Novo Dono")
    
    assert tarefa_atualizada.responsavel == "Novo Dono"
    
    tarefa_buscada = servico_tarefa.buscar_tarefa_por_id(tarefa.tarefa_id)
    assert tarefa_buscada.responsavel == "Novo Dono"


def test_servico_inicia_tarefa(servico_tarefa):
    tarefa = servico_tarefa.criar_tarefa(titulo="Tarefa a Iniciar")
    servico_tarefa.atribuir_responsavel(tarefa.tarefa_id, "Trabalhador")
    
    tarefa_iniciada = servico_tarefa.iniciar_tarefa(tarefa.tarefa_id)
    
    assert tarefa_iniciada.status == StatusTarefa.EM_ANDAMENTO
    
    tarefa_buscada = servico_tarefa.buscar_tarefa_por_id(tarefa.tarefa_id)
    assert tarefa_buscada.status == StatusTarefa.EM_ANDAMENTO


def test_servico_registra_resultado_usando_analisador_falso(servico_tarefa):
    tarefa = servico_tarefa.criar_tarefa(titulo="Tarefa Analisando")
    servico_tarefa.atribuir_responsavel(tarefa.tarefa_id, "Avaliador")
    servico_tarefa.iniciar_tarefa(tarefa.tarefa_id)
    
    resultado = servico_tarefa.analisar_imagem(
        tarefa_id=tarefa.tarefa_id,
        nome_arquivo="teste.png",
        conteudo=b"conteudo"
    )
    
    assert resultado.brilho_medio == 1.5
    assert resultado.contraste_medio == 2.5
    assert resultado.quantidade_bordas == 10
    
    tarefa_buscada = servico_tarefa.buscar_tarefa_por_id(tarefa.tarefa_id)
    assert tarefa_buscada.resultado_analise is not None


def test_servico_conclui_tarefa(servico_tarefa):
    tarefa = servico_tarefa.criar_tarefa(titulo="Tarefa Analisando")
    servico_tarefa.atribuir_responsavel(tarefa.tarefa_id, "Avaliador")
    servico_tarefa.iniciar_tarefa(tarefa.tarefa_id)
    servico_tarefa.analisar_imagem(
        tarefa_id=tarefa.tarefa_id,
        nome_arquivo="teste.png",
        conteudo=b"conteudo"
    )
    
    tarefa_concluida = servico_tarefa.concluir_tarefa(tarefa.tarefa_id)
    
    assert tarefa_concluida.status == StatusTarefa.CONCLUIDA
    
    tarefa_buscada = servico_tarefa.buscar_tarefa_por_id(tarefa.tarefa_id)
    assert tarefa_buscada.status == StatusTarefa.CONCLUIDA
