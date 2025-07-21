from src.api.modules.users.users_models import UserPublic, User, UserUpdate, UserToDB
from src.api.core.repository.base_repository import BaseRepository
from src.api.core.dependencies.container import Container
from src.api.core.services.encryption_service import EncryptionService
import logging
from src.api.core.logs.logger import Logger
from typing import Dict, Any
from sqlalchemy.orm import Session
from uuid import UUID
from src.api.core.decorators.service_error_handler import service_error_handler

class UsersService():
    _MODULE = "users.service" 
    def __init__(self, logger: Logger, repository: BaseRepository):
        self._repository = repository
        self._logger = logger

    @service_error_handler(module=_MODULE)
    def create(self, db: Session, user: UserToDB) -> UserPublic:
        return self._repository.create(db, self.__map_to_db(UserToDB(**user)))

    @service_error_handler(module=_MODULE)
    def resource(self, db: Session, where_col: str, identifier: str | UUID) -> User | None:
        return self._repository.get_one(db, where_col, identifier)

    @service_error_handler("users.service")
    def update(self, db: Session, user_id: UUID, changes: UserUpdate) -> UserPublic:
        return self.map_from_db(self._repository.update(db, key="user_id", value=user_id, changes=changes))

    @service_error_handler(module=_MODULE)
    def delete(self, db: Session, user_id: UUID) -> UserPublic:
        return self.map_from_db(self._repository.delete(db, key="user_id", value=user_id))

    @staticmethod
    def __map_to_db(user: UserToDB) -> User:
        encryption_service: EncryptionService = Container.resolve("encryption_service")
        return User(
            email=encryption_service.encrypt(user.email),
            email_hash=user.email_hash,
            password=user.password
        )

    @staticmethod
    def map_from_db(user: User) -> UserPublic:
        encryption_service: EncryptionService = Container.resolve("encryption_service")
        return UserPublic(
            userId=str(user.user_id),
            email=encryption_service.decrypt(user.email)
        )
