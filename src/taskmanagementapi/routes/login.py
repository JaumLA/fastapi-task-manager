from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from pydantic import BaseModel, EmailStr, Field, ValidationError

from sqlalchemy import Engine
from sqlmodel import Session, select

from taskmanagementapi.authentication import authenticate_user, pswd_hasher
from taskmanagementapi.db import get_engine, User

router = APIRouter(
  prefix="/login"
)

class UserRequest(BaseModel):
  email: EmailStr
  password: str = Field(min_length=8, max_length=32)

@router.post("/")
async def login(user: UserRequest, engine: Annotated[Engine, Depends(get_engine)]):
  error_message = {"message": "Wrong credentials."}

  if not user.password or not user.email:
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Missing information")

  UserRequest.model_validate(user)

  response_user = authenticate_user(user_email=user.email, pswd=user.password)
  return response_user

@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(user: UserRequest, engine: Annotated[Engine, Depends(get_engine)]):
  with Session(engine) as session:

    try:
      UserRequest.model_validate(user)
    except ValidationError as e:
      raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=e.errors())

    operation = select(User).where(User.email == user.email)
    is_email_used = session.exec(operation).first()
    if is_email_used:
      raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Email already used"
      )

    pswd_hashed = pswd_hasher.hash(user.password)
    hashed_user = User(email=user.email, password=pswd_hashed)

    try:
      session.add(hashed_user)
      session.commit()
      session.refresh(hashed_user)
      return {"message": "User created!", "user": hashed_user}
    except:
      session.rollback()

