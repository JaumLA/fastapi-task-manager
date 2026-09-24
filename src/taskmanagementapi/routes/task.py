from datetime import time
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from pydantic import BaseModel, EmailStr

from sqlmodel import Session, select, insert

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
  session: Annotated[Session, Depends(get_session)]
):
  TaskResponse.model_validate(task)
  if not current_user:
    return {"Log again"}

  create_query = insert(Task).values(
    task_name=task.task_name,
    init_time=task.init_time,
    end_time=task.end_time,
    user_id=current_user.id
  )
  created_task = session.exec(create_query).first()
  
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

@router.delete("/{task_id}")
def delete_task(
  task_id: int, 
  current_user: Annotated[TaskUser, Depends(get_current_user)],
  session: Annotated[Session, Depends(get_session)]
):
  if not current_user:
    return {"Log again"}

  tsk_select = select(Task).where(Task.id == task_id, Task.user_id == current_user.id)
  tsk = session.exec(tsk_select).first()
  if not tsk:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")

  try:
    session.delete(tsk)
    session.commit()
    return {"Status": "Task Deleted"}
  except:
    session.rollback()
    return {"error": "something went wrong"}