```markdown
# LASIC Vision API

API desenvolvida em FastAPI para gerenciar tarefas de análise de imagens em um contexto acadêmico/laboratorial.

O projeto possui backend em Python com FastAPI, banco SQLite com SQLAlchemy, análise simples de imagem com OpenCV e frontend em React + TypeScript para consumir a API.

## Objetivo

A LASIC Vision API organiza o fluxo de uma tarefa de análise de imagem:

1. Criar tarefa;
2. Atribuir responsável;
3. Iniciar análise;
4. Enviar imagem;
5. Extrair métricas com OpenCV;
6. Salvar resultado;
7. Concluir tarefa;
8. Visualizar dados no frontend.

## Tecnologias

### Backend
- Python 3.10
- FastAPI
- Pydantic
- SQLAlchemy
- SQLite
- OpenCV
- NumPy
- Pytest

### Frontend
- React
- TypeScript
- Vite
- Lucide React

### Container
- Dockerfile
- Podman/Docker
- Volume local para persistência do SQLite

## Arquitetura

O projeto usa uma arquitetura em camadas inspirada em Clean Code, SOLID e separação de responsabilidades.

```text
app/
├── main.py
├── api/
│   └── rotas/
│       ├── saude.py
│       └── tarefas.py
├── esquemas/
│   ├── tarefa.py
│   └── analise_imagem.py
├── dominio/
│   ├── entidades/
│   │   ├── tarefa.py
│   └── resultado_analise_imagem.py
│   ├── enumeracoes.py
│   ├── excecoes.py
│   └── protocolos.py
├── servicos/
│   └── servico_tarefa.py
├── repositorios/
│   └── sqlite/
│       └── repositorio_tarefa_sqlite.py
├── banco/
│   ├── conexao.py
│   └── modelos_sqlalchemy.py
└── visao/
    └── analisador_imagem_opencv.py

```

### Responsabilidade das Camadas

* **`main.py`**: Monta a aplicação FastAPI, registra as rotas, configura CORS, trata exceções globais e cria as tabelas do banco no startup.
* **`api/rotas`**: Define os endpoints HTTP. As rotas recebem requisições, chamam os serviços e retornam respostas JSON.
* **`esquemas`**: Define os contratos de entrada e saída da API usando Pydantic.
* **`dominio`**: Concentra as regras principais do sistema, como status da tarefa, validações de negócio e entidades.
* **`servicos`**: Coordena os casos de uso da aplicação, como criar tarefa, iniciar tarefa, analisar imagem e concluir tarefa.
* **`repositorios`**: Isola o acesso ao banco de dados. O restante do sistema trabalha com entidades do domínio, não diretamente com tabelas SQLAlchemy.
* **`banco`**: Configura o SQLite, cria sessões e define os modelos SQLAlchemy usados para persistência.
* **`visao`**: Isola o uso do OpenCV e NumPy para extrair métricas simples de imagens.

### Fluxo da Aplicação

```text
Frontend React
       ↓ (HTTP / JSON / FormData)
Rotas FastAPI
       ↓
Schemas Pydantic
       ↓
ServicoTarefa
       ↓
Dominio
       ↓
Repositorio SQLite
       ↓
Banco SQLite

```

No caso de análise de imagem, o service também chama o módulo de visão:

```text
ServicoTarefa
       ↓
AnalisadorImagemOpenCV
       ↓
ResultadoAnaliseImagem

```

### Regras de Negócio

* Uma tarefa nasce com status `pendente`;
* Uma tarefa `pendente` pode receber responsável;
* Uma tarefa só pode iniciar se possuir responsável;
* Uma tarefa iniciada fica com status `em_andamento`;
* Somente uma tarefa `em_andamento` pode receber resultado de análise;
* Uma tarefa só pode ser concluída se possuir resultado de análise;
* Uma tarefa `concluida` não deve ser alterada pelo fluxo principal.

## Endpoints

### Saúde

| Método | Rota | Descrição |
| --- | --- | --- |
| GET | `/health` | Verifica se a API está disponível |

### Tarefas

| Método | Rota | Descrição |
| --- | --- | --- |
| POST | `/tarefas` | Cria uma tarefa |
| GET | `/tarefas` | Lista todas as tarefas |
| GET | `/tarefas/{tarefa_id}` | Busca tarefa por ID |
| PATCH | `/tarefas/{tarefa_id}/responsavel` | Atribui responsável |
| POST | `/tarefas/{tarefa_id}/iniciar` | Inicia uma tarefa |
| POST | `/tarefas/{tarefa_id}/analises/imagem` | Analisa imagem da tarefa |
| POST | `/tarefas/{tarefa_id}/concluir` | Conclui uma tarefa |

### Exemplo de Fluxo no Swagger

1. Acesse `http://127.0.0.1:8000/docs`.
2. Execute `GET /health`.
3. Execute `POST /tarefas`.
4. Copie o `tarefa_id`.
5. Execute `PATCH /tarefas/{tarefa_id}/responsavel`.
6. Execute `POST /tarefas/{tarefa_id}/iniciar`.
7. Execute `POST /tarefas/{tarefa_id}/analises/imagem`.
8. Execute `POST /tarefas/{tarefa_id}/concluir`.
9. Execute `GET /tarefas/{tarefa_id}`.

## Análise de Imagem com OpenCV

A imagem enviada é processada pelo arquivo: `app/visao/analisador_imagem_opencv.py`.

A API extrai:

| Campo | Descrição |
| --- | --- |
| `largura` | largura da imagem em pixels |
| `altura` | altura da imagem em pixels |
| `formato` | extensão/formato da imagem |
| `modo_cor` | modo de cor identificado |
| `brilho_medio` | média dos pixels em tons de cinza |
| `contraste_medio` | desvio padrão dos pixels em tons de cinza |
| `quantidade_bordas` | total de bordas detectadas com Canny |
| `classificacao_brilho` | classifica a imagem como escura, normal ou clara |
| `classificacao_contraste` | classifica o contraste |
| `tags_automaticas` | tags geradas a partir das métricas |

Trecho central da análise:

```python
brilho_medio = float(np.mean(imagem_cinza))
contraste_medio = float(np.std(imagem_cinza))
bordas = cv2.Canny(imagem_cinza, 100, 200)

```

## Banco de Dados

O projeto usa **SQLite** com **SQLAlchemy**. O SQLite salva os dados em um arquivo local: `lasic_vision.db`

* A conexão fica em: `app/banco/conexao.py`
* Os modelos de tabela ficam em: `app/banco/modelos_sqlalchemy.py`
* O repository fica em: `app/repositorios/sqlite/repositorio_tarefa_sqlite.py`

Essa separação evita que as rotas e regras de negócio dependam diretamente do banco de dados.

## Frontend

O frontend está no diretório: `frontend/`

Ele foi desenvolvido com **React, TypeScript e Vite**. O arquivo que centraliza o consumo da API é: `frontend/src/servicos/cliente_api.ts`

O frontend consome a API usando `fetch`, envia JSON para criar e atualizar tarefas e usa `FormData` para enviar imagens.

## Como Rodar Sem Docker

### Backend

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload

```

* **Backend:** `http://127.0.0.1:8000`
* **Swagger:** `http://127.0.0.1:8000/docs`

### Frontend

```bash
cd frontend
npm install
npm run dev

```

* **Frontend:** `http://127.0.0.1:5173`

## Como Rodar Com Podman/Docker

### Backend

Na raiz do projeto:

```bash
podman build -t lasic-vision-backend .
mkdir -p dados
podman run --rm \
  -p 8000:8000 \
  -v "$(pwd)/dados:/app/dados" \
  lasic-vision-backend

```

### Frontend

Em outro terminal:

```bash
cd frontend
podman build -t lasic-vision-frontend .
podman run --rm \
  -p 5173:5173 \
  -e VITE_URL_API=[http://127.0.0.1:8000](http://127.0.0.1:8000) \
  lasic-vision-frontend

```

## Testes

Os testes estão em: `app/tests/`

Para executar:

```bash
pytest

```

Os testes cobrem regras de domínio, serviço de tarefas e rotas principais da API.

## Status do Projeto

O projeto possui:

* [x] Backend FastAPI funcionando;
* [x] Frontend React consumindo a API;
* [x] Banco SQLite persistindo tarefas e resultados;
* [x] OpenCV extraindo métricas simples de imagem;
* [x] Dockerfile para backend;
* [x] Dockerfile para frontend;
* [x] Testes automatizados com Pytest;
* [x] Organização em camadas com separação de responsabilidades.

## Autor

**Cauê Cavalcante Pereira**
Projeto acadêmico desenvolvido para estudo e apresentação no contexto do LASIC.

```

```
