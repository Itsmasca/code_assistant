from src.api.core.dependencies.container import Container
from src.api.core.logs.logger import Logger
from src.api.modules.agents.agents_controller import AgentsController

def configure_agents_dependencies(logger: Logger):
    
    controller = AgentsController()
    Container.register("agents_controller", controller)