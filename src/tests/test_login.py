from ..taskmanagementapi.db import User

from fastapi import status

valid_user = dict(email="123@asd.com", password="oi")
valid_user_existing = dict(email="123@asd.puc", password="oooo")

def test_register_valid_user(client):
  response = client.post("/login/register", json=valid_user)
  assert response.status_code == status.HTTP_201_CREATED

def test_register_existing_user(client):
  response = client.post("login/register", json=valid_user_existing)
  assert response.status_code == status.HTTP_201_CREATED

  client.post("/login/register", json=valid_user_existing)
  response = client.post("/login/register", json=valid_user_existing)
  assert response.status_code == status.HTTP_400_BAD_REQUEST

def test_register_check_type(client):
  response = client.post("/login/register", json={"email": 123, "password": "asd"})
  print(response)


def test_login_valid_user(client):
  response = client.post("/login", json=valid_user)
  assert response.status_code == status.HTTP_200_OK