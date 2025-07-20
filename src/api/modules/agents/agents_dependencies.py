from sqlalchemy.orm import Session
from src.api.core.dependencies.container import Container
from src.api.core.repository.base_repository import BaseRepository
from src.api.core.logs.logger import Logger
from src.api.core.services.http_service import HttpService
from src.api.modules.agents.agents_controller import AgentsController
from src.api.modules.agents.agents_service import AgentsService
from src.api.modules.agents.agents_models import Agent
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