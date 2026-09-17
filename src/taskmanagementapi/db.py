import os
from dotenv import load_dotenv

from datetime import time

from sqlmodel import Field, SQLModel, create_engine

class User(SQLModel, table=True):
  id: int | None = Field(default=None, primary_key=True)
  email: str = Field(unique=True, index=True)
  password: str = Field(exclude=True)

class Tasks(SQLModel, table=True):
  id: int | None = Field(default=None, primary_key=True)
  task_name: str
  init_time: time | None
  end_time: time | None
  user_id: int | None = Field(foreign_key="user.id", ondelete="CASCADE")

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
   exit(1)
engine = create_engine(DATABASE_URL, echo=True)

def create_db_and_tables():
  SQLModel.metadata.create_all(engine)

if __name__ == "__main__":
    create_db_and_tables()