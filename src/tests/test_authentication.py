from fastapi import status

from src.taskmanagementapi.authentication import get_current_user

valid_user = dict(email="123@token.com", password="oi12312321d")
valid_user_authentication = dict(email="123@token.puc", password="oooo213asd21")

def test_token_creation(client):
  user = client.post("/login/register", json=valid_user)
  response = client.post("/token", json=valid_user)
  assert response.status_code == status.HTTP_201_CREATED

async def test_token_authentication(client, session):
  user = client.post("/login/register", json=valid_user_authentication)

  response = client.post("/token", json=valid_user_authentication)
  assert response.status_code == status.HTTP_201_CREATED
  print(response.json())
  user = await get_current_user(token_str=response.json()["access_token"], session=session)

  assert user is not None