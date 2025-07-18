from sqlalchemy.orm import Session
from api.core.dependencies.container import Container
from api.core.repository.base_repository import BaseRepository
from api.core.logs.logger import Logger
from api.core.services.http_service import HttpService
from api.modules.agents.agents_controller import AgentsController
from api.modules.agents.agents_service import AgentsService
from api.modules.agents.agents_models import Agent
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