from src.api.core.logs.logger import Logger
from src.api.core.dependencies.container import Container
from src.api.modules.knowledge_base.knowledge_base_controller import KnowledgeBaseController


def configure_knowledge_base_dependencies():
    http_service = Container.resolve("http_service")
    files_service = Container.resolve("files_service")
    embeddings_service = Container.resolve("ebeddings_service")

    controller = KnowledgeBaseController(
        http_service=http_service,
        files_service=files_service,
        embeddings_service=embeddings_service
    )

    Container.register("knowledge_base_controller", controller)