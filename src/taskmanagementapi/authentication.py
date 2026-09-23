from datetime import timedelta, datetime, timezone
from typing import Annotated

from fastapi import Depends, APIRouter, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

import jwt

from pwdlib import PasswordHash
from pwdlib.hashers.bcrypt import BcryptHasher
from pwdlib.hashers.argon2 import Argon2Hasher

from sqlmodel import Session, select

from src.config import TOKEN_SECRET_KEY
from src.taskmanagementapi.db import User, get_session, get_engine

from pydantic import BaseModel, EmailStr

router = APIRouter(prefix="/token")

pswd_hasher = PasswordHash((BcryptHasher(), Argon2Hasher()))

class Token(BaseModel):
  access_token: str
  token_type: str

class TokenData(BaseModel):
  id: int | None
  email: EmailStr
  exp: datetime

class TokenRequest(BaseModel):
  email: EmailStr
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

def check_exp_time(exp_time: datetime):
  return datetime.now() > exp_time.now()

def authenticate_user(user_email: EmailStr, pswd: str):
  user = check_db_user(user_email)
  # Valida hash da senha no banco
  validated =  pswd_hasher.verify(password=pswd, hash=user.password)
  if not validated:
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
  return user

def check_db_user(user_email: EmailStr):
  # Verifica se existe email
  engine = get_engine()
  with Session(engine) as session:
    find_user = select(User).where(User.email == user_email)
    db_user = session.exec(find_user).first()
    if not db_user:
      raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return db_user

async def get_current_user(token_str: Annotated[str, Depends(oauth2_scheme)]):
  decoded_payload = jwt.decode(token_str, key=TOKEN_SECRET_KEY, algorithms=["HS256"])
  token_data = TokenData(**decoded_payload)
  validated_token = check_exp_time(token_data.exp)
  if not validated_token:
    raise jwt.ExpiredSignatureError()
  validated_user = check_db_user(token_data.email)
  if not validated_user:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
  return UserIdentifacation(id=validated_user.id, email=validated_user.email)

@router.post("/")
async def get_token(token_request: TokenRequest):
  current_user = authenticate_user(token_request.email, token_request.password)
  if not current_user:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
  if not current_user.id:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
  token = create_access_token(id=current_user.id, data=token_request)
  return {"Token": token}