import { useState, useEffect, useCallback } from 'react';
import { Cabecalho } from './componentes/cabecalho';
import { ListaTarefas } from './componentes/lista_tarefas';
import { EstadoVazio } from './componentes/estado_vazio';
import { DetalhesTarefa } from './componentes/detalhes_tarefa';
import { FormularioTarefa } from './componentes/formulario_tarefa';
import type { Tarefa } from './tipos/tarefa';
import {
  verificarSaude,
  listarTarefas,
  criarTarefa as apiCriarTarefa,
  atribuirResponsavel as apiAtribuirResponsavel,
  iniciarTarefa as apiIniciarTarefa,
  analisarImagem as apiAnalisarImagem,
  concluirTarefa as apiConcluirTarefa,
} from './servicos/cliente_api';

function App() {
  const [tarefas, setTarefas] = useState<Tarefa[]>([]);
  const [selecionadaId, setSelecionadaId] = useState<string | null>(null);
  const [criando, setCriando] = useState(false);
  const [apiConectada, setApiConectada] = useState<boolean | null>(null);
  const [carregandoTarefas, setCarregandoTarefas] = useState(false);

  const carregarTarefas = useCallback(async () => {
    const saudeOk = await verificarSaude();
    setApiConectada(saudeOk);

    setCarregandoTarefas(true);
    try {
      const lista = await listarTarefas();
      setTarefas(lista);
    } catch {
      // erro manipulado nos componentes ou estado mantido
    } finally {
      setCarregandoTarefas(false);
    }
  }, []);

  useEffect(() => {
    carregarTarefas();
  }, [carregarTarefas]);

  const tarefaSelecionada = tarefas.find(t => t.id === selecionadaId) || null;

  const criarTarefa = async (titulo: string, descricao: string) => {
    const nova = await apiCriarTarefa(titulo, descricao);
    await carregarTarefas();
    setCriando(false);
    setSelecionadaId(nova.id);
  };

  const atribuirResponsavel = async (id: string, responsavel: string) => {
    await apiAtribuirResponsavel(id, responsavel);
    await carregarTarefas();
  };

  const iniciarTarefa = async (id: string) => {
    await apiIniciarTarefa(id);
    await carregarTarefas();
  };

  const enviarImagem = async (id: string, arquivo: File) => {
    await apiAnalisarImagem(id, arquivo);
    await carregarTarefas();
  };

  const concluirTarefa = async (id: string) => {
    await apiConcluirTarefa(id);
    await carregarTarefas();
  };

  return (
    <div className="layout">
      <Cabecalho apiConectada={apiConectada} />
      <div className="conteudo-principal">
        <ListaTarefas
          tarefas={tarefas}
          tarefaSelecionadaId={selecionadaId}
          aoSelecionar={t => {
            setSelecionadaId(t.id);
            setCriando(false);
          }}
          aoNovaTarefa={() => {
            setCriando(true);
            setSelecionadaId(null);
          }}
          carregando={carregandoTarefas}
        />
        <main className="coluna-principal">
          {criando ? (
            <FormularioTarefa
              aoCriar={criarTarefa}
              aoCancelar={() => setCriando(false)}
            />
          ) : tarefaSelecionada ? (
            <DetalhesTarefa
              tarefa={tarefaSelecionada}
              aoAtribuirResponsavel={atribuirResponsavel}
              aoIniciar={iniciarTarefa}
              aoEnviarImagem={enviarImagem}
              aoConcluir={concluirTarefa}
            />
          ) : (
            <EstadoVazio />
          )}
        </main>
      </div>
    </div>
  );
}

export default App;