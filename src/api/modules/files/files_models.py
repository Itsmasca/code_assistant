from pydantic import BaseModel, Field
from typing import List, Any, Optional, Dict
from sqlalchemy import Column, String, Text, ForeignKey, Integer, Float, DateTime
from sqlalchemy.orm import relationship
from src.api.core.database.db_models import Base
import uuid
from sqlalchemy.dialects.postgresql import UUID, JSON
from datetime import datetime

class FileUpload(BaseModel):
    file_type: str = Field(..., alias="fileType")
    filename: str

class FileToDB(BaseModel):
    user_id: uuid.UUID
    agent_id: uuid.UUID
    file_type: str = Field(..., alias="fileType")
    filename: str
    file_size: str = Field(..., alias="fileSize")
    



class File(Base):

    __tablename__ = "files"
    file_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id"), nullable=False)
    agent_id = Column(UUID(as_uuid=True), ForeignKey("agents.agent_id"), nullable=True)
    filename = Column(Text, nullable=False)
    file_type = Column(Text, nullable=False)
    file_size = Column(String, nullable=True)
    metadata = Column(JSON, nullable=True) 
    created_at = Column(DateTime, default=datetime.now(datetime.timezone.utc), nullable=False)