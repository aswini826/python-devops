from random import randrange
import time
from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
from . import models
from .database import engine, get_db
from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


class Post(BaseModel):
    movie: str
    genre: str
    published: bool = True
    

while True:

    try:
       conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='ashu', cursor_factory=RealDictCursor)
       cursor = conn.cursor()
       print("Database connection was successfully")
       break

    except Exception as error:
       print("Connection of database failed")
       print("Error :", error)
       time.sleep(2)

new_data = [{"title": "Favorite Movie", "content": "Cruella", "id": 1}, {"title": "Favorite Food", "content": "Briyani", "id": 2}]

def find_id(id):
    for p in new_data:
        if p['id'] == id:
            return p

def find_index(id):
    for i, p in enumerate(new_data):
        if p['id'] == id:
            return i
        
@app.get("/sqltest")
def test_post(db: Session = Depends(get_db)):

    test = db.query(models.Post).all()
    return {"data": test}

@app.get("/")
async def root():
    return {"message": "Hello aswini"}

@app.get("/post")
def get_post(db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts """)
    # database = cursor.fetchall()
    database = db.query(models.Post).all()
    return {"data": database}

@app.post("/create", status_code = status.HTTP_201_CREATED)
def create_post(payload: Post):
    cursor.execute("""INSERT INTO "post" (movie, genre, published) VALUES (%s, %s, %s) RETURNING * """,
                    (payload.movie, payload.genre, payload.published))
    create_database = cursor.fetchone()
    conn.commit()
    return {"data": create_database}

@app.get("/post/{id}")
def get_idpost(id: int, response: Response):
    cursor.execute("""SELECT * FROM post WHERE id = %s""", (str(id)))
    data = cursor.fetchone()
    print(data)

    if not data:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail =f'Post with this id {id} is not available')
    return {"data": data}


@app.delete("/post/{id}")
def delete_post(id: int):
    cursor.execute("""DELETE FROM post WHERE id = %s RETURNING * """, (str(id)))
    delete_data = cursor.fetchone()
    conn.commit()
    print(delete_data)
    if delete_data == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f'Post with this id {id} is not available')
    return Response (status_code = status.HTTP_204_NO_CONTENT)



@app.put("/update/{id}")
def update_post(id: int, posts: Post):
    cursor.execute("""UPDATE post SET movie = %s, genre= %s, published=%s WHERE id =%s RETURNING * """, (posts.movie, posts.genre, posts.published, str(id)))
    update_data = cursor.fetchone()
    conn.commit()

    if update_data == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"Post with the id {id} does not exist")

    return {"data": update_data}