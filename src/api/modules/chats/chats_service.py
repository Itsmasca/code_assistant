from src.api.modules.chats.chats_models import Chat, ChatCreate
from src.api.core.repository.base_repository import BaseRepository
import logging
from src.api.core.logs.logger import Logger
from typing import Dict, Any, List
from sqlalchemy.orm import Session
from uuid import UUID
from src.api.core.decorators.service_error_handler import service_error_handler

class ChatsService():
    _MODULE = "chats.service"
    def __init__(self, logger: Logger, repository: BaseRepository):
        self._repository: BaseRepository = repository
        self._logger = logger

    @service_error_handler(module=_MODULE)
    def create(self, db: Session,  agent: ChatCreate) -> Chat:
        return self._repository.create(db=db, data=Chat(**agent.model_dump(by_alias=False)))

    @service_error_handler(module=_MODULE)
    def resource(self, db: Session, chat_id: UUID) -> Chat | None:
        result = self._repository.get_one(db=db, key="chat_id", value=chat_id)
        if result is None:
            return None
        return result
    
    @service_error_handler(module=_MODULE)
    def collection(self, db: Session, user_id: UUID) -> List[Chat]:
        result = self._repository.get_many(db=db, key="user_id", value=user_id)

        if len(result) != 0:
            return result
        return []
    
    @service_error_handler(module=_MODULE)
    def update(self, db: Session, chat_id: UUID, changes: Dict[str, Any]) -> Chat:
        return self._repository.update(db=db, key="chat_id", value=chat_id, changes=changes)

    @service_error_handler(module=_MODULE)
    def delete(self, db: Session, chat_id: UUID)-> Chat:
        return self._repository.delete(db=db, key="chat_id", value=chat_id)
    
    