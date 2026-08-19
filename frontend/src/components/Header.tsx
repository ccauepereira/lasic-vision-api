import React from 'react';
import type { HealthResponse } from '../types/api';

interface HeaderProps {
  health: HealthResponse | null;
  healthLoading: boolean;
  healthError: string | null;
  onRefreshHealth: () => void;
}

export const Header: React.FC<HeaderProps> = ({
  health,
  healthLoading,
  healthError,
  onRefreshHealth,
}) => {
  return (
    <header className="app-header">
      <div className="header-brand">
        <div className="logo-icon">👁️</div>
        <div>
          <h1 id="app-title" className="app-title">Cauê Test - LASIC Vision API</h1>
          <p className="app-subtitle">
            Plataforma Didática de Análise de Imagem (FastAPI + OpenCV + React)
          </p>
        </div>
      </div>

      <div className="health-badge-container">
        {healthLoading ? (
          <div className="health-badge loading">
            <span className="dot pulse"></span>
            Verificando API...
          </div>
        ) : healthError ? (
          <button 
            id="btn-retry-health"
            className="health-badge offline" 
            onClick={onRefreshHealth}
            title="Clique para tentar reconectar"
          >
            <span className="dot offline"></span>
            API Offline (Clique p/ tentar)
          </button>
        ) : health ? (
          <div 
            id="health-status-badge"
            className="health-badge online" 
            onClick={onRefreshHealth}
            title="Clique para atualizar o status"
          >
            <span className="dot online"></span>
            <span className="status-text">
              <strong>{health.projeto}</strong> v{health.versao} (Status: {health.status.toUpperCase()})
            </span>
          </div>
        ) : null}
      </div>
    </header>
  );
};
