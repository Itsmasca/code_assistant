from pydantic import BaseModel, Field
from typing import List, Any, Optional, Dict
from sqlalchemy import Column, String, Text, ForeignKey, Integer, Float, DateTime
from sqlalchemy.orm import relationship
from src.api.core.database.db_models import Base
import uuid
from sqlalchemy.dialects.postgresql import UUID, JSON
from datetime import datetime

class FileCreate(BaseModel):
    filename = str
    file_type = str
    file_size = str
    metadata: Optional[str] = None

class File(Base):

    __tablename__ = "files"
    file_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    filename = Column(Text, nullable=False)
    file_type = Column(Text, nullable=False)
    file_size = Column(String, nullable=True)
    metadata = Column(JSON, nullable=True) 
    created_at = Column(DateTime, default=datetime.now(datetime.timezone.utc), nullable=False)