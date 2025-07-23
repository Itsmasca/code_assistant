from src.api.modules.chats.messages.messages_models import Message, MessageCreate
from src.api.core.repository.base_repository import BaseRepository
import logging
from src.api.core.logs.logger import Logger
from typing import Dict, Any, List
from sqlalchemy.orm import Session
from uuid import UUID
from src.api.core.decorators.service_error_handler import service_error_handler

class MessagesService():
    _MODULE = "messages.service"
    def __init__(self, logger: Logger, repository: BaseRepository):
        self._repository: BaseRepository = repository
        self._logger = logger

    @service_error_handler(module=_MODULE)
    def create(self, db: Session,  message: MessageCreate) -> Message:
        return self._repository.create(db=db, data=Message(**message.model_dump(by_alias=False)))

    @service_error_handler(module=_MODULE)
    def resource(self, db: Session, message_id: UUID) -> Message | None:
        result = self._repository.get_one(db=db, key="chat_id", value=message_id)
        if result is None:
            return None
        return result
    
    @service_error_handler(module=_MODULE)
    def collection(self, db: Session, chat_id: UUID) -> List[Message]:
        result = self._repository.get_many(db=db, key="chat_id", value=chat_id)

        if len(result) != 0:
            return result
        return []
    
    @service_error_handler(module=_MODULE)
    def update(self, db: Session, message_id: UUID, changes: Dict[str, Any]) -> Message:
        return self._repository.update(db=db, key="message_id", value=message_id, changes=changes)

    @service_error_handler(module=_MODULE)
    def delete(self, db: Session, message_id: UUID)-> Message:
        return self._repository.delete(db=db, key="message_id", value=message_id)
    
    