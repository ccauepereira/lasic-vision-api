import { Plus, LoaderCircle } from 'lucide-react';
import type { Tarefa } from '../tipos/tarefa';

interface ListaTarefasProps {
  tarefas: Tarefa[];
  tarefaSelecionadaId: string | null;
  aoSelecionar: (tarefa: Tarefa) => void;
  aoNovaTarefa: () => void;
  carregando?: boolean;
}

export function ListaTarefas({
  tarefas,
  tarefaSelecionadaId,
  aoSelecionar,
  aoNovaTarefa,
  carregando = false,
}: ListaTarefasProps) {
  return (
    <div className="coluna-lateral">
      <div style={{ padding: '1rem', borderBottom: '1px solid #e0e0e0' }}>
        <button
          className="btn-primario"
          style={{ width: '100%', justifyContent: 'center' }}
          onClick={aoNovaTarefa}
        >
          <Plus size={18} /> Nova Tarefa
        </button>
      </div>
      <div className="lista-tarefas">
        {carregando ? (
          <p
            style={{
              textAlign: 'center',
              color: '#666',
              marginTop: '1rem',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              gap: '0.5rem',
            }}
          >
            <LoaderCircle size={18} className="spin" /> Carregando tarefas...
          </p>
        ) : tarefas.length === 0 ? (
          <p style={{ textAlign: 'center', color: '#666', marginTop: '1rem' }}>
            Lista vazia.
          </p>
        ) : (
          tarefas.map(tarefa => (
            <button
              key={tarefa.id}
              className={`item-tarefa ${
                tarefa.id === tarefaSelecionadaId ? 'selecionada' : ''
              }`}
              onClick={() => aoSelecionar(tarefa)}
            >
              <div style={{ fontWeight: 500 }}>{tarefa.titulo}</div>
              <span className={`status-badge status-${tarefa.status}`}>
                {tarefa.status.replace('_', ' ')}
              </span>
            </button>
          ))
        )}
      </div>
    </div>
  );
}