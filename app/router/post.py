from random import randrange
import time
from typing import Optional, List
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from fastapi.params import Body
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
from .. import models,schemas,utils
from ..database import engine, get_db
from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import mode

router = APIRouter(
    prefix="/post",
    tags=['Posts']
)


@router.get("/", response_model=List[schemas.PostResponse])
def get_post(db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts """)
    # database = cursor.fetchall()
    database = db.query(models.Post).all()
    return database



@router.post("/create", status_code = status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_post(payload: schemas.CreatePost, db: Session = Depends(get_db)):
    # cursor.execute("""INSERT INTO "post" (movie, genre, published) VALUES (%s, %s, %s) RETURNING * """,
    #                 (payload.movie, payload.genre, payload.published))
    # create_database = cursor.fetchone()
    # conn.commit()
    create_database = models.Post(**payload.dict())

    db.add(create_database)
    db.commit()
    db.refresh(create_database)
    return  create_database



@router.get("/{id}", response_model=schemas.PostResponse)
def get_idpost(id: int, response: Response, db: Session = Depends(get_db)):
    data = db.query(models.Post).filter(models.Post.id == id).first()
    # cursor.execute("""SELECT * FROM post WHERE id = %s""", (str(id)))
    # data = cursor.fetchone()
    if not data:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail =f'Post with this id {id} is not available')
    return  data



@router.delete("/{id}")
def delete_post(id: int, db: Session = Depends(get_db)):
    delete_data = db.query(models.Post).filter(models.Post.id == id)
    # cursor.execute("""DELETE FROM post WHERE id = %s RETURNING * """, (str(id)))
    # delete_data = cursor.fetchone()
    # conn.commit()
    if delete_data.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f'Post with this id {id} is not available')

    delete_data.delete(synchronize_session = False)
    db.commit()
    return Response (status_code = status.HTTP_204_NO_CONTENT)



@router.put("/update/{id}", response_model=schemas.PostResponse)
def update_post(id: int, posts: schemas.CreatePost, db: Session = Depends(get_db)):
    # cursor.execute("""UPDATE post SET movie = %s, genre= %s, published=%s WHERE id =%s RETURNING * """, (posts.movie, posts.genre, posts.published, str(id)))
    # update_data = cursor.fetchone()
    # conn.commit()

    update_data = db.query(models.Post).filter(models.Post.id == id)
    first = update_data.first()

    if first == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"Post with the id {id} does not exist")
    
    update_data.update(posts.dict(), synchronize_session = False)
    db.commit()
    return update_data.first()