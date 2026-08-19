import React from 'react';

interface JsonViewerProps {
  data: unknown;
}

export const JsonViewer: React.FC<JsonViewerProps> = ({ data }) => {
  return (
    <div className="json-section">
      <h3 className="section-subtitle">💻 JSON Bruto Retornado pela API</h3>
      <pre className="json-box">
        <code>{JSON.stringify(data, null, 2)}</code>
      </pre>
    </div>
  );
};
