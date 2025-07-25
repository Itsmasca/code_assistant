from src.api.core.services.webtoken_service import WebTokenService
from src.api.core.middleware.middleware_service import MiddlewareService
from src.api.core.dependencies.container import Container
from src.api.core.services.encryption_service import EncryptionService
from src.api.core.logs.logger import Logger
from src.api.core.services.hashing_service import HashingService
from src.api.core.services.request_validation_service import RequestValidationService
from src.api.core.services.http_service import HttpService
from src.api.modules.users.users_dependencies import configure_users_dependencies
from src.api.modules.agents.agents_dependencies import configure_agents_dependencies

def configure_container():
    # core   
    encryption_service = EncryptionService()
    Container.register("encryption_service", encryption_service)

    logger = Logger()
    Container.register("logger", logger)

    hashing_service = HashingService()
    Container.register("hashing_service", hashing_service)

    request_validatation_service = RequestValidationService()
    Container.register("request_validation_service", request_validatation_service)

    webtoken_service = WebTokenService()
    Container.register("webtoken_service", webtoken_service)

    http_service = HttpService(
        encryption_service=encryption_service,
        logger=logger,
        hashing_service = hashing_service,
        request_validation_service=request_validatation_service,
        webtoken_service=webtoken_service
    )
    Container.register("http_service", http_service)

    middleware_service = MiddlewareService(
        http_service=http_service
    )
    Container.register("middleware_service", middleware_service)

    # users 
    configure_users_dependencies(logger=logger)

    # agents 
    configure_agents_dependencies(logger=logger)






    





