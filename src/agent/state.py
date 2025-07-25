from typing import List
from typing_extensions import TypedDict
from src.api.modules.chats.messages.messages_models import Message
import uuid


class GraphState(TypedDict):
    error: str
    messages: List
    generation: str
    iterations: int
    input:str
    agentName: str
    improvedPrompt: str
    agentJson: str 


class GenerateCodeState(TypedDict):
    input: str
    chat_history: List[Message]
    generated_code: str
    final_code: str
