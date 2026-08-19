import React, { useState, useRef } from 'react';
import type { DragEvent, ChangeEvent } from 'react';

interface ImageUploaderProps {
  onAnalyze: (file: File) => void;
  isLoading: boolean;
  selectedFile: File | null;
  setSelectedFile: (file: File | null) => void;
  previewUrl: string | null;
  setPreviewUrl: (url: string | null) => void;
}

export const ImageUploader: React.FC<ImageUploaderProps> = ({
  onAnalyze,
  isLoading,
  selectedFile,
  setSelectedFile,
  previewUrl,
  setPreviewUrl,
}) => {
  const [isDragging, setIsDragging] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleFileSelect = (file: File) => {
    if (!file.type.startsWith('image/')) {
      alert('Por favor, selecione um arquivo de imagem válido (PNG, JPG, JPEG, WEBP, etc).');
      return;
    }

    setSelectedFile(file);
    const url = URL.createObjectURL(file);
    setPreviewUrl(url);
  };

  const handleInputChange = (e: ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      handleFileSelect(e.target.files[0]);
    }
  };

  const handleDragOver = (e: DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(true);
  };

  const handleDragLeave = (e: DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(false);
  };

  const handleDrop = (e: DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(false);

    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFileSelect(e.dataTransfer.files[0]);
    }
  };

  const handleClear = () => {
    setSelectedFile(null);
    if (previewUrl) {
      URL.revokeObjectURL(previewUrl);
      setPreviewUrl(null);
    }
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (selectedFile && !isLoading) {
      onAnalyze(selectedFile);
    }
  };

  const formatFileSize = (bytes: number): string => {
    if (bytes < 1024) return `${bytes} B`;
    if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
    return `${(bytes / (1024 * 1024)).toFixed(2)} MB`;
  };

  return (
    <section className="uploader-section">
      <h2 className="section-title">
        <span className="icon">📁</span> Upload de Imagem para Análise
      </h2>

      <form onSubmit={handleSubmit}>
        <div
          id="dropzone"
          className={`dropzone ${isDragging ? 'dragging' : ''} ${previewUrl ? 'has-preview' : ''}`}
          onDragOver={handleDragOver}
          onDragLeave={handleDragLeave}
          onDrop={handleDrop}
          onClick={() => !previewUrl && fileInputRef.current?.click()}
        >
          <input
            type="file"
            id="image-file-input"
            ref={fileInputRef}
            onChange={handleInputChange}
            accept="image/*"
            style={{ display: 'none' }}
          />

          {previewUrl ? (
            <div className="preview-container">
              <img src={previewUrl} alt="Preview da imagem" className="image-preview" />
              <div className="file-info-overlay">
                <span className="file-name">{selectedFile?.name}</span>
                <span className="file-size">{selectedFile && formatFileSize(selectedFile.size)}</span>
              </div>
            </div>
          ) : (
            <div className="dropzone-prompt">
              <div className="upload-icon">📸</div>
              <p className="prompt-main">Arraste e solte uma imagem aqui</p>
              <p className="prompt-sub">ou clique para selecionar do computador</p>
              <span className="supported-formats">Suporta PNG, JPG, JPEG, WEBP, BMP</span>
            </div>
          )}
        </div>

        <div className="action-buttons">
          {previewUrl && (
            <button
              type="button"
              id="btn-clear-image"
              className="btn btn-secondary"
              onClick={handleClear}
              disabled={isLoading}
            >
              🔄 Limpar / Outra Imagem
            </button>
          )}

          <button
            type="submit"
            id="btn-submit-analysis"
            className="btn btn-primary"
            disabled={!selectedFile || isLoading}
          >
            {isLoading ? (
              <>
                <span className="spinner"></span> Analisando Imagem...
              </>
            ) : (
              <>⚡ Executar Análise Vision API</>
            )}
          </button>
        </div>
      </form>
    </section>
  );
};
