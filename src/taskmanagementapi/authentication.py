from copy import copy
from datetime import timedelta, datetime, timezone

from fastapi import HTTPException, status
import jwt

from ..config import TOKEN_SECRET_KEY

from pydantic import BaseModel


class Token(BaseModel):
  access_token: str
  token_type: str

class TokenData(BaseModel):
  email: str
  exp: datetime

def create_access_token(data: TokenData, expires_delta: timedelta | None = None):
  to_encode = copy(data)
  if expires_delta:
    expire = datetime.now(timezone.utc) + expires_delta
  else:
    expire = datetime.now(timezone.utc) + timedelta(minutes=30)
  to_encode.exp = expire
  encoded = jwt.encode(to_encode.model_dump(), TOKEN_SECRET_KEY, algorithm="HS256")

  return encoded

def authenticate(token: Token):
  decoded_token = jwt.decode(token.access_token, key=TOKEN_SECRET_KEY)
  token_data = TokenData(**decoded_token)
  if datetime.now() > token_data.exp.now():
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You need to login again")