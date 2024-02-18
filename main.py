from random import randrange
from typing import Optional
from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel

app = FastAPI()

class Post(BaseModel):
    Movie: str
    Genre: str
    Rating: Optional[float] = None 
    Published: bool = True


new_data = [{"title": "Favorite Movie", "content": "Cruella", "id": 1}, {"title": "Favorite Food", "content": "Briyani", "id": 2}]


@app.get("/")
async def root():
    return {"message": "Hello aswini"}

@app.get("/post")
def get_post():
    return {"data": new_data}

@app.post("/create")
def create_post(payload: Post):
    post_dict = payload.dict()
    post_dict['id'] = randrange(0, 1000000)
    new_data.append(post_dict)
    return {"data": post_dict}
