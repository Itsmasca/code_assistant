from pydantic import BaseModel, Field
from sqlalchemy import Column, String, Text, ForeignKey
from src.api.core.database.db_models import Base
import uuid
from sqlalchemy.dialects.postgresql import UUID

class MessageCreate(BaseModel):
    chat_id: uuid.UUID
    sender: str
    text: str

class MessagePublic(BaseModel):
    messageId: uuid.UUID = Field(..., alias="message_id")
    chatId: uuid.UUID = Field(..., alias="chat_id")
    sender: str
    text: str

    model_config = {
        "from_attributes": True,
        "populate_by_name": True, 
    }

class Message(Base):
    __tablename__ = "messages"
    message_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    chat_id = Column(UUID(as_uuid=True), ForeignKey("chats.chat_id", ondelete="CASCADE"), nullable=False)
    sender = Column(Text, nullable=False)
    text = Column(Text, nullable=False)


