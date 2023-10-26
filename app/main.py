from fastapi import FastAPI, HTTPException, status
from models.models import User

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
    return user.username, db
