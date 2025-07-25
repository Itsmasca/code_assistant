from src.api.core.services.webtoken_service import WebTokenService
from src.api.core.middleware.middleware_service import MiddlewareService
from src.api.core.dependencies.container import Container
from src.api.core.services.encryption_service import EncryptionService
from src.api.core.services.email_service import EmailService
from src.api.core.logs.logger import Logger
from src.api.core.services.hashing_service import HashingService
from src.api.core.services.request_validation_service import RequestValidationService
from src.api.core.services.http_service import HttpService
from src.api.modules.users.users_dependencies import configure_users_dependencies
from src.api.modules.agents.agents_dependencies import configure_agents_dependencies
from src.api.modules.chats.messages.message_dependencies import configure_messages_dependencies
from src.api.modules.chats.chats_dependencies import configure_chats_dependencies
from src.service.Qdrant import QdrantRetriever
from src.api.core.services.embedding_service import EmbeddingService
from src.agent.prompt_templates import PromptService
from  src.service.Redis_service import RedisService

def configure_container():
    ## Core ##  

    ## independent services ##
    email_service = EmailService()
    Container.register("email_service", email_service)

    embeddings_service = EmbeddingService()
    Container.register("embeddings_service", embeddings_service)

    encryption_service = EncryptionService()
    Container.register("encryption_service", encryption_service)

    logger = Logger()
    Container.register("logger", logger)

    hashing_service = HashingService()
    Container.register("hashing_service", hashing_service)
    
    redis_service = RedisService()
    Container.register("redis_service", redis_service)

    retriever_service = QdrantRetriever()
    Container.register("retriever_service", retriever_service)

    request_validatation_service = RequestValidationService()
    Container.register("request_validation_service", request_validatation_service)

    webtoken_service = WebTokenService()
    Container.register("webtoken_service", webtoken_service)

    ## dependent services ## must configure independent services above this line ##

    # http 
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


    # prompts 
    prompt_templates = PromptService(
        embedding_service=embeddings_service
    )
    Container.register("prompt_templates", prompt_templates)
   
   ## Module ## must configure core dependencies above this line ##
    
    # agents 
    configure_agents_dependencies(
        logger=logger,
        http_service=http_service,
        redis_service=redis_service
    )

    # chats
    configure_chats_dependencies(logger=logger, http_service=http_service)

    # messages
    configure_messages_dependencies(logger=logger, http_service=http_service)

    # users 
    configure_users_dependencies(logger=logger, http_service=http_service)






    





