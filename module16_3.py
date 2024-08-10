from fastapi import FastAPI, Path, HTTPException
from typing import Annotated

app = FastAPI()

users = {'1': 'Имя: Example, возраст: 18'}

@app.get("/users")
async def get_users():
    return users

@app.post("/user/{username}/{age}")
async def create_user(
    username: Annotated[str, Path(description="Enter username", min_length=5, max_length=20, example="UrbanUser")],
    age: Annotated[int, Path(description="Enter age", ge=18, le=120, example=24)]
):
    new_id = str(max(map(int, users.keys())) + 1)
    users[new_id] = f"Имя: {username}, возраст: {age}"
    return f"User {new_id} is registered"

@app.put("/user/{user_id}/{username}/{age}")
async def update_user(
    user_id: Annotated[int, Path(description="Enter User ID", ge=1, le=100, example=1)],
    username: Annotated[str, Path(description="Enter username", min_length=5, max_length=20, example="UrbanProfi")],
    age: Annotated[int, Path(description="Enter age", ge=18, le=120, example=28)]
):
    user_id = str(user_id)
    if user_id in users:
        users[user_id] = f"Имя: {username}, возраст: {age}"
        return f"User {user_id} has been updated"
    else:
        raise HTTPException(status_code=404, detail="User not found")

@app.delete("/user/{user_id}")
async def delete_user(
    user_id: Annotated[int, Path(description="Enter User ID", ge=1, le=100, example=2)]
):
    user_id = str(user_id)
    if user_id in users:
        del users[user_id]
        return f"User {user_id} has been deleted"
    else:
        raise HTTPException(status_code=404, detail="User not found")
