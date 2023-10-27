from fastapi import FastAPI, HTTPException, status
from app.models.models import User, ToLogin
from email_validator import validate_email, EmailNotValidError
from bcrypt import hashpw, checkpw, gensalt

app = FastAPI()

db: list[User] = []


@app.post("/auth/register")
async def register(user: User):
    try:
        emailinfo = validate_email(user.email, check_deliverability=False)
        user.email = emailinfo.normalized
    except EmailNotValidError as error:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(error))

    for existing_user in db:
        if user.username == existing_user.username or user.email == existing_user.email:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT)

    user.password = str(hashpw(bytes(user.password, "UTF8"), gensalt()), "UTF8")

    db.append(user)
    return {"username": user.username, "email": user.email}


@app.post("/auth/login")
async def login(user_auth: ToLogin):
    for existing_user in db:
        if user_auth.login == existing_user.username or user_auth.login == existing_user.email:
            if checkpw(bytes(user_auth.password, "UTF8"), bytes(existing_user.password, "UTF8")):
                return {"username": existing_user.username, "email": existing_user.email}

            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@app.get("/users")
async def get_users(page: int | None = None, limit: int | None = None):
    users = db

    if page is not None and limit is not None:
        users = db[(page - 1) * limit: page * limit]

    return list(map(
        lambda user: {"username": user.username, "email": user.email},
        users
    ))
