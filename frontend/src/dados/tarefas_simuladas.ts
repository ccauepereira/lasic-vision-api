import type { Tarefa } from '../tipos/tarefa';

export const tarefasSimuladas: Tarefa[] = [
  {
    id: 1,
    titulo: 'Analise de placa de circuito',
    descricao: 'Verificar defeitos na solda.',
    responsavel: 'Maria',
    status: 'concluida',
    resultadoAnalise: {
      largura: 1920,
      altura: 1080,
      formato: 'JPEG',
      modoCor: 'RGB',
      brilhoMedio: 120.5,
      contrasteMedio: 55.2,
      classificacaoBrilho: 'Normal',
      classificacaoContraste: 'Medio',
      quantidadeBordas: 1250,
      tagsAutomaticas: ['circuito', 'solda', 'eletronica'],
    }
  },
  {
    id: 2,
    titulo: 'Validacao de lamina microscopica',
    descricao: 'Contagem de celulas anormais.',
    responsavel: 'Joao',
    status: 'em_andamento',
    resultadoAnalise: null
  },
  {
    id: 3,
    titulo: 'Inspecao de componente metalico',
    descricao: 'Procurar por rachaduras e desgaste.',
    responsavel: null,
    status: 'pendente',
    resultadoAnalise: null
  }
];