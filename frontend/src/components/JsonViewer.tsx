import React, { useState } from 'react';

interface JsonViewerProps {
  data: unknown;
  title?: string;
}

export const JsonViewer: React.FC<JsonViewerProps> = ({
  data,
  title = 'JSON Bruto Retornado pela API (Didático)',
}) => {
  const [isCopied, setIsCopied] = useState(false);
  const [isExpanded, setIsExpanded] = useState(true);

  const jsonString = JSON.stringify(data, null, 2);

  const handleCopy = () => {
    navigator.clipboard.writeText(jsonString).then(() => {
      setIsCopied(true);
      setTimeout(() => setIsCopied(false), 2000);
    });
  };

  return (
    <section className="json-section" id="raw-json-section">
      <div className="json-header">
        <h2 className="section-title margin-0">
          <span className="icon">💻</span> {title}
        </h2>
        <div className="json-controls">
          <button
            type="button"
            id="btn-copy-json"
            className="btn btn-sm btn-secondary"
            onClick={handleCopy}
          >
            {isCopied ? '✅ Copiado!' : '📋 Copiar JSON'}
          </button>
          <button
            type="button"
            id="btn-toggle-json"
            className="btn btn-sm btn-secondary"
            onClick={() => setIsExpanded(!isExpanded)}
          >
            {isExpanded ? '🔽 Ocultar' : '▶️ Expandir'}
          </button>
        </div>
      </div>

      {isExpanded && (
        <div className="json-code-wrapper">
          <pre className="json-code" id="raw-json-content">
            <code>{jsonString}</code>
          </pre>
        </div>
      )}
    </section>
  );
};
