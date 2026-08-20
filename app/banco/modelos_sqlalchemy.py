from __future__ import annotations

from datetime import datetime
from uuid import UUID

from sqlalchemy import DateTime, ForeignKey, JSON, String, Uuid
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class BaseModelo(DeclarativeBase):
    """Base compartilhada pelos modelos de persistencia."""


class ModeloTarefa(BaseModelo):
    """Representa a tabela de tarefas sem incorporar regras de negocio."""

    __tablename__ = "tarefas"

    tarefa_id: Mapped[UUID] = mapped_column(Uuid, primary_key=True)
    titulo: Mapped[str] = mapped_column(String(255), nullable=False)
    descricao: Mapped[str | None] = mapped_column(String, nullable=True)
    responsavel: Mapped[str | None] = mapped_column(String(255), nullable=True)
    status: Mapped[str] = mapped_column(String(30), nullable=False)
    criado_em: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )
    atualizado_em: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

    analise_imagem: Mapped[ModeloAnaliseImagem | None] = relationship(
        back_populates="tarefa",
        cascade="all, delete-orphan",
        single_parent=True,
        uselist=False,
    )


class ModeloAnaliseImagem(BaseModelo):
    """Representa somente os dados extraidos de uma imagem analisada."""

    __tablename__ = "analises_imagem"

    analise_id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
    )
    tarefa_id: Mapped[UUID] = mapped_column(
        Uuid,
        ForeignKey("tarefas.tarefa_id"),
        nullable=False,
        unique=True,
    )
    nome_arquivo: Mapped[str] = mapped_column(String(255), nullable=False)
    largura: Mapped[int] = mapped_column(nullable=False)
    altura: Mapped[int] = mapped_column(nullable=False)
    formato: Mapped[str] = mapped_column(String(50), nullable=False)
    modo_cor: Mapped[str] = mapped_column(String(100), nullable=False)
    brilho_medio: Mapped[float] = mapped_column(nullable=False)
    contraste_medio: Mapped[float] = mapped_column(nullable=False)
    classificacao_brilho: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )
    classificacao_contraste: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )
    quantidade_bordas: Mapped[int] = mapped_column(nullable=False)
    tags_automaticas: Mapped[list[str]] = mapped_column(JSON, nullable=False)
    criado_em: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

    tarefa: Mapped[ModeloTarefa] = relationship(
        back_populates="analise_imagem"
    )
