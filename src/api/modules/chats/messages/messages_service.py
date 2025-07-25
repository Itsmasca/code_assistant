from src.api.modules.chats.messages.messages_models import Message, MessageCreate
from src.api.modules.chats.messages.messages_repository import MessagesRepository
import logging
from src.api.core.logs.logger import Logger
from typing import Dict, Any, List
from sqlalchemy.orm import Session
from uuid import UUID
from src.api.core.decorators.service_error_handler import service_error_handler
from operator import attrgetter

class MessagesService():
    _MODULE = "messages.service"
    def __init__(self, logger: Logger, repository: MessagesRepository):
        self._repository: MessagesRepository = repository
        self._logger = logger

    @service_error_handler(module=_MODULE)
    def create_many(self, db: Session,  messages: List[MessageCreate]) -> Message:
        return self._repository.create_many(db=db, data=[Message(**message.model_dump(by_alias=False)) for message in messages])

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
            return sorted(result, key=attrgetter("created_at"), reverse=True)
        return []
    
    @service_error_handler(module=_MODULE)
    def update(self, db: Session, message_id: UUID, changes: Dict[str, Any]) -> Message:
        return self._repository.update(db=db, key="message_id", value=message_id, changes=changes)

    @service_error_handler(module=_MODULE)
    def delete(self, db: Session, message_id: UUID)-> Message:
        return self._repository.delete(db=db, key="message_id", value=message_id)
    
    def handle_messages(self, db: Session, chat_id: UUID, human_message: str, ai_message: str): 
        incoming_message = MessageCreate(
            chat_id=chat_id,
            sender="user",
            text=human_message
        )

        outgoing_message = MessageCreate(
            chat_id=chat_id,
            sender="ai",
            text=ai_message
        )

        return self.create_many(db=db, messages=[incoming_message, outgoing_message])
    
    