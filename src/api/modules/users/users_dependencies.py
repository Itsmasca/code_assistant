from sqlalchemy.orm import Session
from api.core.dependencies.container import Container
from api.core.repository.base_repository import BaseRepository
from api.core.logs.logger import Logger
from api.modules.users.users_models import User
from api.core.services.http_service import HttpService
from api.modules.users.users_service import UsersService
from api.modules.users.users_controller import UsersController

def configure_users_dependencies(logger: Logger):
    repository = BaseRepository(model=User)
    http_service: HttpService = Container.resolve("http_service")
    service = UsersService(
        logger=logger,
        repository=repository
    )
    controller = UsersController(
        https_service=http_service,
        users_service=service
    )

    Container.register("users_service", service)
    Container.register("users_controller", controller)