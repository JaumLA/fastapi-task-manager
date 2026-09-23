import pytest
from fastapi.testclient import TestClient
from sqlmodel import SQLModel, Session

from src.taskmanagementapi.db import get_session, get_engine
from src.taskmanagementapi.main import app
from src.config import TEST_DATABASE_URL

from sqlalchemy import create_engine

if not TEST_DATABASE_URL:
  exit(1)

def get_engine_override():
  return engine()

@pytest.fixture(scope="session")
def engine():
  test_engine = create_engine(url=TEST_DATABASE_URL)

  SQLModel.metadata.create_all(test_engine)

  yield test_engine

  SQLModel.metadata.drop_all(test_engine)

@pytest.fixture(name="session")
def session_fixture(engine):
  with Session(engine) as session:
    yield session

    session.close()

@pytest.fixture(name="client")
def client_fixture(session: Session):
  def get_session_override():
    return session
  
  app.dependency_overrides[get_session] = get_session_override
  app.dependency_overrides[get_engine] = get_engine_override

  with TestClient(app) as c:
    yield c

  app.dependency_overrides.clear()