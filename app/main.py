import uvicorn
from fastapi import FastAPI
from fastapi.responses import FileResponse, JSONResponse

from app.models.models import User

app = FastAPI()


@app.get("/")
async def root():
    return FileResponse("templates/index.html")


@app.post("/sum")
async def calculate(num1: int | float, num2: int | float):
    return JSONResponse({"result": num1 + num2})


@app.get("/custom")
async def read_custom_message():
    return {"message": "This is a custom message!"}


@app.get('/users')
async def get_users():
    user = User(**{"id": "123", "username": "mary"})
    return user

# @app.get("/user/{user_id}")
# async def get_user():


@app.post('/user', response_model=User)
async def get_user(user: User):
    return user


if __name__ == '__main__':
    uvicorn.run(app,
                host='127.0.0.1',
                port=8080)
