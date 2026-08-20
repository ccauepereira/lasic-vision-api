import { useState } from 'react';
import { Plus, LoaderCircle, CircleAlert } from 'lucide-react';

interface FormularioTarefaProps {
  aoCriar: (titulo: string, descricao: string) => Promise<void> | void;
  aoCancelar: () => void;
}

export function FormularioTarefa({ aoCriar, aoCancelar }: FormularioTarefaProps) {
  const [titulo, setTitulo] = useState('');
  const [descricao, setDescricao] = useState('');
  const [carregando, setCarregando] = useState(false);
  const [erro, setErro] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (titulo.trim()) {
      setCarregando(true);
      setErro(null);
      try {
        await aoCriar(titulo.trim(), descricao.trim());
      } catch (err: unknown) {
        if (err instanceof Error) {
          setErro(err.message);
        } else {
          setErro('Erro ao criar tarefa.');
        }
      } finally {
        setCarregando(false);
      }
    }
  };

  return (
    <form className="formulario" onSubmit={handleSubmit}>
      <h2>Nova Tarefa</h2>
      {erro && (
        <p
          style={{
            display: 'flex',
            alignItems: 'center',
            gap: '0.5rem',
            color: '#d32f2f',
            marginTop: '1rem',
          }}
        >
          <CircleAlert size={18} /> {erro}
        </p>
      )}
      <div className="campo-form" style={{ marginTop: '1rem' }}>
        <label>Titulo</label>
        <input
          value={titulo}
          onChange={e => setTitulo(e.target.value)}
          required
          disabled={carregando}
        />
      </div>
      <div className="campo-form">
        <label>Descricao</label>
        <input
          value={descricao}
          onChange={e => setDescricao(e.target.value)}
          disabled={carregando}
        />
      </div>
      <div className="acoes-tarefa">
        <button type="submit" className="btn-primario" disabled={carregando}>
          {carregando ? (
            <>
              <LoaderCircle size={18} className="spin" /> Criando...
            </>
          ) : (
            <>
              <Plus size={18} /> Criar
            </>
          )}
        </button>
        <button
          type="button"
          className="btn-secundario"
          onClick={aoCancelar}
          disabled={carregando}
        >
          Cancelar
        </button>
      </div>
    </form>
  );
}