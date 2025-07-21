from pydantic import BaseModel, Field
from typing import List, Any, Optional, Dict
from sqlalchemy import Column, String, Text, ForeignKey, Integer, Float
from sqlalchemy.orm import relationship
from src.api.core.database.db_models import Base
import uuid
from sqlalchemy.dialects.postgresql import UUID, JSON


class AgentCreate(BaseModel):
    agentName: str
    agentPrompt: str
    agentJson: Dict

class AgentPublic(BaseModel):
    agentId: str = Field(..., alias="agent_id")
    userId: str = Field(..., alias="user_id")
    agentName: str = Field(..., alias="agent_name")
    agentPrompt: str = Field(..., alias="agent_prompt")
    agentJson: Dict = Field(..., alias="agent_json")

    model_config = {
        "from_attributes": True,
        "populate_by_name": True, 
    }

    
class AgentUpdate(BaseModel):
    agent_name: Optional[str] = Field(None, alias="agentName")
    agent_prompt: Optional[str] = Field(None, alias="agentPrompt")
    agent_json: Optional[str] = Field(None, alias="agentJson")

    class Config:
        validate_by_name = True

class AgentToDB(BaseModel):
    user_id: uuid.UUID
    agentName: str
    agentPrompt: str
    agentJson: Dict


class Agent(Base):
    __tablename__ = "agents"
    agent_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)
    agent_name = Column(Text, nullable=False)
    agent_prompt = Column(Text, nullable=True)
    agent_json = Column(JSON, nullable=True)
