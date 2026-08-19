from fastapi import APIRouter

router = APIRouter(tags=["Health"])


@router.get("/health")
def health_check():
    return {
        "status": "ok",
        "projeto": "LASIC Vision API",
        "versao": "0.1.0",
    }