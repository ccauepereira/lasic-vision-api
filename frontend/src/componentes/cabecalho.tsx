import { ChartNoAxesColumn } from 'lucide-react';

export function Cabecalho() {
  return (
    <header className="cabecalho">
      <h1>
        <ChartNoAxesColumn size={24} />
        LASIC Vision API
      </h1>
      <span className="indicador-modo">Modo demonstracao</span>
    </header>
  );
}