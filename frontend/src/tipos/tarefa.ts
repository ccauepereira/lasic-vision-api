export type StatusTarefa = 'pendente' | 'em_andamento' | 'concluida';

export interface ResultadoAnalise {
  nomeArquivo?: string;
  largura: number;
  altura: number;
  formato: string;
  modoCor: string;
  brilhoMedio: number;
  contrasteMedio: number;
  classificacaoBrilho: string;
  classificacaoContraste: string;
  quantidadeBordas: number;
  tagsAutomaticas: string[];
  criadoEm?: string;
}

export interface Tarefa {
  id: string;
  titulo: string;
  descricao: string | null;
  responsavel: string | null;
  status: StatusTarefa;
  resultadoAnalise: ResultadoAnalise | null;
  criadoEm?: string;
  atualizadoEm?: string;
}

export interface RespostaAnaliseBackend {
  nome_arquivo: string;
  largura: number;
  altura: number;
  formato: string;
  modo_cor: string;
  brilho_medio: number;
  contraste_medio: number;
  classificacao_brilho: string;
  classificacao_contraste: string;
  quantidade_bordas: number;
  tags_automaticas: string[];
  criado_em: string;
}

export interface RespostaTarefaBackend {
  tarefa_id: string;
  titulo: string;
  descricao: string | null;
  responsavel: string | null;
  status: StatusTarefa;
  resultado_analise: RespostaAnaliseBackend | null;
  criado_em: string;
  atualizado_em: string;
}

export interface RespostaSaudeBackend {
  status: string;
  projeto: string;
  versao: string;
}