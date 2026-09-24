from fastapi import FastAPI
from taskmanagementapi import authentication

from taskmanagementapi.routes import login, task

app = FastAPI()

app.include_router(login.router)
app.include_router(authentication.router)
app.include_router(task.router)

@app.get("/")
async def root():
  return {"teste": "Hello from docker!!!"}
