from ..taskmanagementapi.db import User

from fastapi import status

valid_user = User(email="123@asd.com", password="123")

def test_user_register(client):
  response = client.post("/login/register", json=valid_user.model_dump())
  assert response.status_code == status.HTTP_201_CREATED

def test_login_user(client):
  response = client.post("/login", json=valid_user.model_dump())
  assert response.status_code == status.HTTP_200_OK