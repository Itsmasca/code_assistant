from fastapi import APIRouter, BackgroundTasks, Depends, Body, Request
from src.api.core.dependencies.container import Container
from typing import List
from src.api.core.middleware.auth_middleware import auth_middleware
from sqlalchemy.orm import Session
from src.api.core.database.sessions import get_db_session
from src.api.modules.chats.chats_controller import ChatsController
from src.api.modules.chats.chats_models import ChatPublic
from src.api.core.middleware.middleware_service import security
import uuid


router = APIRouter(
    prefix="/chats",
    tags=["Chats"],
    dependencies=[Depends(security)] 
)

def get_controller() -> ChatsController:
    return Container.resolve("chats_controller")

@router.post("/secure/create", status_code=201)
def secure_create(
    request: Request,
    _=Depends(auth_middleware),
    db: Session = Depends(get_db_session),
    controller: ChatsController = Depends(get_controller)
):
    return controller.create_request(request=request, db=db)

@router.get("/secure/collection", status_code=200, response_model=List[ChatPublic])
async def secure_collection( 
    request: Request,
    _=Depends(auth_middleware), 
    db: Session = Depends(get_db_session),
    controller: ChatsController = Depends(get_controller)
):
    return await controller.collection_request(request=request, db=db)


    

