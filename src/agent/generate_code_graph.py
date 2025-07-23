from pydantic import BaseModel
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END
from langchain_anthropic import ChatAnthropic
from src.agent.prompt_templates import PromptService
from src.api.core.dependencies.container import Container

class GenerateCodeState(BaseModel):
    input: str
    generated_code: str
    final_code: str


# generate code 

async def generate_code(state: GenerateCodeState, llm: ChatAnthropic):

    prompt_service: PromptService = Container.resolve("prompt_service")

    prompt = prompt_service.code_generation_prompt(state=state)

    chain = llm | prompt

    response = await chain.ainvoke({"input": state["input"]})

    state["generated_code"] = response.content.strip().lower()

    return state

# revise code 
async def revise_code(state: GenerateCodeState, llm: ChatAnthropic):
    prompt_service: PromptService = Container.resolve("prompt_service")

    prompt = prompt_service.code_revision_prompt(state=state)

    chain = llm | prompt

    response = await chain.ainvoke({"code": state["generated_code"]})

    state["final_code"] = response.content.strip().lower()

    return state



def create_graph(llm: ChatAnthropic):
    graph = StateGraph(GenerateCodeState)

    async def generate_code_node(state):
        return await generate_code(state=state, llm=llm, )
    
    async def revise_code_node(state):
        return await revise_code(state=state, llm=llm)

    graph.add_node("generate_code", generate_code_node)
    graph.add_node("revise_code", revise_code_node)
    graph.set_entry_point("generate")

    graph.add_edge("revise_code", END)

    return graph.compile()