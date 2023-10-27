import math
from fastapi import FastAPI, HTTPException, status
/from models.models import User, ToLogin

app = FastAPI()

db: list[User] = []


@app.post("/auth/register")
def register(user: User):
    for existing_user in db:
        if user.username == existing_user.username or user.email == existing_user.email:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT)
    if "@" not in user.email or ".com" not in user.email:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE)
    db.append(user)
    return user.username, user.email


@app.post("/auth/login")
def login(user_auth: ToLogin):
    for existing_user in db:
        if user_auth.login == existing_user.username or user_auth.login == existing_user.email:
            if user_auth.password == existing_user.password:
                return existing_user.username, existing_user.email

            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
