
from sqlalchemy.orm import Session

from config.security import hash_password
from schema.user import CreateUser
from cruds.user import user_crud


def create_user(db: Session, user_in: CreateUser):
    """
    Create a new user in the database.
    """
    db_user = user_crud.create(
        db=db,
        obj_in=user_in.model_copy(update={"password": hash_password(user_in.password)}),
    )

    return db_user