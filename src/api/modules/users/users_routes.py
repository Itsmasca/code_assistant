from fastapi import APIRouter, Depends, Body, Request
from src.api.core.dependencies.container import Container
from src.api.core.middleware.auth_middleware import auth_middleware
from src.api.core.middleware.verification_middleware import verification_middleware
from src.api.modules.users.users_controller import UsersController
from src.api.modules.users.users_models import UserCreate, UserUpdate, UserLogin, UserPublic, VerifyEmail, VerifyEmailResponse, LoginResponse
from src.api.core.models.http_responses import ResponseWithDetail
from sqlalchemy.orm import Session
from src.api.core.database.sessions import get_db_session
from src.api.core.middleware.middleware_service import security

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

def get_controller() -> UsersController:
    controller: UsersController = Container.resolve("users_controller") 
    return controller

@router.post("/verify-email", status_code=200, response_model=VerifyEmailResponse)
def verify_email(
    request: Request,
    data: VerifyEmail = Body(...),
    db: Session = Depends(get_db_session),
    controller: UsersController = Depends(get_controller)
):
    """
    ## Verify email request

    This endpoint sends a verifcation email.
    The token in the response is needed for a create user request.
    """
    return controller.verify_email(request=request, db=db, email=data.email)

@router.post("/verified/create", status_code=201, response_model=ResponseWithDetail)
def verified_create(
    request: Request,
    _=Depends(verification_middleware),
    data: UserCreate = Body(...),
    db: Session = Depends(get_db_session),
    controller: UsersController = Depends(get_controller)
    
):
    """
    ## Create user request

    This endpoint creates a user in the database.
    A verification token is needed from the verify email request along with the verification code the user recieved in the email.
    """
    return controller.create_request(request=request, db=db, new_user=data)

@router.get("/secure/resource", status_code=200, response_model=UserPublic, dependencies=[Depends(security)])
def secure_resource(
    request: Request,
    _=Depends(auth_middleware),
    db: Session = Depends(get_db_session),
    controller: UsersController = Depends(get_controller)
):
    """
    ## User resource request

    This endpoints gets the current user
    """
    return controller.resource_request(request=request)

@router.put("/secure/update", status_code=200, dependencies=[Depends(security)], response_model=ResponseWithDetail)
def secure_update(
    request: Request,
    data: UserUpdate = Body(...),
    _=Depends(auth_middleware),
    db: Session = Depends(get_db_session),
    controller: UsersController = Depends(get_controller)
):
    """
    ## Update request

    This endpoint updates the current users password.
    """
    return controller.update_request(request=request, db=db, data=data)

@router.delete("/secure/delete", status_code=200, dependencies=[Depends(security)], response_model=ResponseWithDetail)
def secure_delete(
    request: Request,
    _=Depends(auth_middleware),
    db: Session = Depends(get_db_session),
    controller: UsersController = Depends(get_controller)
):
    """
    ## Delete request

    This endpoint deletes the current user.
    """
    return controller.delete_request(request=request, db=db)

@router.post("/login", status_code=200, response_model=LoginResponse)
def login(
    request: Request,
    data: UserLogin = Body(...),
    db: Session = Depends(get_db_session),
    controller: UsersController = Depends(get_controller)
):
    """
    ## Login

    This enpoint gets the auth token necessary for further requests.
    """
    return controller.login(request=request, db=db, data=data)
