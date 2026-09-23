from fastapi import FastAPI
from src.taskmanagementapi import authentication

from src.taskmanagementapi.routes import login, task

app = FastAPI()

app.include_router(login.router)
app.include_router(authentication.router)
app.include_router(task.router)

@app.get("/")
async def root():
  return {"teste": "Hello World!!!"}
