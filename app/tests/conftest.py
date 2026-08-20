import os
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from fastapi.testclient import TestClient

# Define o banco de dados em memoria para os testes
os.environ["LASIC_VISION_URL_BANCO"] = "sqlite:///:memory:"

from app.banco.modelos_sqlalchemy import BaseModelo
import app.banco.conexao as conexao
from app.banco.conexao import obter_sessao
from app.main import app

# Substitui o motor padrao por um que usa StaticPool (obrigatorio para memory db com TestClient)
motor_banco_teste = create_engine(
    "sqlite:///:memory:",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
fabrica_sessoes_teste = sessionmaker(
    bind=motor_banco_teste,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
)

conexao.motor_banco = motor_banco_teste
conexao.fabrica_sessoes = fabrica_sessoes_teste


@pytest.fixture(scope="function", autouse=True)
def configurar_banco():
    """Cria as tabelas em memoria para cada teste e as descarta ao final."""
    BaseModelo.metadata.create_all(bind=motor_banco_teste)
    yield
    BaseModelo.metadata.drop_all(bind=motor_banco_teste)


@pytest.fixture(scope="function")
def sessao():
    """Fornece uma sessao do SQLAlchemy conectada ao banco em memoria."""
    sessao = fabrica_sessoes_teste()
    try:
        yield sessao
    finally:
        sessao.close()


@pytest.fixture(scope="function")
def cliente(sessao):
    """Cliente de teste do FastAPI com injecao da sessao em memoria."""
    def obter_sessao_teste():
        try:
            yield sessao
        finally:
            pass

    app.dependency_overrides[obter_sessao] = obter_sessao_teste
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
