from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class BasePost(BaseModel):
    movie: str
    genre: str
    published: bool = True


class CreatePost(BasePost):
    pass


class PostResponse(BasePost):
    id: int
    created_at: datetime
    class Config:
        orm_mode=True


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode=True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None
    