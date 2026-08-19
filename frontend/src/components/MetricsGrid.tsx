import React from 'react';
import type { AnaliseImagemResponse } from '../types/api';

interface MetricsGridProps {
  data: AnaliseImagemResponse;
}

export const MetricsGrid: React.FC<MetricsGridProps> = ({ data }) => {
  return (
    <div className="cards-grid">
      <div className="metric-card">
        <span className="card-tag">Arquivo</span>
        <span className="card-val font-mono" title={data.arquivo}>{data.arquivo}</span>
      </div>

      <div className="metric-card">
        <span className="card-tag">Largura</span>
        <span className="card-val highlight-blue">{data.largura} <small>px</small></span>
      </div>

      <div className="metric-card">
        <span className="card-tag">Altura</span>
        <span className="card-val highlight-blue">{data.altura} <small>px</small></span>
      </div>

      <div className="metric-card">
        <span className="card-tag">Modo de Cor</span>
        <span className="card-val">{data.modo_cor}</span>
      </div>

      <div className="metric-card">
        <span className="card-tag">Brilho Médio</span>
        <span className="card-val">{data.brilho_medio}</span>
      </div>

      <div className="metric-card">
        <span className="card-tag">Contraste Médio</span>
        <span className="card-val">{data.contraste_medio}</span>
      </div>

      <div className="metric-card">
        <span className="card-tag">Qtd. de Bordas</span>
        <span className="card-val highlight-dark">{data.quantidade_bordas}</span>
      </div>

      <div className="metric-card">
        <span className="card-tag">Classificação Brilho</span>
        <span className="card-val status-pill">{data.classificacao_brilho}</span>
      </div>

      <div className="metric-card">
        <span className="card-tag">Classificação Contraste</span>
        <span className="card-val status-pill">{data.classificacao_contraste}</span>
      </div>
    </div>
  );
};
