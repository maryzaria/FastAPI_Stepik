import uvicorn
from fastapi import FastAPI, status
from fastapi.responses import FileResponse, JSONResponse
from typing_extensions import Union

from app.db_example import sample_products
from app.models.models import Feedback, Product, User

app = FastAPI()


@app.get("/")
async def root() -> FileResponse:
    return FileResponse("templates/index.html")


@app.post("/sum")
async def calculate(num1: int | float, num2: int | float) -> JSONResponse:
    return JSONResponse({"result": num1 + num2})


@app.get("/custom")
async def read_custom_message() -> dict:
    return {"message": "This is a custom message!"}


@app.get("/users")
async def get_users() -> User:
    user = User(**{"id": "123", "username": "mary"})
    return user


@app.get("/user/{user_id}", response_model=None)
async def get_user(user_id: int) -> JSONResponse | dict:
    if user_id < 0:
        return JSONResponse(
            {"error": "user_id must be a positive number"},
            status_code=status.HTTP_400_BAD_REQUEST,
        )
    return {"message": f"user {user_id}"}


@app.post("/user", response_model=User)
async def get_user(user: User) -> User:
    # user: User - проверяем входные данные на соответствие модели
    # response_model=User - указываем модель ответа
    return user


@app.post("/feedback")
async def post_feedback(form: Feedback) -> JSONResponse:
    return JSONResponse({"message": f"Feedback received. Thank you, {form.name}!"})


@app.get("/product/search")
async def products_search(
    keyword: str, category: str = None, limit: int = 10
) -> list[Product]:
    result = list(
        filter(lambda item: keyword.lower() in item.get("name", ""), sample_products)
    )
    if category:
        result = list(
            filter(
                lambda item: item.get("category", "").lower() == category.lower(),
                result,
            )
        )
    return result[:limit]


@app.get("/product/{product_id}", response_model=None)
async def detail_product(product_id: int) -> Product | JSONResponse:
    for product in sample_products:
        if product.get("product_id") == product_id:
            return product
    return JSONResponse(
        {"error": f"Product with id={product_id} not found"},
        status_code=status.HTTP_404_NOT_FOUND,
    )


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8080)
