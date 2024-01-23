from pydantic import BaseModel, computed_field
from datetime import date


class User(BaseModel):
    id: int
    username: str
    age: int
    register_at: date = date.today()
    friends: list[int] = []

    @computed_field
    def is_adult(self) -> bool:
        return self.age >= 18
