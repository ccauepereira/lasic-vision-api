import { ChartNoAxesColumn, CheckCircle2, XCircle, LoaderCircle } from 'lucide-react';

interface CabecalhoProps {
  apiConectada: boolean | null;
}

export function Cabecalho({ apiConectada }: CabecalhoProps) {
  return (
    <header className="cabecalho">
      <h1>
        <ChartNoAxesColumn size={24} />
        LASIC Vision API
      </h1>
      {apiConectada === null ? (
        <span className="indicador-modo modo-carregando">
          <LoaderCircle size={14} className="spin" /> Verificando API...
        </span>
      ) : apiConectada ? (
        <span className="indicador-modo modo-conectado">
          <CheckCircle2 size={14} /> API Conectada
        </span>
      ) : (
        <span className="indicador-modo modo-desconectado">
          <XCircle size={14} /> API Desconectada
        </span>
      )}
    </header>
  );
}