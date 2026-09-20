from typing import Annotated

from fastapi import APIRouter, Depends, Query

from pydantic import Field
from sqlalchemy import Engine

from taskmanagementapi.db import get_engine, Task

class TaskRequest(Task):
  task_name: str = Field()

router = APIRouter(prefix="/task")

@router.get("/list")
def get_tasks(
  user_id: Annotated[int, Query(gt=0)],
  token: str,
  engine: Annotated[Engine, Depends(get_engine)]
  #check_authentication: Annotated[bool, check_authentication]
):
  pass