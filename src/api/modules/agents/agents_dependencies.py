from sqlalchemy.orm import Session
from core.dependencies.container import Container
from core.repository.base_repository import BaseRepository
from core.logs.logger import Logger
from core.services.http_service import HttpService
from modules.agents.agents_controller import AgentsController
from modules.agents.agents_service import AgentsService
from modules.agents.agents_models import Agent
def configure_agents_dependencies(logger: Logger):
    repository = BaseRepository(model=Agent)
    http_service: HttpService = Container.resolve("http_service")
    service = AgentsService(
        logger=logger,
        repository=repository
    )
    controller = AgentsController(
        https_service=http_service,
        agents_service= service
    )

    Container.register("agents_service", service)
    Container.register("agents_controller", controller)