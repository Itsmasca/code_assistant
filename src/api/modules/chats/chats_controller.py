from src.api.modules.chats.chats_models import Chat, ChatPublic
from src.api.modules.users.users_models import User
from src.api.modules.chats.chats_service import ChatsService
from src.api.modules.chats.chats_models import  Chat, ChatCreate
from fastapi import Request
from src.api.core.services.http_service import HttpService
from sqlalchemy.orm import Session
import uuid
from src.api.modules.users.users_models import User


class ChatsController:
    def __init__(self, https_service: HttpService, chats_service: ChatsService):
        self._http_service: HttpService = https_service
        self._chats_service = chats_service
        self._module = "chats.controller"

    def create_request(self, request: Request, db: Session):
        user: User = request.state.user

        chat = self._chats_service.create(db=db, chat=ChatCreate(
            user_id=user.user_id
        ))

        return chat.chat_id
 
    def collection_request(self, request: Request, db: Session):
        user: User = request.state.user

        data = self._chats_service.collection(db=db, user_id=user.user_id)
        
        return [self.__to_public(chat) for chat in data]
        
   
    @staticmethod
    def __to_public(message: Chat) -> ChatPublic:
        return ChatPublic.model_validate(message, from_attributes=True, by_name=True)
