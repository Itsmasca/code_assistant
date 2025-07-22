from src.api.core.dependencies.container import Container
from src.api.core.logs.logger import Logger
from src.api.core.services.http_service import HttpService
from src.api.modules.files.files_controller import FilesController
from src.api.modules.files.files_service import FilesService
from src.api.modules.files.files_models import File
from src.api.core.repository.base_repository import BaseRepository

def configure_files_dependencies(logger: Logger):
    repository = BaseRepository(File)
    http_service = Container.resolve("http_service")
    service = FilesService(logger=logger, repository=repository)
    controller = FilesController(http_service=http_service, files_service=service)