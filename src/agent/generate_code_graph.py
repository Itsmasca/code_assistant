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

    prompt_service: PromptService = Container.resolve("prompt_service")

    prompt = prompt_service.code_generation_prompt()

    chain = llm | prompt

    response = await chain.ainvoke({"input": state["input"]})

    state["response"] = response.content.strip().lower()

    return state

# revise code 
async def revise_code(state: GenerateCodeState, llm: ChatAnthropic):
    prompt_service: PromptService = Container.resolve("prompt_service")

    prompt = prompt_service.code_revision_prompt()

    chain = llm | prompt

    response = await chain.ainvoke({"input": state["input"]})

    state["response"] = response.content.strip().lower()

    return state



def create_graph(llm: ChatAnthropic):
    graph = StateGraph(GenerateCodeState)

    graph.add_node("generate_code", generate_code)
    graph.add_node("revise_code", revise_code)
    graph.set_entry_point("classify_intent")

    return graph.compile()