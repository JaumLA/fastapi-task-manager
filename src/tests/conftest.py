import pytest
from fastapi.testclient import TestClient
from sqlmodel import SQLModel

from ..taskmanagementapi.db import get_engine
from ..taskmanagementapi.main import app
from ..config import TEST_DATABASE_URL

from sqlalchemy import create_engine

if not TEST_DATABASE_URL:
  exit(1)

@pytest.fixture()
def client():
  test_engine = create_engine(url=TEST_DATABASE_URL, echo=True)
  def engine():
    return test_engine
  
  app.dependency_overrides[get_engine] = engine
  SQLModel.metadata.create_all(test_engine)

  yield TestClient(app)



