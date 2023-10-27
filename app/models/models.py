from pydantic import BaseModel


class User(BaseModel):
    username: str
    email: str
    password: str


class ToLogin(BaseModel):
    login: str
    password: str


class ToGetUsers(BaseModel):
    page: int
    limit: int
