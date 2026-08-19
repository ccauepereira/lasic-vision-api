import React from 'react';
import type { AnaliseImagemResponse } from '../types/api';

interface MetricsGridProps {
  data: AnaliseImagemResponse;
}

export const MetricsGrid: React.FC<MetricsGridProps> = ({ data }) => {
  const getBrightnessBadgeClass = (classificacao: string) => {
    const lower = classificacao.toLowerCase();
    if (lower.includes('escuro') || lower.includes('baixo')) return 'badge-warning';
    if (lower.includes('claro') || lower.includes('alto')) return 'badge-info';
    return 'badge-success';
  };

  const getContrastBadgeClass = (classificacao: string) => {
    const lower = classificacao.toLowerCase();
    if (lower.includes('baixo')) return 'badge-warning';
    if (lower.includes('alto')) return 'badge-primary';
    return 'badge-success';
  };

  return (
    <section className="metrics-section">
      <h2 className="section-title">
        <span className="icon">📊</span> Métricas Extraídas (OpenCV)
      </h2>

      <div className="metrics-grid">
        <div className="metric-card" id="card-arquivo">
          <div className="card-header">
            <span className="card-icon">📄</span>
            <span className="card-label">Arquivo</span>
          </div>
          <div className="card-value file-name-value" title={data.arquivo}>
            {data.arquivo}
          </div>
          <div className="card-footer">Nome retornado pelo backend</div>
        </div>

        <div className="metric-card" id="card-dimensoes">
          <div className="card-header">
            <span className="card-icon">📐</span>
            <span className="card-label">Dimensões</span>
          </div>
          <div className="card-value highlight-cyan">
            {data.largura} × {data.altura} <span className="unit">px</span>
          </div>
          <div className="card-footer">Largura × Altura da imagem</div>
        </div>

        <div className="metric-card" id="card-modo-cor">
          <div className="card-header">
            <span className="card-icon">🎨</span>
            <span className="card-label">Modo de Cor</span>
          </div>
          <div className="card-value highlight-purple">
            {data.modo_cor}
          </div>
          <div className="card-footer">Formato do espaço de cores</div>
        </div>

        <div className="metric-card" id="card-brilho">
          <div className="card-header">
            <span className="card-icon">☀️</span>
            <span className="card-label">Brilho Médio</span>
          </div>
          <div className="card-value">
            {data.brilho_medio.toFixed(2)}
          </div>
          <div className="card-footer">
            <span className={`badge ${getBrightnessBadgeClass(data.classificacao_brilho)}`}>
              {data.classificacao_brilho}
            </span>
          </div>
        </div>

        <div className="metric-card" id="card-contraste">
          <div className="card-header">
            <span className="card-icon">☯️</span>
            <span className="card-label">Contraste Médio</span>
          </div>
          <div className="card-value">
            {data.contraste_medio.toFixed(2)}
          </div>
          <div className="card-footer">
            <span className={`badge ${getContrastBadgeClass(data.classificacao_contraste)}`}>
              {data.classificacao_contraste}
            </span>
          </div>
        </div>

        <div className="metric-card" id="card-bordas">
          <div className="card-header">
            <span className="card-icon">🔍</span>
            <span className="card-label">Bordas (Canny)</span>
          </div>
          <div className="card-value highlight-emerald">
            {data.quantidade_bordas.toLocaleString('pt-BR')}
          </div>
          <div className="card-footer">Pixels de borda detectados</div>
        </div>
      </div>
    </section>
  );
};
