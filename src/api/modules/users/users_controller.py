from api.modules.users.users_service import UsersService
from api.modules.users.users_models import UserCreate, User, UserUpdate, UserLogin
from fastapi import BackgroundTasks, Depends, Body, Request, HTTPException
from fastapi.responses import JSONResponse
from api.core.services.http_service import HttpService
import logging
from sqlalchemy.orm import Session

class UsersController:
    def __init__(self, https_service: HttpService, users_service: UsersService):
        self._http_service: HttpService = https_service
        self._users_service = users_service
        self._module = "users.controller"

    def create_request(self, request: Request, db: Session, new_user: UserCreate):
        verification_code = request.state.verification_code

        if new_user.code != verification_code:
            raise HTTPException(status_code=403, detail="Incorrect verification code")
        
        hashed_password = self._http_service.hashing_service.hash_password(password=new_user.password)
        hashed_email = self._http_service.hashing_service.hash_for_search(data=new_user.email)

        user_data = {
            **new_user.model_dump(),
            "password": hashed_password,
            "email_hash": hashed_email
        }
        
        self._users_service.create(db=db, user=user_data)
        
        return {"detail": "User created"}
    

    
    def resource_request(self, request: Request):
        user: User = request.state.user

        data = self._users_service.map_from_db(user=user)
        
        return data
        

    def update_request(self, request: Request, db: Session, data: UserUpdate):
        user: User = request.state.user 

        self._http_service.hashing_service.compare_password(data.oldPassword, user.password)
        hashed_password = self._http_service.hashing_service.hash_password(data.newPassword)
    

        self._users_service.update(
            db=db,
            user_id=user.user_id, 
            changes={"password": hashed_password}
        )

        return {"detail": "User updated"}

    def delete_request(self, request: Request, db: Session):
        user: User = request.state.user

        self._users_service.delete(
            db=db,
            user_id=user.user_id
        )

        return {"detail": "User deleted"}
    
    def login(self, request: Request, db: Session, data: UserLogin): 
        hashed_email = self._http_service.hashing_service.hash_for_search(data=data.email)
        
        user: User = self._http_service.request_validation_service.verify_resource(
            service_key="users_service",
            params={"db": db, "where_col": "email_hash", "identifier": hashed_email},
            not_found_message="User not found",
        )

        self._http_service.hashing_service.compare_password(data.password, user.password)

        token = self._http_service.webtoken_service.generate_token({
            "user_id": str(user.user_id)
        }, "7d")

        return {"token": token}

