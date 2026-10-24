from fastapi import APIRouter
from app.api.v1.endpoints import (
    health,
    repos,
    analysis,
    metrics,
    architecture,
    chat,
    webhooks,
    explorer,
    assessment,
    sessions,
    sonar,
    course,
)

api_router = APIRouter()

api_router.include_router(health.router, tags=["Health & Diagnostics"])
api_router.include_router(course.router, prefix="/course", tags=["OpenNavy Course Plotter"])
api_router.include_router(sonar.router, prefix="/sonar", tags=["OpenNavy Fleet Sonar"])
api_router.include_router(repos.router, prefix="/repos", tags=["Repositories"])
api_router.include_router(analysis.router, prefix="/repos", tags=["Analysis & Streaming"])
api_router.include_router(metrics.router, prefix="/repos", tags=["Metrics & Findings"])
api_router.include_router(architecture.router, prefix="/repos", tags=["Nautical Chart (Architecture)"])
api_router.include_router(chat.router, prefix="/repos", tags=["Conversational RAG Chat"])
api_router.include_router(explorer.router, prefix="/repos", tags=["DeepCode Explorer (DeepWiki)"])
api_router.include_router(assessment.router, prefix="/assessment", tags=["AI Opportunity Assessment"])
api_router.include_router(sessions.router, prefix="/sessions", tags=["Chat Sessions & Resume"])
api_router.include_router(webhooks.router, prefix="/webhooks", tags=["Git Webhooks & CI/CD"])
