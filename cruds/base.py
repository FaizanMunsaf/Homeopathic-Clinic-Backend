from sqlalchemy.orm import Session
from typing import Type, TypeVar, Generic
from pydantic import BaseModel


T = TypeVar("T")  # Model type
S = TypeVar("S", bound=BaseModel)  # Schema type


class BaseCRUD(Generic[T, S]):
    def __init__(self, model: Type[T]):
        self.model = model

    def create(self, db: Session, obj_in: S):
        db_obj = self.model(**obj_in.dict())
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_all(self, db: Session):
        return db.query(self.model).all()

    def get(self, db: Session, id_value: str, id_field: str = "id"):
        obj = (
            db.query(self.model)
            .filter(getattr(self.model, id_field) == id_value)
            .first()
        )
        return obj

    def update(self, db: Session, id_value: str, obj_update: S, id_field: str = "id"):
        obj = (
            db.query(self.model)
            .filter(getattr(self.model, id_field) == id_value)
            .first()
        )
        if not obj:
            return None
        update_data = obj_update.model_dump(
            exclude_unset=True
        )  # Exclude fields that are not provided
        for key, value in update_data.items():
            setattr(obj, key, value)

        db.commit()
        db.refresh(obj)
        return obj

    def delete(self, db: Session, id_value: str, id_field: str = "id"):
        obj = (
            db.query(self.model)
            .filter(getattr(self.model, id_field) == id_value)
            .first()
        )
        if not obj:
            return None

        db.delete(obj)
        db.commit()
        return {"message": f"{self.model.__name__} deleted successfully"}
