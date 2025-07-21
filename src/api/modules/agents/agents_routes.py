from fastapi import APIRouter, BackgroundTasks, Depends, Body, Request
from src.api.core.dependencies.container import Container
from typing import List
from src.api.core.middleware.auth_middleware import auth_middleware
from sqlalchemy.orm import Session
from src.api.core.database.sessions import get_db_session
from src.api.modules.agents.agents_models import AgentCreate, AgentUpdate, AgentPublic
from src.api.modules.agents.agents_controller import AgentsController
import uuid
from src.api.core.middleware.middleware_service import security
<<<<<<< HEAD
from src.agent.agent import app as agent_graph
=======

>>>>>>> c0a151f05385b7daabca88c4297547d1afb98b70

router = APIRouter(
    prefix="/agents",
    tags=["Agent"],
    dependencies=[Depends(security)] 
)

def get_controller():
    return Container.resolve("agents_controller")

@router.post("/generate-code")
def generate_code(request: Request, data: dict = Body(...)):
    from src.agent.agent import app as agent_graph  # <-- Importa aquí, dentro de la función
    initial_state = {
        "messages": [],
        "iterations": 0,
        "error": "no",
        "agentName": data.get("agentName", "DefaultAgent"),
        "improvedPrompt": data.get("improvedPrompt", ""),
        "agentJson": data.get("agentJson", {}),
    }
    result = agent_graph.invoke(initial_state)
    return {
        "code": getattr(result["generation"], "code", ""),
        "imports": getattr(result["generation"], "imports", ""),
        "prefix": getattr(result["generation"], "prefix", ""),
        "messages": result.get("messages", []),
        "agentName": result.get("agentName", ""),
        "improvedPrompt": result.get("improvedPrompt", ""),
        "agentJson": result.get("agentJson", {}),
        "error": result.get("error", "no"),
    }

<<<<<<< HEAD
@router.post("/generate-code")
def generate_code(request: Request, data: dict = Body(...)):
    initial_state = {
        "messages": [],
        "iterations": 0,
        "error": "no",
        "agentName": data.get("agentName", "DefaultAgent"),
        "improvedPrompt": data.get("improvedPrompt", ""),
        "agentJson": data.get("agentJson", {}),
    }
    result = agent_graph.invoke(initial_state)
    # Solo regresa el bloque de código generado y metadatos útiles
    return {
        "code": getattr(result["generation"], "code", ""),
        "imports": getattr(result["generation"], "imports", ""),
        "prefix": getattr(result["generation"], "prefix", ""),
        "messages": result.get("messages", []),
        "agentName": result.get("agentName", ""),
        "improvedPrompt": result.get("improvedPrompt", ""),
        "agentJson": result.get("agentJson", {}),
        "error": result.get("error", "no"),
    }

=======
>>>>>>> c0a151f05385b7daabca88c4297547d1afb98b70
@router.post("/secure/create", status_code=201)
def secure_create(
    requset: Request,
    _=Depends(auth_middleware),
    db: Session = Depends(get_db_session),
    controller: AgentsController = Depends(get_controller),
    data: AgentCreate = Body(...)
):
    return controller.create_request(requset=requset, db=db, data=data)

@router.get("/secure/resource/{agent_id}", status_code=200, response_model=AgentPublic)
def secure_resource(
    agent_id: uuid.UUID,
    request: Request,
    _=Depends(auth_middleware),
    db: Session = Depends(get_db_session),
    controller: AgentsController = Depends(get_controller)
):
    return controller.resource_request(request=request, db=db, agent_id=agent_id)

@router.get("/secure/collection", status_code=200, response_model=List[AgentPublic])
def secure_collection(
    request: Request,
    _=Depends(auth_middleware),
    db: Session = Depends(get_db_session),
    controller: AgentsController = Depends(get_controller)
):
    return controller.collection_request(request=request, db=db)

@router.put("/secure/{agent_id}", status_code=200)
def secure_update(
    agent_id: uuid.UUID,
    request: Request,
    _=Depends(auth_middleware),
    db: Session = Depends(get_db_session),
    controller: AgentsController = Depends(get_controller),
    data: AgentUpdate = Body(...)
):
    return controller.update_request(request=request, db=db, data=data, agent_id=agent_id)

@router.delete("/secure/{agent_id}")
def secure_delete(
    agent_id: uuid.UUID,
    request: Request,
    _=Depends(auth_middleware),
    db: Session = Depends(get_db_session),
    controller: AgentsController = Depends(get_controller)
):
    return controller.delete_request(request=request, db=db, agent_id=agent_id)
    