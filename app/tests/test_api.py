from datetime import date

from app.main import app
from fastapi import status
from fastapi.testclient import TestClient

client = TestClient(app)


class TestAPI:
    base_url = 'http://127.0.0.1:8080/'

    def test_sum_successful(self):
        response = client.post(url=f'{self.base_url}sum',
                               params={"num1": 5, "num2": 10})
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {"result": 15}

    def test_sum_bad_request(self):
        response = client.post(url=f'{self.base_url}sum',
                               params={"num1": 5})
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        assert response.json().get("detail", {})[0].get("type") == "missing"

    def test_custom(self):
        response = client.get(url=self.base_url+'custom')
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {"message": "This is a custom message!"}

    def test_create_user(self):
        url = f"{self.base_url}user"
        data = {"id": "123", "username": "mary", 'age': '29'}
        response = client.post(url, json=data)
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {
            'id': 123,
            'username': 'mary',
            'age': 29,
            'register_at': str(date.today()),
            'friends': [], 'is_adult': True
        }

