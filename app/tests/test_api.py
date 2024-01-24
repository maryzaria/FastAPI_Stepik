from datetime import date

from fastapi import status
from fastapi.testclient import TestClient

from app.db_example import sample_product_1
from app.main import app

client = TestClient(app)


class TestAPI:
    base_url = "http://127.0.0.1:8080/"

    def test_sum_successful(self):
        response = client.post(
            url=f"{self.base_url}sum", params={"num1": 5, "num2": 10}
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {"result": 15}

    def test_sum_bad_request(self):
        response = client.post(url=f"{self.base_url}sum", params={"num1": 5})
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        assert response.json().get("detail", {})[0].get("type") == "missing"

    def test_custom(self):
        response = client.get(url=self.base_url + "custom")
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {"message": "This is a custom message!"}

    def test_create_user(self):
        url = f"{self.base_url}user"
        data = {"id": "123", "username": "mary", "age": "29"}
        response = client.post(url, json=data)
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {
            "id": 123,
            "username": "mary",
            "age": 29,
            "register_at": str(date.today()),
            "friends": [],
            "is_adult": True,
        }

    def test_get_user_by_user_id(self):
        url = f"{self.base_url}user/101"
        response = client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {"message": "user 101"}

        url = f"{self.base_url}user/-101"
        response = client.get(url)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == {"error": "user_id must be a positive number"}

    def test_feedback(self):
        url = f"{self.base_url}feedback"
        correct_data = {"name": "Alice", "message": "Great course! I'm learning a lot."}
        response = client.post(url, json=correct_data)
        assert response.status_code == status.HTTP_200_OK

        incorrect_data = {"message": "Great course! I'm learning a lot."}
        response = client.post(url, json=incorrect_data)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_get_product_by_id(self):
        url = f"{self.base_url}product/123"
        response = client.get(url)
        assert response.json() == sample_product_1

        url = f"{self.base_url}product/1"
        response = client.get(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json() == {"error": f"Product with id=1 not found"}

    def test_get_product_search(self):
        url = (
            f"{self.base_url}product/search?keyword=phone&category=Electronics&limit=1"
        )
        response = client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.json()) == 1
