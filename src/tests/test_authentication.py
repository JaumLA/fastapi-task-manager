from fastapi import status

valid_user = dict(email="123@token.com", password="oi12312321d")
valid_user_existing = dict(email="123@token.puc", password="oooo213asd21")

def test_token_creation(client):
  user = client.post("/login/register", json=valid_user)
  response = client.post("/token", json=valid_user)
  response.status_code = status.HTTP_201_CREATED