# LASIC Vision API — Documentação do Projeto

API desenvolvida em FastAPI para organização e execução de análises computacionais de imagens em contexto acadêmico/laboratorial, aplicando GitFlow, POO em Python, princípios SOLID, Clean Code e testes automatizados.

---

## 🖥️ Seção: Cauê Test (Interface da Branch `feature/fastapi-basic`)

### 1. O que é o Cauê Test?
O **Cauê Test** é um painel visual didático e interativo desenvolvido em **React + TypeScript + Vite** dentro do diretório `frontend/`. Ele funciona como um cliente de laboratório para testar e demonstrar em tempo real os endpoints expostos pela **LASIC Vision API**.

---

### 2. Qual problema ele resolve?
Antes da criação desta interface, a verificação das métricas extraídas pelo OpenCV dependia do envio manual de requisições via cURL, Postman ou pela documentação OpenAPI/Swagger (`/docs`). 

O **Cauê Test** resolve esse problema ao fornecer:
- Uma interface gráfica limpa e responsiva.
- Preview imediato da imagem selecionada.
- Exibição de métricas estruturadas em *cards* visuais.
- Agrupamento de tags automáticas em *badges*.
- Apresentação didática do JSON bruto retornado pela API para fins de inspeção e validação acadêmica.

---

### 3. Como o Frontend conversa com o Backend?

A comunicação ocorre via protocolo HTTP (REST) entre o cliente React (`http://127.0.0.1:5173`) e o servidor FastAPI (`http://127.0.0.1:8000`):

1. **Checagem de Integridade (`GET /health`)**:
   - O botão `⚡ Testar GET /health` dispara uma requisição `GET` sem corpo para `http://127.0.0.1:8000/health`.
   - O backend retorna um JSON confirmando o estado operacional (`{"status": "ok", "projeto": "LASIC Vision API", "versao": "0.1.0"}`).

2. **Envio e Análise de Imagem (`POST /analises/imagem`)**:
   - A imagem selecionada é empacotada em um objeto nativo `FormData` sob a chave `arquivo`.
   - O frontend envia uma requisição `POST` com o cabeçalho `multipart/form-data` para `http://127.0.0.1:8000/analises/imagem`.
   - O backend processa o arquivo via OpenCV e retorna um payload JSON contendo os dados analíticos.

3. **Configuração de CORS (Cross-Origin Resource Sharing)**:
   - Para permitir essa comunicação entre portas distintas (`:5173` -> `:8000`), o FastAPI utiliza o `CORSMiddleware` em `app/main.py`, liberando estritamente as origens `http://127.0.0.1:5173` e `http://localhost:5173`.

---

### 4. Como rodar o Backend

A partir da raiz do projeto (`lasic-vision-api/`):

```bash
# 1. Ativar o ambiente virtual Python
source .venv/bin/activate

# 2. Iniciar o servidor Uvicorn com hot-reload ativo na porta 8000
uvicorn app.main:app --reload --port 8000
```
> **Servidor Backend ativo em:** `http://127.0.0.1:8000`  
> **Documentação Swagger:** `http://127.0.0.1:8000/docs`

---

### 5. Como rodar o Frontend

Em um novo terminal, navegue até a pasta `frontend/`:

```bash
# 1. Entrar na pasta do frontend
cd frontend

# 2. Instalar as dependências do Node.js (caso necessário)
npm install

# 3. Iniciar o servidor de desenvolvimento Vite
npm run dev
```
> **Aplicação Frontend ativa em:** `http://localhost:5173`

---

### 6. Roteiro de Testes

#### Teste 1: Checagem do Endpoint `/health`
1. Com o backend e o frontend em execução, abra `http://localhost:5173`.
2. No cabeçalho superior, clique no botão **"⚡ Testar GET /health"**.
3. Observe a resposta: um badge verde indicará `✓ Status: ok (LASIC Vision API v0.1.0)`.

#### Teste 2: Upload e Análise de Imagem
1. No painel **"1. Entrada de Imagem"**, clique na área pontilhada para selecionar um arquivo de imagem (`.png`, `.jpg`, `.jpeg` ou `.bmp`).
2. Confirme se a imagem é carregada na área de *preview* com a indicação do nome e tamanho do arquivo.
3. Clique no botão **"Analisar Imagem"**.
4. Observe o indicador de carregamento (*loading spinner*).
5. Após o retorno do backend, veja no painel **"2. Resultados da Análise"**:
   - Os 9 *cards* contendo as métricas computadas.
   - As *badges* com as tags geradas automaticamente.
   - O bloco de código com o JSON bruto formatado.

---

### 7. Quais dados o OpenCV retorna?

A classe `OpenCVAnalyzer` (`app/vision/opencv_analyzer.py`) processa os bytes da imagem enviada e retorna a seguinte estrutura JSON:

| Campo | Tipo | Descrição / Método de Cálculo |
| :--- | :--- | :--- |
| `arquivo` | `string` | Nome original do arquivo enviado pelo cliente |
| `largura` | `integer` | Largura da imagem em pixels (`imagem.shape[1]`) |
| `altura` | `integer` | Altura da imagem em pixels (`imagem.shape[0]`) |
| `modo_cor` | `string` | Espaço de cor computado (ex: `"BGR com 3 canais"`) |
| `brilho_medio` | `float` | Média de luminância da imagem em escala de cinza (`np.mean`) |
| `contraste_medio` | `float` | Desvio padrão da luminância em escala de cinza (`np.std`) |
| `quantidade_bordas` | `integer` | Total de pixels de borda detectados pelo algoritmo Canny (`cv2.Canny`) |
| `classificacao_brilho` | `string` | Classificação categórica: `"escura"`, `"clara"` ou `"normal"` |
| `classificacao_contraste` | `string` | Classificação categórica: `"baixo_contraste"`, `"alto_contraste"` ou `"contraste_adequado"` |
| `tags_automaticas` | `list[str]` | Conjunto ordenado de tags geradas a partir das métricas extraídas |

---

### 8. Limitações Atuais do Sistema

Nesta etapa inicial do desenvolvimento (`feature/fastapi-basic`), o sistema possui as seguintes limitações deliberadas:

- **Visão Computacional Clássica**: A análise é puramente estatística/determinística usando algoritmos clássicos do OpenCV (médias, desvio padrão, filtro Canny). Não há uso de modelos de Inteligência Artificial ou Redes Neurais Convolucionais nesta fase.
- **Arquitetura Stateless (Sem Banco de Dados)**: As análises são processadas em memória e os resultados não são salvos em banco de dados relacional ou não-relacional.
- **Sem Autenticação/Autorização**: Todos os endpoints são públicos e não requerem tokens JWT ou controle de acesso.
- **Regras de Análise Simples**: As regras de classificação utilizam limiares estáticos (*thresholds*) para fins demonstrativos.

---

### 9. Próximos Passos do Projeto

O planejamento da evolução do projeto prevê a implementação dos seguintes módulos nas próximas sprints:

1. **Processamento Assíncrono / Tarefas em Segundo Plano**: Integração de filas para processamento de imagens de alta resolução sem bloquear a thread principal da API.
2. **Persistência de Dados (SQLite + SQLAlchemy)**: Criação de banco de dados para histórico de análises efetuadas.
3. **Containerização com Docker**: Empacotamento do backend FastAPI, do frontend React e do banco em contêineres Docker usando `docker-compose`.
4. **Evolução do Frontend Principal**: Expansão do painel técnico para incluir histórico de análises, filtros e dashboards comparativos.
5. **Ampliação de Testes**: Expansão da suíte de testes automatizados no backend (`pytest`) e testes de componentes no frontend.
