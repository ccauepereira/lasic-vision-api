import React from 'react';
import type { HealthResponse } from '../types/api';

interface HeaderProps {
  healthData: HealthResponse | null;
  healthLoading: boolean;
  healthError: string | null;
  onTestHealth: () => void;
}

export const Header: React.FC<HeaderProps> = ({
  healthData,
  healthLoading,
  healthError,
  onTestHealth,
}) => {
  return (
    <header className="lab-header">
      <div className="header-brand">
        <span className="brand-tag">LASIC VISION LAB</span>
        <h1 className="lab-title">Cauê Test</h1>
        <p className="lab-subtitle">Painel de Demonstração Técnico: FastAPI + OpenCV</p>
      </div>

      <div className="health-control">
        <button 
          type="button" 
          className="btn btn-outline" 
          onClick={onTestHealth}
          disabled={healthLoading}
        >
          {healthLoading ? (
            <span className="loading-inline">
              <span className="spinner spinner-dark"></span> Checando...
            </span>
          ) : (
            '⚡ Testar GET /health'
          )}
        </button>

        {healthData && (
          <div className="health-status health-online">
            <span className="dot dot-online"></span>
            <span><strong>{healthData.projeto}</strong> v{healthData.versao} ({healthData.status.toUpperCase()})</span>
          </div>
        )}

        {healthError && (
          <div className="health-status health-offline">
            <span className="dot dot-offline"></span>
            <span>API Off-line: {healthError}</span>
          </div>
        )}
      </div>
    </header>
  );
};
