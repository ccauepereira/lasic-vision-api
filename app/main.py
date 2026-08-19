from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import analises, health

app = FastAPI(
    title="LASIC VISION API",
    version="0.1.0",
    description = "Primeira API com FastAPI com OpenCV"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(analises.router)