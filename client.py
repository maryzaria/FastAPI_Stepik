import requests
from app.models.models import User

url = "http://127.0.0.1:8080/user"
data = {"id": "123", "username": "mary", 'age': '29'}

response = requests.post(url, json=data)
print(response.json())