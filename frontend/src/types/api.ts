export interface HealthResponse {
  status: string;
  projeto: string;
  versao: string;
}

export interface AnaliseImagemResponse {
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
