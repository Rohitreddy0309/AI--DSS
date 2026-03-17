from fastapi import FastAPI
from core.database import engine, Base
from models import vendors
from api.v1.router import router
app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(router, prefix="/api")

@app.get("/")
def read_root():
    return {"message": "FastAPI PostgreSQL working"}