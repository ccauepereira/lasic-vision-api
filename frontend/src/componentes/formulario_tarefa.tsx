import { useState } from 'react';
import { Plus } from 'lucide-react';

interface FormularioTarefaProps {
  aoCriar: (titulo: string, descricao: string) => void;
  aoCancelar: () => void;
}

export function FormularioTarefa({ aoCriar, aoCancelar }: FormularioTarefaProps) {
  const [titulo, setTitulo] = useState('');
  const [descricao, setDescricao] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (titulo && descricao) {
      aoCriar(titulo, descricao);
    }
  };

  return (
    <form className="formulario" onSubmit={handleSubmit}>
      <h2>Nova Tarefa</h2>
      <div className="campo-form" style={{marginTop: '1rem'}}>
        <label>Titulo</label>
        <input value={titulo} onChange={e => setTitulo(e.target.value)} required />
      </div>
      <div className="campo-form">
        <label>Descricao</label>
        <input value={descricao} onChange={e => setDescricao(e.target.value)} required />
      </div>
      <div className="acoes-tarefa">
        <button type="submit" className="btn-primario">
          <Plus size={18} /> Criar
        </button>
        <button type="button" className="btn-secundario" onClick={aoCancelar}>
          Cancelar
        </button>
      </div>
    </form>
  );
}