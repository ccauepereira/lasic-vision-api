from fastapi import APIRouter

router = APIRouter(tags=["Saude"])


@router.get(
    "/health",
    summary="Verifica a saude da API",
    description="Informa se a LASIC Vision API esta disponivel.",
    response_description="Estado atual da API.",
)
def verificar_saude() -> dict[str, str]:
    return {
        "status": "ok",
        "projeto": "LASIC Vision API",
        "versao": "0.1.0",
    }
