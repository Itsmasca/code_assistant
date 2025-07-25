from src.api.core.dependencies.container import Container
from src.api.core.logs.logger import Logger
from src.api.modules.agents.agents_controller import AgentsController
from src.api.core.services.http_service import HttpService
from src.service.Llm_service import Llmservice
from  src.service.Redis_service import RedisService

def configure_agents_dependencies(logger: Logger, http_service: HttpService, redis_service: RedisService):
    service = Llmservice(
        logger=logger,
        redis_service=redis_service
    )
    
    controller = AgentsController(https_service=http_service, llm_service=service)
    
    Container.register("llm_service", service)
    Container.register("agents_controller", controller)
    