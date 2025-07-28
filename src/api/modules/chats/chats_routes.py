from fastapi import APIRouter, BackgroundTasks, Depends, Body, Request
from src.api.core.dependencies.container import Container
from typing import List, Dict
from src.api.core.middleware.auth_middleware import auth_middleware
from sqlalchemy.orm import Session
from src.api.core.database.sessions import get_db_session
from src.api.modules.chats.chats_controller import ChatsController
from src.api.modules.chats.chats_models import ChatPublic, ChatCreateResposne, ChatUpdate
from src.api.core.models.http_responses import ResponseWithDetail
from src.api.core.middleware.middleware_service import security
import uuid


router = APIRouter(
    prefix="/chats",
    tags=["Chats"],
    dependencies=[Depends(security)] 
)

def get_controller() -> ChatsController:
    return Container.resolve("chats_controller")

@router.post("/secure/create", status_code=201, response_model=ChatCreateResposne)
def secure_create(
    request: Request,
    _=Depends(auth_middleware),
    db: Session = Depends(get_db_session),
    controller: ChatsController = Depends(get_controller)
):
    """
    ## Chat create request

    This endpoint creates a chat in the database.
    The id returned is needed for all requests to the llm.
    No request body is needed but can be added.

    - **title**: optional string for chat identification.
    - **Resposne**: chatId needed for  llm  interactions.

    """
    return controller.create_request(request=request, db=db)

@router.get("/secure/collection", status_code=200, response_model=List[ChatPublic])
def secure_collection( 
    request: Request,
    _=Depends(auth_middleware), 
    db: Session = Depends(get_db_session),
    controller: ChatsController = Depends(get_controller)
):
    """
    ## Chat collection request

    This endpoint returns a list of chats by the user id in the auth token.
    """
    return controller.collection_request(request=request, db=db)


@router.put("/secure/update/{chat_id}", status_code=200, response_model=ResponseWithDetail)
def secure_update(
    chat_id: uuid.UUID,
    data: ChatUpdate,
    request: Request,
    _=Depends(auth_middleware),
    db: Session = Depends(get_db_session),
    controller: ChatsController = Depends(get_controller)
): 
    """
    ## Update request

    This endpont updates the title of the chat provided in the params
    """
    return controller.update_request(
        request=request,
        db=db,
        data=data,
        chat_id=chat_id
    )
    
