from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Response, status

from pydantic import ValidationError

from sqlalchemy import Engine
from sqlmodel import Session, select

from ...taskmanagementapi.db import get_engine, User

from pwdlib import PasswordHash
from pwdlib.hashers.bcrypt import BcryptHasher
from pwdlib.hashers.argon2 import Argon2Hasher

pswd_hasher = PasswordHash((BcryptHasher(), Argon2Hasher()))

router = APIRouter(
  prefix="/login"
)

@router.post("/")
async def login(user: User, engine: Annotated[Engine, Depends(get_engine)]):
  error_message = {"message": "Wrong credentials."}
  with Session(engine) as session:

    if not user.password or not user.email:
      raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Missing information")

    User.model_validate(user)

    # Verifica se existe email
    statement = select(User).where(User.email == user.email)
    db_user = session.exec(statement).first()
    if not db_user:
      return error_message

    # Valida hash da senha no banco
    validation, updated_hash_pswd =  pswd_hasher.verify_and_update(password=user.password, hash=db_user.password)
    if not validation:
      return error_message

    # Se precisar atualiza o hash da senha
    db_user.password = updated_hash_pswd if updated_hash_pswd else db_user.password
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user

@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(user: User, engine: Annotated[Engine, Depends(get_engine)]):
  with Session(engine) as session:

    try:
      User.model_validate(user)
    except ValidationError:
      raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Wrong parameter type")

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

