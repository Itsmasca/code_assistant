from src.api.modules.files.files_models import File, FileCreate
from src.api.core.repository.base_repository import BaseRepository
import logging
from src.api.core.logs.logger import Logger
from typing import Dict, Any, List
from sqlalchemy.orm import Session
from uuid import UUID
from src.api.core.decorators.service_error_handler import service_error_handler

class FilesService():
    _MODULE = "files.service"
    def __init__(self, logger: Logger, repository: BaseRepository):
        self._repository: BaseRepository = repository
        self._logger = logger

    @service_error_handler(module=_MODULE)
    def create(self, db: Session,  file: FileCreate) -> File:
        return self._repository.create(db=db, data=File(**file.model_dump()))

    @service_error_handler(module=_MODULE)
    def resource(self, db: Session, file_id: UUID) -> File | None:
        result = self._repository.get_one(db=db, key="file_id", value=file_id)
        if result is None:
            return None
        return result
    
    @service_error_handler(module=_MODULE)
    def collection(self, db: Session, agent_id: UUID) -> List[File]:
        result = self._repository.get_many(db=db, key="user_id", value=agent_id)

        if len(result) != 0:
            return result
        return []
    
    @service_error_handler(module=_MODULE)
    def update(self, db: Session, file_id: UUID, changes: Dict[str, Any]) -> File:
        return self._repository.update(db=db, key="agent_id", value=file_id, changes=changes)

    @service_error_handler(module=_MODULE)
    def delete(self, db: Session, file_id: UUID)-> File:
        return self._repository.delete(db=db, key="file_id", value=file_id)
    
    
