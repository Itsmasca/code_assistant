from fastapi import APIRouter, BackgroundTasks, Depends, Body, Request, HTTPException
from src.api.core.dependencies.container import Container
from typing import List
from src.api.core.middleware.auth_middleware import auth_middleware
from sqlalchemy.orm import Session
from src.api.core.database.sessions import get_db_session
from src.api.modules.agents.agents_models import AgentCreate, AgentUpdate, AgentPublic, GenerateCode
from src.api.modules.agents.agents_controller import AgentsController
from src.api.core.services.http_service import HttpService
import uuid
from src.api.core.middleware.middleware_service import security

router = APIRouter(
    prefix="/agents",
    tags=["Agent"],
    dependencies=[Depends(security)] 
)

def get_controller():
    return Container.resolve("agents_controller")

@router.post("/secure/generate-code/{agent_id}", status_code=200)
def generate_code(
    request: Request, 
    _=Depends(auth_middleware), 
    db: Session = Depends(get_db_session),
    data: GenerateCode = Body(...)
):
    from src.agent.agent import app as agent_graph  # <-- Importa aquí, dentro de la función
    
    # http_service: HttpService = Container.resolve("http_service")
    # agent_resource: AgentPublic =  http_service.request_validation_service.verify_resource(
    #         "agents_service",
    #         {"db": db, "agent_id": agent_id},
    #         "Agent not found"
    #     )
    
    initial_state = {
        "messages": [],
        "iterations": 0,
        "error": "no",
        "agentName": "Reflexagent",
        "improvedPrompt": "Agenty to rreflex a few thoughs by providing two thoughs",
        "agentJson": """
        {
        // ...tu JSON completo aquí (sin cambios)...
        "openapi": "3.0.3",
        "info": {
          "version": "1.6.85",
          "title": "ConfigRouteAnalyzer",
          "description": "NeuralSeek - The business LLM accelerator",
          "license": {
            "name": "End User License Agreement",
            "url": "https://neuralseek.com/eula"
          },
          "contact": {
            "name": "NeuralSeek Support",
            "url": "https://neuralseek.com",
            "email": "support@NeuralSeek.com"
          },
          "termsOfService": "https://neuralseek.com/eula"
        },
        // ...resto del JSON...
        // (no lo repito aquí por espacio, pero no cambies nada más)
      }
""",
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
    