from fastapi import FastAPI

from backend.database import init_db

app = FastAPI()

init_db()


@app.get("/")
def read_root():
    return {"Hello": "asds!"}
