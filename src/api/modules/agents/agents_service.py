from src.api.modules.agents.agents_models import Agent, AgentCreate, AgentPublic, AgentToDB, AgentUpdate
from src.api.core.repository.base_repository import BaseRepository
import logging
from src.api.core.logs.logger import Logger
from typing import Dict, Any, List
from sqlalchemy.orm import Session
from uuid import UUID
from src.api.core.decorators.service_error_handler import service_error_handler

class AgentsService():
    _MODULE = "agents.service"
    def __init__(self, logger: Logger, repository: BaseRepository):
        self._repository: BaseRepository = repository
        self._logger = logger

    @service_error_handler(module=_MODULE)
    def create(self, db: Session,  agent: AgentToDB) -> AgentPublic:
        return self.__map_from_db(self._repository.create(db=db, data=self.__map_to_db(AgentToDB(**agent))))

    @service_error_handler(module=_MODULE)
    def resource(self, db: Session, agent_id: UUID) -> AgentPublic | None:
        result = self._repository.get_one(db=db, key="agent_id", value=agent_id)
        if result is None:
            return None
        return self.__map_from_db(result)
    
    @service_error_handler(module=_MODULE)
    def collection(self, db: Session, user_id: UUID) -> List[AgentPublic]:
        result = self._repository.get_many(db=db, key="user_id", value=user_id)

        if len(result) != 0:
            return [self.__map_from_db(agent).model_dump() for agent in result]
        return []
    
    @service_error_handler(module=_MODULE)
    def update(self, db: Session, agent_id: UUID, changes: Dict[str, Any]) -> AgentPublic:
        return self.__map_from_db(self._repository.update(db=db, key="agent_id", value=agent_id, changes=changes))

    @service_error_handler(module=_MODULE)
    def delete(self, db: Session, agent_id: UUID)-> AgentPublic:
        return self.__map_from_db(self._repository.delete(db=db, key="agent_id", value=agent_id))
    
    @staticmethod
    def __map_to_db(agent: AgentToDB) -> Agent:
        return Agent.model_validate(agent)

    @staticmethod
    def __map_from_db(agent: Agent) -> AgentPublic:
        return AgentPublic.model_validate(agent)
