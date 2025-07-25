from pydantic import BaseModel, Field, ConfigDict
from sqlalchemy import Column, String, Text, ForeignKey
from src.api.core.database.db_models import Base
import uuid
from sqlalchemy.dialects.postgresql import UUID
from typing import Optional
from pydantic.alias_generators import to_camel

class ChatCreate(BaseModel):
    user_id: uuid.UUID

class ChatUpdate(BaseModel):
    title: uuid.UUID

class ChatPublic(BaseModel):
    chat_id: uuid.UUID
    user_id: uuid.UUID
    title: Optional[str] = None

    model_config = ConfigDict(
        populate_by_name=True,
        from_attributes=True,
        serialize_by_alias=True,
        alias_generator=to_camel
    )


class Chat(Base):
    __tablename__ = "chats"
    chat_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)
    title = Column(Text, nullable=True)



