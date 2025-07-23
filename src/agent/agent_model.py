from pydantic import BaseModel
from typing import List, Any
from  src.agent.state import GraphState


class LLMConfig(BaseModel):
    prompt: str;
    tools: List[Any];
    max_tokens: int;

class GenerateCode(BaseModel):
    prefix: str
    imports: str
    code: Any

class AgentRequest(BaseModel):
    agentName: str
    improvedPrompt: str
    agentJson: str

class ReactCodeGenerationRequest(BaseModel):
    input: str
