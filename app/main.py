from fastapi import FastAPI
from app.routers import analises, health

app = FastAPI(
    title="LASIC VISION API",
    version="0.1.0",
    description = "Primeira API com FastAPI com OpenCV"
)

app.include_router(health.router)
app.include_router(analises.router)