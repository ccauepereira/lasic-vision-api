import { useState } from 'react';
import './App.css';

// Interfaces TypeScript para respostas da API
interface HealthResponse {
  status: string;
  projeto: string;
  versao: string;
}

interface AnaliseResponse {
  arquivo: string;
  largura: number;
  altura: number;
  modo_cor: string;
  brilho_medio: number;
  contraste_medio: number;
  quantidade_bordas: number;
  classificacao_brilho: string;
  classificacao_contraste: string;
  tags_automaticas: string[];
}

export function App() {
  // Estados para o endpoint GET /health
  const [healthData, setHealthData] = useState<HealthResponse | null>(null);
  const [healthLoading, setHealthLoading] = useState<boolean>(false);
  const [healthError, setHealthError] = useState<string | null>(null);

  // Estados para upload e preview da imagem
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);

  // Estados para a resposta da análise POST /analises/imagem
  const [resultado, setResultado] = useState<AnaliseResponse | null>(null);
  const [isAnalyzing, setIsAnalyzing] = useState<boolean>(false);
  const [apiError, setApiError] = useState<string | null>(null);

  // 1. Função para testar GET http://127.0.0.1:8000/health
  const testarHealth = async () => {
    setHealthLoading(true);
    setHealthError(null);
    try {
      const res = await fetch('http://127.0.0.1:8000/health');
      if (!res.ok) {
        throw new Error(`Status ${res.status}: ${res.statusText}`);
      }
      const data: HealthResponse = await res.json();
      setHealthData(data);
    } catch (err) {
      setHealthError(err instanceof Error ? err.message : 'Falha ao conectar no endpoint /health');
      setHealthData(null);
    } finally {
      setHealthLoading(false);
    }
  };

  // 2 e 3. Manipular seleção de arquivo de imagem e preview
  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      setSelectedFile(file);
      setPreviewUrl(URL.createObjectURL(file));
      setResultado(null);
      setApiError(null);
    }
  };

  // 4 e 5. Função para enviar a imagem via POST FormData para http://127.0.0.1:8000/analises/imagem
  const analisarImagem = async () => {
    if (!selectedFile) return;

    setIsAnalyzing(true);
    setApiError(null);
    setResultado(null);

    const formData = new FormData();
    formData.append('arquivo', selectedFile);

    try {
      const res = await fetch('http://127.0.0.1:8000/analises/imagem', {
        method: 'POST',
        body: formData,
      });

      if (!res.ok) {
        let message = `Erro ${res.status}`;
        try {
          const errBody = await res.json();
          if (errBody.detail) {
            message = typeof errBody.detail === 'string' ? errBody.detail : JSON.stringify(errBody.detail);
          }
        } catch {
          // Ignora erro ao ler corpo de erro
        }
        throw new Error(message);
      }

      const data: AnaliseResponse = await res.json();
      setResultado(data);
    } catch (err) {
      setApiError(err instanceof Error ? err.message : 'Erro ao processar imagem na API');
    } finally {
      setIsAnalyzing(false);
    }
  };

  return (
    <div className="lab-container">
      {/* Cabeçalho */}
      <header className="lab-header">
        <div className="header-titles">
          <h1 className="lab-title">Cauê Test</h1>
          <p className="lab-subtitle">Teste visual da LASIC Vision API com FastAPI + OpenCV</p>
        </div>

        {/* 1. Botão para testar GET /health */}
        <div className="health-section">
          <button 
            type="button" 
            className="btn btn-outline" 
            onClick={testarHealth}
            disabled={healthLoading}
          >
            {healthLoading ? 'Verificando...' : 'Testar GET /health'}
          </button>

          {healthData && (
            <span className="health-badge health-success">
              ✓ Status: {healthData.status} ({healthData.projeto} v{healthData.versao})
            </span>
          )}

          {healthError && (
            <span className="health-badge health-error">
              ✕ Off-line: {healthError}
            </span>
          )}
        </div>
      </header>

      {/* Grid Principal do Laboratório */}
      <main className="lab-main-grid">
        {/* Painel Esquerdo: Seleção e Preview de Imagem */}
        <section className="panel">
          <h2 className="panel-title">1. Entrada de Imagem</h2>

          <div className="form-group">
            <label htmlFor="image-input" className="file-label">
              Selecionar imagem do computador:
            </label>
            {/* 2. Campo para selecionar imagem */}
            <input
              id="image-input"
              type="file"
              accept="image/*"
              onChange={handleFileChange}
              className="file-input"
            />
          </div>

          {/* 3. Preview da Imagem */}
          {previewUrl ? (
            <div className="preview-box">
              <p className="preview-caption">Preview do Arquivo Selecionado:</p>
              <img src={previewUrl} alt="Preview da imagem selecionada" className="preview-img" />
              <p className="file-details">
                <strong>Arquivo:</strong> {selectedFile?.name} ({(selectedFile?.size ? selectedFile.size / 1024 : 0).toFixed(1)} KB)
              </p>
            </div>
          ) : (
            <div className="empty-preview">
              Nenhuma imagem selecionada. Escolha um arquivo acima.
            </div>
          )}

          {/* 4. Botão Analisar Imagem */}
          <button
            type="button"
            className="btn btn-primary btn-block"
            onClick={analisarImagem}
            disabled={!selectedFile || isAnalyzing}
          >
            {/* 6. Loading enquanto analisa */}
            {isAnalyzing ? (
              <span className="loading-text">
                <span className="spinner"></span> Analisando imagem...
              </span>
            ) : (
              'Analisar Imagem'
            )}
          </button>

          {/* 7. Mensagem de Erro se a API falhar */}
          {apiError && (
            <div className="error-banner">
              <strong>Erro na requisição:</strong> {apiError}
            </div>
          )}
        </section>

        {/* Painel Direito: Resultados da Análise */}
        <section className="panel">
          <h2 className="panel-title">2. Resultados da Análise</h2>

          {resultado ? (
            <div className="results-container">
              {/* 8. Cards com as métricas retornadas */}
              <div className="metrics-grid">
                <div className="card">
                  <span className="card-label">Arquivo</span>
                  <span className="card-value font-mono">{resultado.arquivo}</span>
                </div>

                <div className="card">
                  <span className="card-label">Largura</span>
                  <span className="card-value">{resultado.largura} px</span>
                </div>

                <div className="card">
                  <span className="card-label">Altura</span>
                  <span className="card-value">{resultado.altura} px</span>
                </div>

                <div className="card">
                  <span className="card-label">Modo de Cor</span>
                  <span className="card-value">{resultado.modo_cor}</span>
                </div>

                <div className="card">
                  <span className="card-label">Brilho Médio</span>
                  <span className="card-value">{resultado.brilho_medio}</span>
                </div>

                <div className="card">
                  <span className="card-label">Contraste Médio</span>
                  <span className="card-value">{resultado.contraste_medio}</span>
                </div>

                <div className="card">
                  <span className="card-label">Quantidade de Bordas</span>
                  <span className="card-value">{resultado.quantidade_bordas}</span>
                </div>

                <div className="card">
                  <span className="card-label">Classificação de Brilho</span>
                  <span className="card-value badge-text">{resultado.classificacao_brilho}</span>
                </div>

                <div className="card">
                  <span className="card-label">Classificação de Contraste</span>
                  <span className="card-value badge-text">{resultado.classificacao_contraste}</span>
                </div>
              </div>

              {/* 9. Tags Automáticas como Badges */}
              <div className="tags-block">
                <h3 className="sub-title">Tags Automáticas:</h3>
                <div className="badges-list">
                  {resultado.tags_automaticas.map((tag, idx) => (
                    <span key={idx} className="badge">
                      {tag}
                    </span>
                  ))}
                </div>
              </div>

              {/* 10. JSON Bruto Retornado */}
              <div className="json-block">
                <h3 className="sub-title">JSON Bruto Retornado pela API:</h3>
                <pre className="json-box">
                  <code>{JSON.stringify(resultado, null, 2)}</code>
                </pre>
              </div>
            </div>
          ) : (
            <div className="empty-results">
              Aguardando envio de imagem para exibir as métricas de análise.
            </div>
          )}
        </section>
      </main>
    </div>
  );
}

export default App;
