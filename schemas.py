from pydantic import BaseModel
from typing import Optional


# User model
class UserInDB(BaseModel):
    username: str
    email: str
    password: str


class LoginRequest(BaseModel):
    username: str
    password: str


# Task creation model
class TaskModel(BaseModel):
    ip_address: str


class RefreshTokenRequest(BaseModel):
    refresh_token: str


# Pydantic model for returning user details
class UserResponse(BaseModel):
    username: str
    email: str


# Pydantic model for token data
class TokenData(BaseModel):
    username: str
    exp: Optional[int] = None


# Task creation model
class TaskCreate(BaseModel):
    ip_address: str
