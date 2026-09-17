from fastapi import APIRouter

from sqlmodel import Session, select

from src.taskmanagementapi.db import engine, User

from pwdlib import PasswordHash
from pwdlib.hashers.bcrypt import BcryptHasher
from pwdlib.hashers.argon2 import Argon2Hasher

pswd_hasher = PasswordHash((BcryptHasher(), Argon2Hasher()))

router = APIRouter(
  prefix="/login"
)

@router.post("/")
async def login(user: User):
  error_message = {"message": "Wrong credentials."}
  with Session(engine) as session:

    if not user.password or not user.email:
      return {"message": "Missing password or email."}
    
    User.model_validate(user)

    statement = select(User).where(User.email == user.email)
    db_user = session.exec(statement).first()
    if not db_user:
      return error_message
    
    validation, updated_hash_pswd =  pswd_hasher.verify_and_update(password=user.password, hash=db_user.password)
    if not validation:
      return error_message

    db_user.password = updated_hash_pswd if updated_hash_pswd else db_user.password
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user

@router.post("/register")
async def register_user(user: User):
  with Session(engine) as session:
    User.model_validate(user)
    pswd_hashed = pswd_hasher.hash(user.password)
    hashed_user = User(email=user.email, password=pswd_hashed)
    try:
      session.add(hashed_user)
      session.commit()
      session.refresh(hashed_user)
      return {"message": "User created!", "user": hashed_user}
    except:
      return {"message": "email already used"}

