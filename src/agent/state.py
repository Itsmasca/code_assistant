from typing import List
from typing_extensions import TypedDict
from  pydantic import BaseModel


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
    generated_code: str
    final_code: str
