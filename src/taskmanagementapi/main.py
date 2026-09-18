from fastapi import FastAPI

from .routes import login

app = FastAPI()

app.include_router(login.router)

@app.get("/")
async def root():
  return {"teste": "Hello World!!!"}
