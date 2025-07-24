from src.api.core.repository.base_repository import BaseRepository
from src.api.modules.chats.messages.messages_models import Message
from sqlalchemy.orm import Session
from typing import List

class MessagesRepository(BaseRepository):
    def __init__(self):
        super().__init__(Message)
    
    def create_many(self, db: Session, messages: List[Message]) -> List[Message]:
        db.add_all(messages)
        db.commit()
        for msg in messages:
            db.refresh(msg)
        return messages