from pydantic import BaseModel, EmailStr, Field
from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from src.api.core.database.db_models import Base 
import uuid


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    code: int

class VerifyEmail(BaseModel):
    email: EmailStr

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserUpdate(BaseModel):
    newPassword: str
    oldPassword: str

class UserPublic(BaseModel):
    userId: str
    email: EmailStr

class UserToDB(BaseModel):
    email: EmailStr
    email_hash: str
    password: str
    code: int
    


class User(Base):
    __tablename__ = "users"

    user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    email_hash = Column(String, unique=True, nullable=False, index=True)
    password = Column(String, nullable=False)

