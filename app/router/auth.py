from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session
from .. import database, schemas, models, utils

router = APIRouter(tags=['Authentication'])

@router.post('/login')
def login(user_credantials: schemas.UserLogin, Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email == user_credantials.email).first() # type: ignore

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid Credentials")
    
    if not utils.verify(user_credantials.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid Credentials")
