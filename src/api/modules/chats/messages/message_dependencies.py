from src.api.core.dependencies.container import Container
from src.api.core.logs.logger import Logger
from src.api.modules.chats.messages.messages_repository import MessagesRepository
from src.api.modules.chats.messages.messages_service import MessagesService
from src.api.modules.chats.messages.messages_controller import MessagesController
from src.api.core.services.http_service import HttpService

def configure_messages_dependencies(logger: Logger, http_service: HttpService):
    repository = MessagesRepository()
    service = MessagesService(logger=logger, repository=repository)
    controller = MessagesController(https_service=http_service, messages_service=service)

    Container.register("messages_service", service)
    Container.register("messages_controller", controller) 