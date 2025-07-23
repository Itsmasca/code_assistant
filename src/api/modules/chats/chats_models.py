from pydantic import BaseModel, Field
from sqlalchemy import Column, String, Text, ForeignKey
from src.api.core.database.db_models import Base
import uuid
from sqlalchemy.dialects.postgresql import UUID

class ChatCreate(BaseModel):
    user_id: uuid.UUID
    title: str


class ChatPublic(BaseModel):
    chatId: uuid.UUID = Field(..., alias="chat_id")
    userId: uuid.UUID = Field(..., alias="user_id")
    title: str

    model_config = {
        "from_attributes": True,
        "populate_by_name": True, 
    }


class Chat(Base):
    __tablename__ = "chats"
    chat_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)
    title = Column(Text, nullable=True)



