from src.api.core.dependencies.container import Container
from src.api.modules.chats.chats_service import ChatsService
from src.api.modules.chats.chats_controller import ChatsController
from src.api.modules.chats.chats_models import Chat
from src.api.core.repository.base_repository import BaseRepository
from src.api.core.services.http_service import HttpService
from src.api.core.logs.logger import Logger

def configure_chats_dependencies(logger: Logger, http_service: HttpService):
    repository = BaseRepository(Chat)
    service = ChatsService(logger=logger, repository=repository)
    controller = ChatsController(https_service=http_service, chats_service=service)

    Container.register("chats_service", service)
    Container.register("chats_controller", controller)