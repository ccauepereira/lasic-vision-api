import os

from fastapi import FastAPI, Request
from fastapi.openapi.utils import get_openapi
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.rotas import saude, tarefas
from app.banco.conexao import criar_tabelas
from app.dominio.excecoes import (
    ErroImagemInvalida,
    ErroRegraNegocio,
    ErroTarefaNaoEncontrada,
)

app = FastAPI(
    title="LASIC VISION API",
    version="0.1.0",
    description="API para gerenciamento de tarefas e analises de imagens.",
    openapi_tags=[
        {
            "name": "Saude",
            "description": "Verificacao de disponibilidade da API.",
        },
        {
            "name": "Tarefas",
            "description": "Ciclo de vida das tarefas de analise de imagem.",
        },
    ],
)

origens_cors = [
    "http://127.0.0.1:5173",
    "http://localhost:5173",
]

origem_frontend = os.getenv("LASIC_VISION_ORIGEM_FRONTEND")
if origem_frontend:
    origens_cors.append(origem_frontend)

# O CORS (Cross-Origin Resource Sharing) e uma mecanica de seguranca dos navegadores 
# que bloqueia requisicoes HTTP assincronas (fetch/XHR) entre origens/portas diferentes.
# Adicionamos o middleware liberando estritamente a porta de dev do React (:5173).
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(saude.router)
app.include_router(tarefas.router)


def _resposta_erro(status_code: int, mensagem: str) -> JSONResponse:
    return JSONResponse(status_code=status_code, content={"detail": mensagem})


@app.exception_handler(ErroImagemInvalida)
def tratar_erro_imagem_invalida(
    request: Request,
    erro: ErroImagemInvalida,
) -> JSONResponse:
    return _resposta_erro(400, str(erro))


@app.exception_handler(ErroTarefaNaoEncontrada)
def tratar_erro_tarefa_nao_encontrada(
    request: Request,
    erro: ErroTarefaNaoEncontrada,
) -> JSONResponse:
    return _resposta_erro(404, str(erro))


@app.exception_handler(ErroRegraNegocio)
def tratar_erro_regra_negocio(
    request: Request,
    erro: ErroRegraNegocio,
) -> JSONResponse:
    return _resposta_erro(409, str(erro))


def criar_openapi_em_portugues() -> dict:
    if app.openapi_schema:
        return app.openapi_schema

    esquema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
        tags=app.openapi_tags,
    )
    for operacoes in esquema["paths"].values():
        for operacao in operacoes.values():
            for resposta in operacao.get("responses", {}).values():
                if resposta.get("description") == "Successful Response":
                    resposta["description"] = "Resposta bem-sucedida."
                if resposta.get("description") == "Validation Error":
                    resposta["description"] = "Erro de validacao."

    componentes = esquema.get("components", {}).get("schemas", {})
    if "HTTPValidationError" in componentes:
        componentes["HTTPValidationError"]["title"] = "Erro de validacao HTTP"
    if "ValidationError" in componentes:
        componentes["ValidationError"]["title"] = "Detalhe do erro de validacao"

    app.openapi_schema = esquema
    return app.openapi_schema


app.openapi = criar_openapi_em_portugues


@app.on_event("startup")
def inicializar_banco() -> None:
    """Cria as tabelas locais antes de a aplicacao aceitar requisicoes."""
    criar_tabelas()
