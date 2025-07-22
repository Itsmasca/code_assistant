from fastapi import APIRouter, Body, Request,  Depends, UploadFile, File
from fastapi.responses import JSONResponse
from core.dependencies.container import Container
from  src.api.core.database.sessions import get_db_session
from src.api.modules.knowledge_base.knowledge_base_controller import KnowledgeBaseController
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/knowledge-base",
    tags=["Knowledge Base"]
)

def get_controller() -> KnowledgeBaseController:
    Container.resolve("knowledge_base_controller")

@router.post("/upload", response_class=JSONResponse)
async def add_to_knowledge_base(
    uploaded_file: UploadFile = File(...),
    controller: KnowledgeBaseController = Depends(get_controller),
    db: Session = Depends(get_db_session)
):
    file_bytes = await uploaded_file.read()

    # 3. Extract metadata
    filename = uploaded_file.filename
    file_type = uploaded_file.content_type
    file_size = len(file_bytes)
    return controller.add_to_knowledge_base(
        db=db,

    )