from pydantic import BaseModel


class CreateUser(BaseModel):
    email: str = "test@example.com"
    username: str = "testuser"
    role: str = "super-admin"
    password: str = "None"
