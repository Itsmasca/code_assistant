from src.api.core.services.http_service import HttpService
from src.api.modules.agents.agents_models import Agent
from src.api.modules.users.users_models import User
from src.api.core.services.embedding_service import EmbeddingService
from src.api.modules.files.files_service import FilesService
from src.api.modules.files.files_models import FileCreate
from fastapi import Request, File, UploadFile
from sqlalchemy.orm import Session

class KnowledgeBaseController:
    def __init__(self, http_service: HttpService, files_service: FilesService, embeddings_service: EmbeddingService):
        self._http_service = http_service
        self.files_service = files_service
        self.embeddings_service = embeddings_service

    async def add_to_knowledge_base(self, db: Session, data: UploadFile = File(...)):

        file_bytes = await data.read()
        filename = data.filename
        file_type = data.content_type
        file_size = str(len(file_bytes))
  
        file = self.files_service.create(
            db=db,
            file=FileCreate(
                filename = filename,
                file_type = file_type,
                file_size = file_size
            )
        )

        await self.embeddings_service.embed_uploaded_document(
            file_bytes=file_bytes,
            file_type=file_type,
            filename=data.filename,
            file_id=file.file_id
        )

        return {"detail": "File added to knowledgebase"}
        
