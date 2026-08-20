import pytest
from uuid import uuid4
import cv2
import numpy as np

def criar_imagem_valida_bytes() -> bytes:
    # Cria uma imagem 10x10 preta
    imagem = np.zeros((10, 10, 3), dtype=np.uint8)
    _, buffer = cv2.imencode('.png', imagem)
    return buffer.tobytes()

def test_get_health_retorna_200(cliente):
    resposta = cliente.get("/health")
    assert resposta.status_code == 200


def test_post_tarefas_cria_tarefa_com_201(cliente):
    resposta = cliente.post("/tarefas", json={"titulo": "Nova Tarefa", "descricao": "Desc"})
    assert resposta.status_code == 201
    dados = resposta.json()
    assert dados["titulo"] == "Nova Tarefa"
    assert dados["status"] == "pendente"


def test_fluxo_completo_de_tarefa_funciona(cliente):
    # 1. Cria a tarefa
    resposta_criacao = cliente.post("/tarefas", json={"titulo": "Tarefa Fluxo Completo"})
    assert resposta_criacao.status_code == 201
    tarefa_id = resposta_criacao.json()["tarefa_id"]

    # 2. Atribui responsavel
    resposta_responsavel = cliente.patch(f"/tarefas/{tarefa_id}/responsavel", json={"responsavel": "Manoel"})
    assert resposta_responsavel.status_code == 200
    assert resposta_responsavel.json()["responsavel"] == "Manoel"

    # 3. Inicia
    resposta_inicia = cliente.post(f"/tarefas/{tarefa_id}/iniciar")
    assert resposta_inicia.status_code == 200
    assert resposta_inicia.json()["status"] == "em_andamento"

    # 4. Envia imagem valida
    imagem_bytes = criar_imagem_valida_bytes()
    arquivos = {"arquivo": ("teste.png", imagem_bytes, "image/png")}
    resposta_analise = cliente.post(f"/tarefas/{tarefa_id}/analises/imagem", files=arquivos)
    assert resposta_analise.status_code == 200
    assert resposta_analise.json()["formato"] == "PNG"

    # 5. Conclui
    resposta_conclui = cliente.post(f"/tarefas/{tarefa_id}/concluir")
    assert resposta_conclui.status_code == 200
    assert resposta_conclui.json()["status"] == "concluida"


def test_iniciar_sem_responsavel_retorna_409(cliente):
    resposta_criacao = cliente.post("/tarefas", json={"titulo": "Tarefa Sem Responsavel"})
    tarefa_id = resposta_criacao.json()["tarefa_id"]

    resposta_inicia = cliente.post(f"/tarefas/{tarefa_id}/iniciar")
    assert resposta_inicia.status_code == 409
    assert "responsavel antes de ser iniciada" in resposta_inicia.json()["detail"]


def test_buscar_tarefa_inexistente_retorna_404(cliente):
    id_falso = str(uuid4())
    resposta = cliente.get(f"/tarefas/{id_falso}")
    assert resposta.status_code == 404
    assert "nao encontrada" in resposta.json()["detail"]


def test_imagem_com_extensao_invalida_retorna_400(cliente):
    resposta_criacao = cliente.post("/tarefas", json={"titulo": "Tarefa Imagem Invalida"})
    tarefa_id = resposta_criacao.json()["tarefa_id"]
    
    cliente.patch(f"/tarefas/{tarefa_id}/responsavel", json={"responsavel": "Manoel"})
    cliente.post(f"/tarefas/{tarefa_id}/iniciar")

    # Arquivo com extensao txt
    arquivos = {"arquivo": ("documento.txt", b"conteudo de texto", "text/plain")}
    resposta = cliente.post(f"/tarefas/{tarefa_id}/analises/imagem", files=arquivos)
    assert resposta.status_code == 400
    assert "Formato invalido" in resposta.json()["detail"]
