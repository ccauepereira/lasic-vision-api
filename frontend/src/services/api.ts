import type { HealthResponse, AnaliseImagemResponse } from '../types/api';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export async function fetchHealth(): Promise<HealthResponse> {
  const response = await fetch(`${API_BASE_URL}/health`, {
    method: 'GET',
    headers: {
      'Accept': 'application/json',
    },
  });

  if (!response.ok) {
    throw new Error(`Erro na resposta do backend: ${response.status} ${response.statusText}`);
  }

  return response.json();
}

export async function analisarImagem(file: File): Promise<AnaliseImagemResponse> {
  const formData = new FormData();
  formData.append('arquivo', file);

  const response = await fetch(`${API_BASE_URL}/analises/imagem`, {
    method: 'POST',
    body: formData,
  });

  if (!response.ok) {
    let errorDetail = `Erro HTTP ${response.status}`;
    try {
      const errJson = await response.json();
      if (errJson.detail) {
        errorDetail = typeof errJson.detail === 'string' 
          ? errJson.detail 
          : JSON.stringify(errJson.detail);
      }
    } catch {
      // Ignora erro de parse
    }
    throw new Error(errorDetail);
  }

  return response.json();
}
