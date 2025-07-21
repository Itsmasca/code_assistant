from pydantic import BaseModel
from typing import List, Any, Optional
from sqlalchemy import Column, String, Text, ForeignKey, Integer, Float
from sqlalchemy.orm import relationship
from src.api.core.database.db_models import Base
import uuid
from sqlalchemy.dialects.postgresql import UUID, JSON


class InteractionRequest(BaseModel):
    conversationiId: str

class LLMConfig(BaseModel):
    prompt: str;
    tools: List[Any];
    max_tokens: int;
    temperature: float

class AgentCreate(BaseModel):
    agentName: str
    agentDescription: Optional[str]

class AgentPublic(BaseModel):
    agentId: str
    userId: str
    agentName: str
    agentDescription: Optional[str]

class AgentUpdate(BaseModel):
    agentName: Optional[str]
    agentDescription: Optional[str]

class AgentPrivate(BaseModel):
    user_id: str
    agentName: str
    agentDescription: Optional[str]


class Agent(Base):
    __tablename__ = "agents"
    agent_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)
    agent_name = Column(Text, nullable=False)
    agent_prompt = Column(Text, nullable=True)
    agent_json = Column(JSON, nullable=True)
