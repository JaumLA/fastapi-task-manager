from fastapi import FastAPI
from taskmanagementapi import authentication

from taskmanagementapi.routes import login

app = FastAPI()

app.include_router(login.router)
app.include_router(authentication.router)

@app.get("/")
async def root():
  return {"teste": "Hello World!!!"}
