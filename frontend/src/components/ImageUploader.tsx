import React from 'react';

interface ImageUploaderProps {
  previewUrl: string | null;
  selectedFile: File | null;
  isAnalyzing: boolean;
  apiError: string | null;
  onFileChange: (e: React.ChangeEvent<HTMLInputElement>) => void;
  onClearFile: () => void;
  onAnalyze: () => void;
}

export const ImageUploader: React.FC<ImageUploaderProps> = ({
  previewUrl,
  selectedFile,
  isAnalyzing,
  apiError,
  onFileChange,
  onClearFile,
  onAnalyze,
}) => {
  return (
    <section className="panel upload-panel">
      <div className="panel-header">
        <h2 className="panel-title">📷 Entrada de Imagem</h2>
        <span className="panel-badge">Passo 1</span>
      </div>

      <div className="upload-box-wrapper">
        <label htmlFor="image-input" className={`upload-zone ${previewUrl ? 'has-file' : ''}`}>
          <input
            id="image-input"
            type="file"
            accept="image/*"
            onChange={onFileChange}
            className="file-input-hidden"
          />

          {previewUrl ? (
            <div className="preview-content">
              <img src={previewUrl} alt="Preview da imagem selecionada" className="preview-image" />
              <div className="file-meta">
                <span className="file-name">{selectedFile?.name}</span>
                <span className="file-size">
                  {(selectedFile?.size ? selectedFile.size / 1024 : 0).toFixed(1)} KB
                </span>
              </div>
            </div>
          ) : (
            <div className="upload-prompt">
              <div className="upload-icon-circle">🖼️</div>
              <p className="upload-text-main">Clique para selecionar uma imagem</p>
              <p className="upload-text-sub">Formatos aceitos: PNG, JPG, JPEG, BMP</p>
            </div>
          )}
        </label>
      </div>

      <div className="action-row">
        {selectedFile && (
          <button
            type="button"
            className="btn btn-secondary"
            onClick={onClearFile}
            disabled={isAnalyzing}
          >
            Limpar
          </button>
        )}

        <button
          type="button"
          className="btn btn-primary btn-grow"
          onClick={onAnalyze}
          disabled={!selectedFile || isAnalyzing}
        >
          {isAnalyzing ? (
            <span className="loading-inline">
              <span className="spinner spinner-light"></span> Processando imagem...
            </span>
          ) : (
            'Analisar Imagem'
          )}
        </button>
      </div>

      {apiError && (
        <div className="alert-error">
          <span className="alert-icon">⚠️</span>
          <div className="alert-body">
            <strong>Erro na Chamada da API:</strong>
            <p>{apiError}</p>
          </div>
        </div>
      )}
    </section>
  );
};
