from datetime import date

from pydantic import BaseModel, computed_field


class User(BaseModel):
    id: int
    username: str
    age: int
    register_at: date = date.today()
    friends: list[int] = []

    @computed_field
    def is_adult(self) -> bool:
        return self.age >= 18


class Feedback(BaseModel):
    name: str
    message: str


class Product(BaseModel):
    product_id: int
    name: str
    category: str
    price: float
