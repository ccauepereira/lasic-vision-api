import type {
  Tarefa,
  ResultadoAnalise,
  RespostaAnaliseBackend,
  RespostaTarefaBackend,
  RespostaSaudeBackend,
} from '../tipos/tarefa';

const URL_API = import.meta.env.VITE_URL_API || 'http://localhost:8000';

function mapearResultadoAnalise(dados: RespostaAnaliseBackend): ResultadoAnalise {
  return {
    nomeArquivo: dados.nome_arquivo,
    largura: dados.largura,
    altura: dados.altura,
    formato: dados.formato,
    modoCor: dados.modo_cor,
    brilhoMedio: dados.brilho_medio,
    contrasteMedio: dados.contraste_medio,
    classificacaoBrilho: dados.classificacao_brilho,
    classificacaoContraste: dados.classificacao_contraste,
    quantidadeBordas: dados.quantidade_bordas,
    tagsAutomaticas: dados.tags_automaticas,
    criadoEm: dados.criado_em,
  };
}

function mapearTarefa(dados: RespostaTarefaBackend): Tarefa {
  return {
    id: dados.tarefa_id,
    titulo: dados.titulo,
    descricao: dados.descricao,
    responsavel: dados.responsavel,
    status: dados.status,
    resultadoAnalise: dados.resultado_analise
      ? mapearResultadoAnalise(dados.resultado_analise)
      : null,
    criadoEm: dados.criado_em,
    atualizadoEm: dados.atualizado_em,
  };
}

async function tratarRespostaErro(resposta: Response): Promise<never> {
  let mensagemErro = `Erro HTTP ${resposta.status}`;
  try {
    const json = await resposta.json();
    if (json && typeof json.detail === 'string') {
      mensagemErro = json.detail;
    } else if (json && Array.isArray(json.detail)) {
      mensagemErro = json.detail
        .map((item: { msg?: string }) => item.msg || 'Erro de validacao')
        .join(', ');
    }
  } catch {
    // resposta nao e JSON
  }
  throw new Error(mensagemErro);
}

export async function verificarSaude(): Promise<boolean> {
  try {
    const resposta = await fetch(`${URL_API}/health`);
    if (!resposta.ok) {
      return false;
    }
    const dados: RespostaSaudeBackend = await resposta.json();
    return dados.status === 'ok';
  } catch {
    return false;
  }
}

export async function listarTarefas(): Promise<Tarefa[]> {
  const resposta = await fetch(`${URL_API}/tarefas`);
  if (!resposta.ok) {
    await tratarRespostaErro(resposta);
  }
  const dados: RespostaTarefaBackend[] = await resposta.json();
  return dados.map(mapearTarefa);
}

export async function buscarTarefa(tarefaId: string): Promise<Tarefa> {
  const resposta = await fetch(`${URL_API}/tarefas/${tarefaId}`);
  if (!resposta.ok) {
    await tratarRespostaErro(resposta);
  }
  const dados: RespostaTarefaBackend = await resposta.json();
  return mapearTarefa(dados);
}

export async function criarTarefa(
  titulo: string,
  descricao?: string | null
): Promise<Tarefa> {
  const resposta = await fetch(`${URL_API}/tarefas`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      titulo,
      descricao: descricao || null,
    }),
  });
  if (!resposta.ok) {
    await tratarRespostaErro(resposta);
  }
  const dados: RespostaTarefaBackend = await resposta.json();
  return mapearTarefa(dados);
}

export async function atribuirResponsavel(
  tarefaId: string,
  responsavel: string
): Promise<Tarefa> {
  const resposta = await fetch(`${URL_API}/tarefas/${tarefaId}/responsavel`, {
    method: 'PATCH',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      responsavel,
    }),
  });
  if (!resposta.ok) {
    await tratarRespostaErro(resposta);
  }
  const dados: RespostaTarefaBackend = await resposta.json();
  return mapearTarefa(dados);
}

export async function iniciarTarefa(tarefaId: string): Promise<Tarefa> {
  const resposta = await fetch(`${URL_API}/tarefas/${tarefaId}/iniciar`, {
    method: 'POST',
  });
  if (!resposta.ok) {
    await tratarRespostaErro(resposta);
  }
  const dados: RespostaTarefaBackend = await resposta.json();
  return mapearTarefa(dados);
}

export async function analisarImagem(
  tarefaId: string,
  arquivo: File
): Promise<ResultadoAnalise> {
  const formData = new FormData();
  formData.append('arquivo', arquivo);

  const resposta = await fetch(`${URL_API}/tarefas/${tarefaId}/analises/imagem`, {
    method: 'POST',
    body: formData,
  });
  if (!resposta.ok) {
    await tratarRespostaErro(resposta);
  }
  const dados: RespostaAnaliseBackend = await resposta.json();
  return mapearResultadoAnalise(dados);
}

export async function concluirTarefa(tarefaId: string): Promise<Tarefa> {
  const resposta = await fetch(`${URL_API}/tarefas/${tarefaId}/concluir`, {
    method: 'POST',
  });
  if (!resposta.ok) {
    await tratarRespostaErro(resposta);
  }
  const dados: RespostaTarefaBackend = await resposta.json();
  return mapearTarefa(dados);
}
