from fastapi import APIRouter, Body, Request
from fastapi.responses import JSONResponse
from core.dependencies.container import Container
from src.api.core.services.embedding_service import EmbeddingService


router = APIRouter(
    prefix="/api/files",
    tags=["Files"]
)


