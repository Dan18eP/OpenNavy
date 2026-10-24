from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.database import init_db
from app.api.v1.api import api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Inicializar tablas de Base de Datos al arrancar
    init_db()
    yield


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Sistema de análisis y revisión de código multi-lenguaje con rúbrica RAG y documentación viva.",
    lifespan=lifespan,
)

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Montar rutas de API v1
app.include_router(api_router, prefix=settings.API_V1_STR)


@app.get("/", summary="Root Index")
def root():
    return {
        "message": f"Bienvenido a {settings.PROJECT_NAME}",
        "docs_url": "/docs",
        "api_v1": settings.API_V1_STR,
        "health_check": f"{settings.API_V1_STR}/health",
    }
