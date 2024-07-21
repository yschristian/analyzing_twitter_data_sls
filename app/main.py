from fastapi import FastAPI
from .routers import q2
from . import models
from .database import engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(q2.router)

@app.get("/")
def read_root():
    return {"Hello": "World"}
