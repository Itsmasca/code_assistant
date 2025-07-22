from fastapi import APIRouter, BackgroundTasks, Depends, Body, Request, HTTPException,UploadFile, File
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
from src.agent.agent_model import AgentRequest


router = APIRouter(
    prefix="/agents",
    tags=["Agent"],
    dependencies=[Depends(security)] 
)

def get_controller():
    return Container.resolve("agents_controller")

@router.post("/secure/generate-code", status_code=200)
def generate_code(
    data: AgentRequest = Body(...), 
    _=Depends(auth_middleware),
    controller: AgentsController = Depends(get_controller)
):
    return controller.prompted_code_generator(data=data)

    