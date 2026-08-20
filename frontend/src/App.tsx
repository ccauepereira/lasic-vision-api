import { useState } from 'react';
import { Cabecalho } from './componentes/cabecalho';
import { ListaTarefas } from './componentes/lista_tarefas';
import { EstadoVazio } from './componentes/estado_vazio';
import { DetalhesTarefa } from './componentes/detalhes_tarefa';
import { FormularioTarefa } from './componentes/formulario_tarefa';
import { tarefasSimuladas } from './dados/tarefas_simuladas';
import type { Tarefa, ResultadoAnalise } from './tipos/tarefa';

// PONTO DE INTEGRACAO FUTURA: 
// Substituir a gestao de estado local destas funcoes por chamadas HTTP reais da FastAPI.

function App() {
  const [tarefas, setTarefas] = useState<Tarefa[]>(tarefasSimuladas);
  const [selecionadaId, setSelecionadaId] = useState<number | null>(null);
  const [criando, setCriando] = useState(false);

  const tarefaSelecionada = tarefas.find(t => t.id === selecionadaId) || null;

  const criarTarefa = (titulo: string, descricao: string) => {
    const nova: Tarefa = {
      id: Math.max(...tarefas.map(t => t.id), 0) + 1,
      titulo,
      descricao,
      responsavel: null,
      status: 'pendente',
      resultadoAnalise: null
    };
    setTarefas([...tarefas, nova]);
    setCriando(false);
    setSelecionadaId(nova.id);
  };

  const atualizarTarefa = (id: number, atualizacoes: Partial<Tarefa>) => {
    setTarefas(tarefas.map(t => t.id === id ? { ...t, ...atualizacoes } : t));
  };

  const simularAnalise = (): ResultadoAnalise => ({
    largura: 800,
    altura: 600,
    formato: 'PNG',
    modoCor: 'Grayscale',
    brilhoMedio: 98.4,
    contrasteMedio: 32.1,
    classificacaoBrilho: 'Escuro',
    classificacaoContraste: 'Baixo',
    quantidadeBordas: 450,
    tagsAutomaticas: ['simulacao', 'teste']
  });

  return (
    <div className="layout">
      <Cabecalho />
      <div className="conteudo-principal">
        <ListaTarefas 
          tarefas={tarefas} 
          tarefaSelecionadaId={selecionadaId} 
          aoSelecionar={(t) => { setSelecionadaId(t.id); setCriando(false); }} 
          aoNovaTarefa={() => { setCriando(true); setSelecionadaId(null); }}
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
              aoAtribuirResponsavel={(id, res) => atualizarTarefa(id, { responsavel: res })}
              aoIniciar={(id) => atualizarTarefa(id, { status: 'em_andamento' })}
              aoEnviarImagem={(id) => atualizarTarefa(id, { resultadoAnalise: simularAnalise() })}
              aoConcluir={(id) => atualizarTarefa(id, { status: 'concluida' })}
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