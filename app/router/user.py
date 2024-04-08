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
    prefix="/users",
    tags=['Users']
)


@router.post("/", status_code = status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):

    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    create_users = models.User(**user.dict())

    db.add(create_users)
    db.commit()
    db.refresh(create_users)

    return  create_users


@router.get("/{id}", response_model = schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail =f'Post with this id {id} is not available')
    return  user