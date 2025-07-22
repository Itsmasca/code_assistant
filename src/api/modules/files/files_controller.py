from  src.api.modules.files.files_service import FilesService
from  src.api.modules.files.files_models import File
from src.api.modules.users.users_models import User
from src.api.modules.agents.agents_models import Agent
from src.api.core.services.http_service import HttpService
from fastapi import Request, HTTPException, params
from fastapi.responses import JSONResponse
from src.api.core.services.http_service import HttpService
import logging
from sqlalchemy.orm import Session
import uuid

class FilesController:
    def __init__(self, http_service: HttpService, files_service: FilesService):
        self._http_service = http_service
        self._files_service= files_service
    
    def resource_request(self, request: Request, db: Session, file_id: uuid.UUID):
        user: User = request.state.user

        data: File = self._http_service.request_validation_service.verify_resource(
            "files_service",
            {"db": db, "file_id": file_id},
            "File not found"
        )

        self._http_service.request_validation_service.validate_action_authorization(user.user_id, data.user_id)

        return self.__to_public(data)
    
    def collection_request(self, request: Request, db: Session, agent_id: uuid.UUID):
        user: User = request.state.user

        agent_resource: Agent = self._http_service.request_validation_service.verify_resource(
            "agents_service",
            {"db": db, "agent_id": agent_id},
            "Agent not found"
        )

        self._http_service.request_validation_service.validate_action_authorization(user.user_id, agent_resource.user_id)
        
        data = self._files_service.collection(agent_id=agent_id)

        return [self.__to_public(file) for file in data]

    @staticmethod
    def __to_public(file: File) -> File:
        return File.model_validate(file)