# middleware/auth_middleware.py
from fastapi import Request
from api.core.dependencies.container import Container
from api.core.middleware.middleware_service import MiddlewareService


def verification_middleware(request: Request):
    middleware_service: MiddlewareService = Container.resolve("middleware_service")
    verification_code = middleware_service.verify(request)

    request.state.verification_code = verification_code
    return verification_code
  
        