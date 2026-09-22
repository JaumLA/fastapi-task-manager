from datetime import timedelta, datetime, timezone
from typing import Annotated

from fastapi import Depends, APIRouter
from fastapi.security import OAuth2PasswordBearer

import jwt

from pwdlib import PasswordHash
from pwdlib.hashers.bcrypt import BcryptHasher
from pwdlib.hashers.argon2 import Argon2Hasher

from sqlmodel import Session, select

from src.config import TOKEN_SECRET_KEY
from taskmanagementapi.db import User, get_engine

from pydantic import BaseModel, EmailStr

router = APIRouter(prefix="/token")

pswd_hasher = PasswordHash((BcryptHasher(), Argon2Hasher()))

class Token(BaseModel):
  access_token: str
  token_type: str

class TokenData(BaseModel):
  id: int | None
  email: str
  exp: datetime

class TokenRequest(BaseModel):
  email:str
  password: str

class UserIdentifacation(BaseModel):
  id: int | None
  email: EmailStr

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def create_access_token(id: int | None, data: TokenRequest, expires_delta: timedelta | None = None):
  token_data = TokenData(id=id, email=data.email, exp=datetime.now(timezone.utc))
  if expires_delta:
    expire = token_data.exp + expires_delta
  else:
    expire = token_data.exp + timedelta(minutes=30)
  token_data.exp = expire
  encoded = jwt.encode(token_data.model_dump(), TOKEN_SECRET_KEY, algorithm="HS256")

  return encoded

def authenticate_token(token: Token):
  decoded_token = jwt.decode(token.access_token, key=TOKEN_SECRET_KEY)
  token_data = TokenData(**decoded_token)
  if datetime.now() > token_data.exp.now():
    return None
  else:
    return token_data

def authenticate_user(user_email: str, pswd: str):
  engine = get_engine()
  with Session(engine) as session:
    # Verifica se existe email
    find_user = select(User).where(User.email == user_email)
    db_user = session.exec(find_user).first()
    if not db_user:
      return None

    # Valida hash da senha no banco
    validated =  pswd_hasher.verify(password=pswd, hash=db_user.password)
    if not validated:
      return None
    return db_user

async def get_current_user(token_str: Annotated[str, Depends(oauth2_scheme)]):
  decoded_payload = jwt.decode(token_str, key=TOKEN_SECRET_KEY)
  token_data = Token(**decoded_payload)
  validated_token = authenticate_token(token_data)
  if not validated_token:
    raise Exception()
  validated_user = authenticate_user(validated_token.email, validated_token.email)
  if not validated_user:
    raise Exception()
  return UserIdentifacation(id=validated_user.id, email=validated_user.email)

@router.post("/")
async def get_token(token_request: TokenRequest):
  current_user = authenticate_user(token_request.email, token_request.password)
  if not current_user:
    raise Exception()
  if not current_user.id:
    Exception()
  token = create_access_token(id=current_user.id, data=token_request)
  return {"Token": token}