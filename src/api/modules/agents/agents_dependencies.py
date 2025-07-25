from src.api.core.dependencies.container import Container
from src.api.core.logs.logger import Logger
from src.api.modules.agents.agents_controller import AgentsController
from src.api.core.services.http_service import HttpService
from src.service.Llm_service import Llmservice

def configure_agents_dependencies(http_service: HttpService, llm_service: Llmservice):
    controller = AgentsController(https_service=http_service, llm_service=llm_service)
    
    Container.register("agents_controller", controller)