from pydantic import BaseModel
from datetime import datetime

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