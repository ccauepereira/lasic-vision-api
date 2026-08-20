export type StatusTarefa = 'pendente' | 'em_andamento' | 'concluida';

export interface ResultadoAnalise {
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
}

export interface Tarefa {
  id: number;
  titulo: string;
  descricao: string;
  responsavel: string | null;
  status: StatusTarefa;
  resultadoAnalise: ResultadoAnalise | null;
}