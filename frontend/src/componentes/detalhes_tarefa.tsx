import { useState, useRef, useEffect } from 'react';
import {
  UserRound,
  Play,
  Upload,
  CheckCircle2,
  LoaderCircle,
  CircleAlert,
} from 'lucide-react';
import type { Tarefa } from '../tipos/tarefa';
import { ResultadoAnaliseVisual } from './resultado_analise';

interface DetalhesTarefaProps {
  tarefa: Tarefa;
  aoAtribuirResponsavel: (id: string, responsavel: string) => Promise<void> | void;
  aoIniciar: (id: string) => Promise<void> | void;
  aoEnviarImagem: (id: string, file: File) => Promise<void> | void;
  aoConcluir: (id: string) => Promise<void> | void;
}

export function DetalhesTarefa({
  tarefa,
  aoAtribuirResponsavel,
  aoIniciar,
  aoEnviarImagem,
  aoConcluir,
}: DetalhesTarefaProps) {
  const [novoResponsavel, setNovoResponsavel] = useState('');
  const [carregando, setCarregando] = useState(false);
  const [erro, setErro] = useState<string | null>(null);
  const [preview, setPreview] = useState<string | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    setNovoResponsavel('');
    setErro(null);
    setPreview(null);
  }, [tarefa.id]);

  const handleAtribuir = async () => {
    if (novoResponsavel.trim()) {
      setCarregando(true);
      setErro(null);
      try {
        await aoAtribuirResponsavel(tarefa.id, novoResponsavel.trim());
        setNovoResponsavel('');
      } catch (err: unknown) {
        if (err instanceof Error) {
          setErro(err.message);
        } else {
          setErro('Erro ao atribuir responsavel.');
        }
      } finally {
        setCarregando(false);
      }
    }
  };

  const handleIniciar = async () => {
    setCarregando(true);
    setErro(null);
    try {
      await aoIniciar(tarefa.id);
    } catch (err: unknown) {
      if (err instanceof Error) {
        setErro(err.message);
      } else {
        setErro('Erro ao iniciar tarefa.');
      }
    } finally {
      setCarregando(false);
    }
  };

  const handleArquivo = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      const url = URL.createObjectURL(file);
      setPreview(url);
      setErro(null);
      setCarregando(true);
      try {
        await aoEnviarImagem(tarefa.id, file);
      } catch (err: unknown) {
        if (err instanceof Error) {
          setErro(err.message);
        } else {
          setErro('Erro ao enviar imagem.');
        }
      } finally {
        setCarregando(false);
      }
    }
  };

  const handleConcluir = async () => {
    setCarregando(true);
    setErro(null);
    try {
      await aoConcluir(tarefa.id);
    } catch (err: unknown) {
      if (err instanceof Error) {
        setErro(err.message);
      } else {
        setErro('Erro ao concluir tarefa.');
      }
    } finally {
      setCarregando(false);
    }
  };

  return (
    <div className="detalhes">
      <h2>{tarefa.titulo}</h2>
      <p style={{ color: '#555', marginTop: '0.5rem' }}>{tarefa.descricao}</p>
      <div style={{ marginTop: '1.5rem' }}>
        <strong>Status: </strong>
        <span className={`status-badge status-${tarefa.status}`}>
          {tarefa.status.replace('_', ' ')}
        </span>
      </div>
      <div style={{ marginTop: '1rem' }}>
        <strong>Responsavel: </strong>
        {tarefa.responsavel || 'Nenhum'}
      </div>

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

      {tarefa.status === 'pendente' && !tarefa.responsavel && (
        <div className="acoes-tarefa">
          <input
            type="text"
            placeholder="Nome do responsavel"
            value={novoResponsavel}
            onChange={e => setNovoResponsavel(e.target.value)}
            disabled={carregando}
            style={{ padding: '0.5rem', borderRadius: '4px', border: '1px solid #ccc' }}
          />
          <button className="btn-primario" onClick={handleAtribuir} disabled={carregando}>
            {carregando ? (
              <LoaderCircle size={18} className="spin" />
            ) : (
              <UserRound size={18} />
            )}
            Atribuir
          </button>
        </div>
      )}

      {tarefa.status === 'pendente' && tarefa.responsavel && (
        <div className="acoes-tarefa">
          <button className="btn-primario" onClick={handleIniciar} disabled={carregando}>
            {carregando ? (
              <LoaderCircle size={18} className="spin" />
            ) : (
              <Play size={18} />
            )}
            Iniciar Tarefa
          </button>
        </div>
      )}

      {tarefa.status === 'em_andamento' && (
        <div
          style={{
            marginTop: '1.5rem',
            padding: '1rem',
            backgroundColor: '#f8f9fa',
            borderRadius: '4px',
            border: '1px dashed #ccc',
          }}
        >
          <h4>Analisar Imagem</h4>
          <input
            type="file"
            accept="image/*"
            style={{ display: 'none' }}
            ref={fileInputRef}
            onChange={handleArquivo}
          />
          <div className="acoes-tarefa">
            <button
              className="btn-secundario"
              onClick={() => fileInputRef.current?.click()}
              disabled={carregando}
            >
              <Upload size={18} /> Selecionar Arquivo
            </button>
          </div>
          {preview && (
            <img src={preview} alt="Preview" className="preview-imagem" />
          )}
          {carregando && (
            <p
              style={{
                display: 'flex',
                alignItems: 'center',
                gap: '0.5rem',
                color: '#0056b3',
                marginTop: '1rem',
              }}
            >
              <LoaderCircle size={18} className="spin" /> Processando analise OpenCV...
            </p>
          )}
        </div>
      )}

      {tarefa.resultadoAnalise && (
        <>
          <ResultadoAnaliseVisual resultado={tarefa.resultadoAnalise} />
          {tarefa.status === 'em_andamento' && (
            <div className="acoes-tarefa" style={{ marginTop: '2rem' }}>
              <button
                className="btn-primario"
                style={{ backgroundColor: '#2b8a3e' }}
                onClick={handleConcluir}
                disabled={carregando}
              >
                {carregando ? (
                  <LoaderCircle size={18} className="spin" />
                ) : (
                  <CheckCircle2 size={18} />
                )}
                Concluir Tarefa
              </button>
            </div>
          )}
        </>
      )}
    </div>
  );
}