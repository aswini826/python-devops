from random import randrange
from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel

app = FastAPI()

class Post(BaseModel):
    Movie: str
    Genre: str
    Rating: Optional[float] = None 
    Published: bool = True
    

class Update(BaseModel):
    title: str
    content: str


new_data = [{"title": "Favorite Movie", "content": "Cruella", "id": 1}, {"title": "Favorite Food", "content": "Briyani", "id": 2}]

def find_id(id):
    for p in new_data:
        if p['id'] == id:
            return p

def find_index(id):
    for i, p in enumerate(new_data):
        if p['id'] == id:
            return i

@app.get("/")
async def root():
    return {"message": "Hello aswini"}

@app.get("/post")
def get_post():
    return {"data": new_data}

@app.post("/create", status_code = status.HTTP_201_CREATED)
def create_post(payload: Post):
    post_dict = payload.dict()
    post_dict['id'] = randrange(0, 1000000)
    new_data.append(post_dict)
    return {"data": post_dict}

@app.get("/post/{id}")
def get_idpost(id: int, response: Response):
    find = find_id(id)
    if not find:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail =f'Post with this id {id} is not available')
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'message': f'Post with this id {id} is not available'}
    print(find)
    return {"data": find}


@app.delete("/post/{id}", status_code = status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    index = find_index(id)
    new_data.pop(index)
    return {'message': 'Your data deleted successfully'}

@app.put("/update/{id}")
def update_post(id: int, posts: Update):
    print(posts)
    index = find_index(id)
    if index == None:
        raise HTTPException(status_code = status.HTTP_201_CREATED, detail=f"Post with the id {id} does not exist")
    
    post_dict = posts.dict()
    post_dict['id'] = id
    new_data[index] = post_dict
    return {"data": post_dict}