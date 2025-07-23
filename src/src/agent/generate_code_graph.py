from pydantic import BaseModel
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END
from langchain_anthropic import ChatAnthropic
from src.agent.prompt_templates import PromptService
from src.api.core.dependencies.container import Container

class GenerateCodeState(BaseModel):
    input: str
    generated_code: str
    revised_code: str
    final_code: str


# generate code 

async def generate_code(state: GenerateCodeState, llm: ChatAnthropic):

    prompt: PromptService = Container.resolve("prompt_service")


def create_graph(llm: ChatAnthropic):
    graph = StateGraph(GenerateCodeState)


    graph.set_entry_point("classify_intent")

    return graph.compile()