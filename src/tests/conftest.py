import pytest
from fastapi.testclient import TestClient
from sqlmodel import SQLModel, Session, delete

from ..taskmanagementapi.db import get_engine, User, Task
from ..taskmanagementapi.main import app
from ..config import TEST_DATABASE_URL

from sqlalchemy import create_engine

if not TEST_DATABASE_URL:
  exit(1)

def engine():
  return create_engine(url=TEST_DATABASE_URL)

@pytest.fixture()
def client():
  test_engine = engine()
  
  app.dependency_overrides[get_engine] = engine
  SQLModel.metadata.create_all(test_engine)

  with TestClient(app) as c:
    yield c

  with Session(engine()) as session:
    remove_table_user = delete(User)
    remove_table_task = delete(Task)
    session.execute(remove_table_user)
    session.commit()