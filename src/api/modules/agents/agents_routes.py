from fastapi import APIRouter, Depends, Body
from src.api.core.dependencies.container import Container
from src.api.core.middleware.auth_middleware import auth_middleware
from src.api.modules.agents.agents_controller import AgentsController
from src.api.core.middleware.middleware_service import security
from src.agent.agent_model import AgentRequest, ReactCodeGenerationRequest 
from src.agent.generate_code_graph import create_graph
from  src.service.Llm_service import Llmservice


router = APIRouter(
    prefix="/agents",
    tags=["Agent"],
    dependencies=[Depends(security)] 
)

def get_controller():
    return Container.resolve("agents_controller")

def  get_graph():
    llm_service: Llmservice = Container.resolve("llm_service")
    llm = llm_service.llm
    return create_graph(llm=llm)

@router.post("/secure/generate-code", status_code=200)
async def generate_code(
    data: AgentRequest = Body(...), 
    _=Depends(auth_middleware), 
    controller: AgentsController = Depends(get_controller)
):
    return await controller.prompted_code_generator(data=data)

@router.post("/secure/react-code", status_code=200)
async def generate_react_code(
    data: ReactCodeGenerationRequest = Body(...),
    controller: AgentsController = Depends(get_controller),
    graph = Depends(get_graph)
):
    return await controller.prompted_react_code_generator(graph=graph, data=data)
    
    

