from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from api.services.user import create_user
from config.database import get_db
from schema.user import CreateUser

router = APIRouter(prefix="/user", tags=["user"])


@router.post("/signup", status_code=201)
def register_user(request: CreateUser, db: Session = Depends(get_db)):
    return create_user(db=db, user_in=request)
