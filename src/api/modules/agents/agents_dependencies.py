from sqlalchemy.orm import Session
from src.api.core.dependencies.container import Container
from src.api.core.repository.base_repository import BaseRepository
from src.api.core.logs.logger import Logger
from src.api.core.services.http_service import HttpService
from src.api.modules.agents.agents_controller import AgentsController
from src.api.modules.agents.agents_service import AgentsService
from src.api.modules.agents.agents_models import Agent

def configure_agents_dependencies(logger: Logger):
    
    controller = AgentsController()
    Container.register("agents_controller", controller)