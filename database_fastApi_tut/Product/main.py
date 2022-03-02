from fastapi import FastAPI
from .import schemas as sh
from .database import engine
from .import models

app = FastAPI()

models.Base.metadata.create_all(engine)

@app.post("/product")
def add(request: sh.Product):
    return request