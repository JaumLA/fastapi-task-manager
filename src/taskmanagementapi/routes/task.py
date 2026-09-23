from datetime import time
from typing import Annotated

from fastapi import APIRouter, Depends

from pydantic import BaseModel, EmailStr, Field

from sqlalchemy import insert
from sqlmodel import Session, select

from src.taskmanagementapi.db import Task, get_session
from src.taskmanagementapi.authentication import get_current_user

class TaskUser(BaseModel):
  id: int
  email: EmailStr

class TaskResponse(BaseModel):
  task_name: str
  init_time: time | None = None
  end_time: time | None = None

router = APIRouter(prefix="/task")

@router.post("/")
def create_task(
  task: TaskResponse, 
  current_user: Annotated[TaskUser, Depends(get_current_user)],
  session: Annotated[Session, Depends(get_session)]):
  TaskResponse.model_validate(task)
  if not current_user:
    return {"Log again"}

  create_query = insert(Task).values(
    task_name=task.task_name,
    init_time=task.init_time,
    end_time=task.end_time,
    user_id=current_user.id
  )
  created_task = session.exec(create_query).last_inserted_params()
  
  session.commit()
  return created_task

@router.get("/list")
def get_tasks(
  current_user: Annotated[TaskUser, Depends(get_current_user)],
  session: Annotated[Session, Depends(get_session)]
):
  if not current_user:
    return {"Log again"}
  tasks_select = select(Task).where(Task.user_id == current_user.id)
  lot = session.exec(tasks_select).all()
  return lot
  