from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import analises, health

app = FastAPI(
    title="LASIC VISION API",
    version="0.1.0",
    description = "Primeira API com FastAPI com OpenCV"
)

# O CORS (Cross-Origin Resource Sharing) e uma mecanica de seguranca dos navegadores 
# que bloqueia requisicoes HTTP assincronas (fetch/XHR) entre origens/portas diferentes.
# Adicionamos o middleware liberando estritamente a porta de dev do React (:5173).
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5173",
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(analises.router)