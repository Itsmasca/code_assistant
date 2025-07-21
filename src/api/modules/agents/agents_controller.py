from src.api.core.services.http_service import HttpService
from src.api.modules.agents.agents_service import AgentsService
from src.api.modules.agents.agents_models import AgentPublic, AgentCreate, AgentUpdate
from fastapi import BackgroundTasks, Depends, Body, Request, HTTPException, params
from fastapi.responses import JSONResponse
from src.api.core.services.http_service import HttpService
import logging
from sqlalchemy.orm import Session
from src.api.modules.users.users_models import User
import uuid

class AgentsController:
    def __init__(self, http_service: HttpService, agents_service: AgentsService):
        self._http_service = http_service
        self._agents_service = agents_service

    def create_request(self, requset: Request, db: Session, data: AgentCreate):
        user: User = requset.state.user

        agent_data = {
            **data.model_dump(),
            "user_id": user.user_id
        }

        self._agents_service.create(db=db, agent=agent_data)

        return {"detail": "Agent created"}
    
    def resource_request(self, request: Request, db: Session, agent_id: uuid.UUID):
        user: User = request.state.user

        agent_resource: AgentPublic =  self._http_service.request_validation_service.verify_resource(
            "agents_service",
            {"db": db, "agent_id": agent_id},
            "Agent not found"
        )

        self._http_service.request_validation_service.validate_action_authorization(user.user_id, agent_resource.userId)

        return agent_resource
    
    def collection_request(self, request: Request, db: Session):
        user: User = request.state.user

        data = self._agents_service.collection(db=db, user_id=user.user_id)

        return  data
    
    def update_request(self, request: Request, db: Session, data: AgentUpdate, agent_id: uuid.UUID):
        user: User = request.state.user

        agent_resource: AgentPublic =  self._http_service.request_validation_service.verify_resource(
            "agents_service",
            {"db": db, "agent_id": agent_id},
            "Agent not found"
        )
        
        self._http_service.request_validation_service.validate_action_authorization(user.user_id, agent_resource.userId)

        self._agents_service.update(db=db, agent_id=agent_resource.agentId, changes=data.model_dump(exclude_unset=True))

        return {"detail": "Agent updated"}
    
    def delete_request(self, request: Request, db: Session, agent_id: uuid.UUID):
        user: User = request.state.user

        agent_resource: AgentPublic =  self._http_service.request_validation_service.verify_resource(
            "agents_service",
            {"db": db, "agent_id": agent_id},
            "Agent not found"
        )

        self._http_service.request_validation_service.validate_action_authorization(user.user_id, agent_resource.userId)

        self._agents_service.delete(db=db, agent_id=agent_resource.agentId)

        return { "detail": "Agent deleted"}
    



        