from pydantic import BaseModel
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END
from langchain_anthropic import ChatAnthropic
from src.agent.prompt_templates import PromptService
from src.api.core.dependencies.container import Container
from src.agent.state import GenerateCodeState
import re



# generate code 

async def generate_code(state: GenerateCodeState, llm: ChatAnthropic):
    prompt_service: PromptService = Container.resolve("prompt_templates")

    prompt = await prompt_service.code_generation_prompt(state=state)

    chain = prompt | llm

    response = await chain.ainvoke({"input": state["input"]})

    raw_code = response.content.strip()
    clean_code = clean_escaped_jsx(raw_code)

    state["generated_code"] = clean_code

    return state

# revise code 
async def revise_code(state: GenerateCodeState, llm: ChatAnthropic):
    prompt_service: PromptService = Container.resolve("prompt_templates")

    prompt = await prompt_service.code_revision_prompt()

    chain = prompt | llm

    response = await chain.ainvoke({"code": state["generated_code"]})

    raw_code = response.content.strip()
    
    if raw_code == 'UNCHANGED':
        state["final_code"] = state["generated_code"]
    
    else: 
        clean_code = clean_escaped_jsx(raw_code)

        state["final_code"] = clean_code

    return state

def clean_escaped_jsx(escaped_str: str) -> str:
    match = re.search(r"```(?:jsx|js|tsx)?\n(.*?)```", escaped_str, re.DOTALL)
    jsx_raw = match.group(1) if match else escaped_str

    cleaned = bytes(jsx_raw, "utf-8").decode("unicode_escape")

    return cleaned.strip()

def create_graph(llm: ChatAnthropic):
    graph = StateGraph(GenerateCodeState)

    async def generate_code_node(state):
        return await generate_code(state=state, llm=llm)
    
    async def revise_code_node(state):
        return await revise_code(state=state, llm=llm)

    graph.add_node("generate_code", generate_code_node)
    graph.add_node("revise_code", revise_code_node)
    graph.set_entry_point("generate_code")

    graph.add_edge("generate_code", "revise_code")
    graph.add_edge("revise_code", END)

    return graph.compile()