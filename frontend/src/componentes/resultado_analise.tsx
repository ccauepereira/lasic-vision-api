import type { ResultadoAnalise } from '../tipos/tarefa';

interface ResultadoAnaliseProps {
  resultado: ResultadoAnalise;
}

export function ResultadoAnaliseVisual({ resultado }: ResultadoAnaliseProps) {
  return (
    <div style={{ marginTop: '2rem' }}>
      <h3>Resultado da Analise OpenCV</h3>
      <div className="resultado-grid">
        <div className="resultado-item">
          <span>Dimensoes</span>
          <strong>{resultado.largura} x {resultado.altura}</strong>
        </div>
        <div className="resultado-item">
          <span>Formato</span>
          <strong>{resultado.formato}</strong>
        </div>
        <div className="resultado-item">
          <span>Modo de Cor</span>
          <strong>{resultado.modoCor}</strong>
        </div>
        <div className="resultado-item">
          <span>Brilho</span>
          <strong>{resultado.brilhoMedio.toFixed(1)} ({resultado.classificacaoBrilho})</strong>
        </div>
        <div className="resultado-item">
          <span>Contraste</span>
          <strong>{resultado.contrasteMedio.toFixed(1)} ({resultado.classificacaoContraste})</strong>
        </div>
        <div className="resultado-item">
          <span>Quantidade Bordas</span>
          <strong>{resultado.quantidadeBordas}</strong>
        </div>
      </div>
      <div style={{ marginTop: '1rem' }}>
        <h4>Tags Automaticas</h4>
        <div className="tags-lista">
          {resultado.tagsAutomaticas.map(tag => (
            <span key={tag} className="tag-badge">{tag}</span>
          ))}
        </div>
      </div>
    </div>
  );
}