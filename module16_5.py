from fastapi import FastAPI, Path, HTTPException, Request
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import List, Annotated

app = FastAPI()

users: List['User'] = []


class User(BaseModel):
    id: int
    username: str
    age: int


templates = Jinja2Templates(directory="templates")


@app.get("/")
async def read_users(request: Request):
    return templates.TemplateResponse("users.html", {"request": request, "users": users})


@app.get("/user/{user_id}")
async def get_user(request: Request, user_id: Annotated[int, Path(ge=1, le=100)]):
    for user in users:
        if user.id == user_id:
            return templates.TemplateResponse("users.html", {"request": request, "user": user})
    raise HTTPException(status_code=404, detail="User was not found")


@app.post("/user/{username}/{age}")
async def create_user(
    username: Annotated[str, Path(min_length=5, max_length=20, example="UrbanUser")],
    age: Annotated[int, Path(ge=18, le=120, example=24)]
):
    new_id = users[-1].id + 1 if users else 1
    new_user = User(id=new_id, username=username, age=age)
    users.append(new_user)
    return new_user


@app.put("/user/{user_id}/{username}/{age}")
async def update_user(
    user_id: Annotated[int, Path(ge=1, le=100, example=1)],
    username: Annotated[str, Path(min_length=5, max_length=20, example="UrbanProfi")],
    age: Annotated[int, Path(ge=18, le=120, example=28)]
):
    for user in users:
        if user.id == user_id:
            user.username = username
            user.age = age
            return user
    raise HTTPException(status_code=404, detail="User was not found")


@app.delete("/user/{user_id}")
async def delete_user(
    user_id: Annotated[int, Path(ge=1, le=100, example=2)]
):
    for user in users:
        if user.id == user_id:
            users.remove(user)
            return user
    raise HTTPException(status_code=404, detail="User was not found")
