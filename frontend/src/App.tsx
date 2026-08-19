import { useState, useEffect } from 'react';
import type { HealthResponse, AnaliseImagemResponse } from './types/api';
import { Header } from './components/Header';
import { ImageUploader } from './components/ImageUploader';
import { MetricsGrid } from './components/MetricsGrid';
import { TagsList } from './components/TagsList';
import { JsonViewer } from './components/JsonViewer';
import './App.css';

// Centralização da URL base da API
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000';

export function App() {
  // Estados de conexão e saúde
  const [healthData, setHealthData] = useState<HealthResponse | null>(null);
  const [healthLoading, setHealthLoading] = useState<boolean>(false);
  const [healthError, setHealthError] = useState<string | null>(null);

  // Estados de arquivo e preview com gerenciamento de memória
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);

  // Estados do resultado de análise da imagem
  const [resultado, setResultado] = useState<AnaliseImagemResponse | null>(null);
  const [isAnalyzing, setIsAnalyzing] = useState<boolean>(false);
  const [apiError, setApiError] = useState<string | null>(null);

  // Limpeza de URLs de preview para evitar vazamentos de memória (Memory Leak)
  useEffect(() => {
    return () => {
      if (previewUrl) {
        URL.revokeObjectURL(previewUrl);
      }
    };
  }, [previewUrl]);

  // Testar endpoint GET /health
  const testarHealth = async () => {
    setHealthLoading(true);
    setHealthError(null);
    try {
      const res = await fetch(`${API_BASE_URL}/health`);
      if (!res.ok) {
        throw new Error(`Status ${res.status}: ${res.statusText}`);
      }
      const data: HealthResponse = await res.json();
      setHealthData(data);
    } catch (err) {
      setHealthError(
        err instanceof Error
          ? err.message
          : `Não foi possível conectar à API em ${API_BASE_URL}`
      );
      setHealthData(null);
    } finally {
      setHealthLoading(false);
    }
  };

  // Manipular seleção de arquivo com desalocação de URL antiga
  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      if (previewUrl) {
        URL.revokeObjectURL(previewUrl);
      }
      setSelectedFile(file);
      setPreviewUrl(URL.createObjectURL(file));
      setResultado(null);
      setApiError(null);
    }
  };

  // Limpar arquivo selecionado e revogar URL da memória
  const handleClearFile = () => {
    if (previewUrl) {
      URL.revokeObjectURL(previewUrl);
    }
    setSelectedFile(null);
    setPreviewUrl(null);
    setResultado(null);
    setApiError(null);
  };

  // Enviar imagem via POST FormData para /analises/imagem
  const analisarImagem = async () => {
    if (!selectedFile) return;

    setIsAnalyzing(true);
    setApiError(null);
    setResultado(null);

    const formData = new FormData();
    formData.append('arquivo', selectedFile);

    try {
      const res = await fetch(`${API_BASE_URL}/analises/imagem`, {
        method: 'POST',
        body: formData,
      });

      if (!res.ok) {
        let message = `Erro HTTP ${res.status}`;
        try {
          const errBody = await res.json();
          if (errBody.detail) {
            message = typeof errBody.detail === 'string' ? errBody.detail : JSON.stringify(errBody.detail);
          }
        } catch {
          // Mantém mensagem padrão de erro HTTP caso a resposta não seja JSON
        }
        throw new Error(message);
      }

      const data: AnaliseImagemResponse = await res.json();
      setResultado(data);
    } catch (err) {
      setApiError(
        err instanceof Error
          ? err.message
          : 'Erro inesperado durante o processamento da imagem.'
      );
    } finally {
      setIsAnalyzing(false);
    }
  };

  return (
    <div className="lab-container">
      <Header
        healthData={healthData}
        healthLoading={healthLoading}
        healthError={healthError}
        onTestHealth={testarHealth}
      />

      <main className="lab-grid">
        <ImageUploader
          previewUrl={previewUrl}
          selectedFile={selectedFile}
          isAnalyzing={isAnalyzing}
          apiError={apiError}
          onFileChange={handleFileChange}
          onClearFile={handleClearFile}
          onAnalyze={analisarImagem}
        />

        <section className="panel results-panel">
          <div className="panel-header">
            <h2 className="panel-title">📊 Métricas Extraídas (OpenCV)</h2>
            <span className="panel-badge">Passo 2</span>
          </div>

          {resultado ? (
            <div className="results-content">
              <MetricsGrid data={resultado} />
              <TagsList tags={resultado.tags_automaticas} />
              <JsonViewer data={resultado} />
            </div>
          ) : (
            <div className="empty-results-box">
              <div className="empty-icon">🔬</div>
              <p className="empty-title">Nenhum resultado para exibir</p>
              <p className="empty-desc">
                Selecione uma imagem no painel à esquerda e clique em <strong>Analisar Imagem</strong> para visualizar a extração de métricas do OpenCV.
              </p>
            </div>
          )}
        </section>
      </main>

      <footer className="lab-footer">
        <p>LASIC Vision API • Apresentação Técnica &copy; {new Date().getFullYear()}</p>
      </footer>
    </div>
  );
}

export default App;
