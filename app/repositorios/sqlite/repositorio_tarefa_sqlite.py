from datetime import datetime, timezone
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.banco.modelos_sqlalchemy import ModeloAnaliseImagem, ModeloTarefa
from app.dominio.entidades.resultado_analise_imagem import (
    ResultadoAnaliseImagem,
)
from app.dominio.entidades.tarefa import Tarefa
from app.dominio.enumeracoes import StatusTarefa
from app.dominio.protocolos import ProtocoloRepositorioTarefa


class RepositorioTarefaSQLite(ProtocoloRepositorioTarefa):
    """Persiste tarefas e resultados SQLite, convertendo-os para o dominio."""

    def __init__(self, sessao: Session) -> None:
        self._sessao = sessao

    def salvar(self, tarefa: Tarefa) -> Tarefa:
        modelo_tarefa = self._buscar_modelo_por_id(
            self._sessao,
            tarefa.tarefa_id,
        )

        if modelo_tarefa is None:
            modelo_tarefa = self._criar_modelo_tarefa(tarefa)
            self._sessao.add(modelo_tarefa)
        else:
            self._atualizar_modelo_tarefa(modelo_tarefa, tarefa)

        self._sincronizar_resultado(modelo_tarefa, tarefa)
        self._sessao.commit()
        self._sessao.refresh(modelo_tarefa)
        return self._converter_para_entidade(modelo_tarefa)

    def buscar_por_id(self, tarefa_id: UUID) -> Tarefa | None:
        modelo_tarefa = self._buscar_modelo_por_id(self._sessao, tarefa_id)
        if modelo_tarefa is None:
            return None
        return self._converter_para_entidade(modelo_tarefa)

    def listar_todas(self) -> list[Tarefa]:
        consulta = (
            select(ModeloTarefa)
            .options(selectinload(ModeloTarefa.analise_imagem))
            .order_by(ModeloTarefa.criado_em)
        )

        modelos_tarefa = self._sessao.scalars(consulta).all()
        return [
            self._converter_para_entidade(modelo_tarefa)
            for modelo_tarefa in modelos_tarefa
        ]

    @staticmethod
    def _buscar_modelo_por_id(
        sessao: Session,
        tarefa_id: UUID,
    ) -> ModeloTarefa | None:
        consulta = (
            select(ModeloTarefa)
            .options(selectinload(ModeloTarefa.analise_imagem))
            .where(ModeloTarefa.tarefa_id == tarefa_id)
        )
        return sessao.scalar(consulta)

    @staticmethod
    def _criar_modelo_tarefa(tarefa: Tarefa) -> ModeloTarefa:
        return ModeloTarefa(
            tarefa_id=tarefa.tarefa_id,
            titulo=tarefa.titulo,
            descricao=tarefa.descricao,
            responsavel=tarefa.responsavel,
            status=tarefa.status.value,
            criado_em=tarefa.criado_em,
            atualizado_em=tarefa.atualizado_em,
        )

    @staticmethod
    def _atualizar_modelo_tarefa(
        modelo_tarefa: ModeloTarefa,
        tarefa: Tarefa,
    ) -> None:
        modelo_tarefa.titulo = tarefa.titulo
        modelo_tarefa.descricao = tarefa.descricao
        modelo_tarefa.responsavel = tarefa.responsavel
        modelo_tarefa.status = tarefa.status.value
        modelo_tarefa.criado_em = tarefa.criado_em
        modelo_tarefa.atualizado_em = tarefa.atualizado_em

    @staticmethod
    def _sincronizar_resultado(
        modelo_tarefa: ModeloTarefa,
        tarefa: Tarefa,
    ) -> None:
        resultado = tarefa.resultado_analise

        if resultado is None:
            modelo_tarefa.analise_imagem = None
            return

        if modelo_tarefa.analise_imagem is None:
            modelo_tarefa.analise_imagem = ModeloAnaliseImagem(
                tarefa_id=tarefa.tarefa_id,
                nome_arquivo=resultado.nome_arquivo,
                largura=resultado.largura,
                altura=resultado.altura,
                formato=resultado.formato,
                modo_cor=resultado.modo_cor,
                brilho_medio=resultado.brilho_medio,
                contraste_medio=resultado.contraste_medio,
                classificacao_brilho=resultado.classificacao_brilho,
                classificacao_contraste=resultado.classificacao_contraste,
                quantidade_bordas=resultado.quantidade_bordas,
                tags_automaticas=list(resultado.tags_automaticas),
                criado_em=resultado.criado_em,
            )
            return

        modelo_resultado = modelo_tarefa.analise_imagem
        modelo_resultado.nome_arquivo = resultado.nome_arquivo
        modelo_resultado.largura = resultado.largura
        modelo_resultado.altura = resultado.altura
        modelo_resultado.formato = resultado.formato
        modelo_resultado.modo_cor = resultado.modo_cor
        modelo_resultado.brilho_medio = resultado.brilho_medio
        modelo_resultado.contraste_medio = resultado.contraste_medio
        modelo_resultado.classificacao_brilho = resultado.classificacao_brilho
        modelo_resultado.classificacao_contraste = (
            resultado.classificacao_contraste
        )
        modelo_resultado.quantidade_bordas = resultado.quantidade_bordas
        modelo_resultado.tags_automaticas = list(resultado.tags_automaticas)
        modelo_resultado.criado_em = resultado.criado_em

    @staticmethod
    def _converter_para_entidade(modelo_tarefa: ModeloTarefa) -> Tarefa:
        tarefa = Tarefa(
            tarefa_id=modelo_tarefa.tarefa_id,
            titulo=modelo_tarefa.titulo,
            descricao=modelo_tarefa.descricao,
            responsavel=modelo_tarefa.responsavel,
            criado_em=RepositorioTarefaSQLite._em_utc(modelo_tarefa.criado_em),
            atualizado_em=RepositorioTarefaSQLite._em_utc(
                modelo_tarefa.atualizado_em
            ),
        )
        tarefa.status = StatusTarefa(modelo_tarefa.status)

        if modelo_tarefa.analise_imagem is not None:
            tarefa.resultado_analise = (
                RepositorioTarefaSQLite._converter_resultado_para_entidade(
                    modelo_tarefa.analise_imagem
                )
            )

        return tarefa

    @staticmethod
    def _converter_resultado_para_entidade(
        modelo_resultado: ModeloAnaliseImagem,
    ) -> ResultadoAnaliseImagem:
        return ResultadoAnaliseImagem(
            nome_arquivo=modelo_resultado.nome_arquivo,
            largura=modelo_resultado.largura,
            altura=modelo_resultado.altura,
            formato=modelo_resultado.formato,
            modo_cor=modelo_resultado.modo_cor,
            brilho_medio=modelo_resultado.brilho_medio,
            contraste_medio=modelo_resultado.contraste_medio,
            classificacao_brilho=modelo_resultado.classificacao_brilho,
            classificacao_contraste=modelo_resultado.classificacao_contraste,
            quantidade_bordas=modelo_resultado.quantidade_bordas,
            tags_automaticas=tuple(modelo_resultado.tags_automaticas),
            criado_em=RepositorioTarefaSQLite._em_utc(
                modelo_resultado.criado_em
            ),
        )

    @staticmethod
    def _em_utc(data: datetime) -> datetime:
        if data.tzinfo is None:
            return data.replace(tzinfo=timezone.utc)
        return data.astimezone(timezone.utc)
