from fastapi import FastAPI, Path
from typing import Annotated

app = FastAPI()


@app.get("/")
async def read_root():
    return {"message": "Главная страница"}


@app.get("/user/admin")
async def admin_page():
    return {"message": "Вы вошли как администратор"}


@app.get("/user/{user_id}")
async def user_page(
    user_id: Annotated[int, Path(description="Enter User ID", ge=1, le=100, example=1)]
):
    return {"message": f"Вы вошли как пользователь № {user_id}"}


@app.get("/user/{username}/{age}")
async def user_info(
    username: Annotated[str, Path(description="Enter username", min_length=5, max_length=20, example="UrbanUser")],
    age: Annotated[int, Path(description="Enter age", ge=18, le=120, example=24)]
):
    return {"message": f"Информация о пользователе. Имя: {username}, Возраст: {age}"}
