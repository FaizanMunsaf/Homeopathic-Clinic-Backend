from cruds.base import BaseCRUD
from models.user import User
from schema.user import CreateUser


class UserCRUD(BaseCRUD[User, CreateUser]):
    def __init__(self):
        super().__init__(User)


user_crud = UserCRUD()
