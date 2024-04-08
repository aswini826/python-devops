from random import randrange
import time
from typing import Optional, List
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
from . import models,schemas,utils
from .database import engine, get_db
from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import mode
from .router import post,user


models.Base.metadata.create_all(bind=engine)

app = FastAPI()


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
        

@app.get("/")
async def root():
    return {"message": "Hello aswini"}

app.include_router(post.router)
app.include_router(user.router)


