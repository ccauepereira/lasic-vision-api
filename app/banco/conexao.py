import os
from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker


url_banco = os.getenv("LASIC_VISION_URL_BANCO", "sqlite:///./lasic_vision.db")

motor_banco = create_engine(
    url_banco,
    connect_args={"check_same_thread": False},
)
fabrica_sessoes = sessionmaker(
    bind=motor_banco,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
)


def obter_sessao() -> Generator[Session, None, None]:
    """Fornece uma sessao SQLite e garante seu fechamento."""
    sessao = fabrica_sessoes()
    try:
        yield sessao
    finally:
        sessao.close()


def criar_tabelas() -> None:
    """Cria a estrutura de persistencia definida pelos modelos SQLAlchemy."""
    from app.banco.modelos_sqlalchemy import BaseModelo

    BaseModelo.metadata.create_all(bind=motor_banco)
