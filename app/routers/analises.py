from fastapi import APIRouter, File, UploadFile

from app.schemas.analise import AnaliseImagemResponse
from app.services.analise_service import AnaliseImagemService

router = APIRouter(prefix="/analises", tags=["Analises"])

analise_service = AnaliseImagemService()


@router.post("/imagem", response_model=AnaliseImagemResponse)
async def analisar_imagem(arquivo: UploadFile = File(...)):
    conteudo = await arquivo.read()

    return analise_service.analisar(
        nome_arquivo=arquivo.filename,
        conteudo=conteudo,
    )