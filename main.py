from fastapi import FastAPI
from core.database import engine, Base
from models.Users import Users
from models.Companies import Companies
from models.Projects import Project
from models.Transmittals import Transmittals
from models.deliverables import Deliverables
from models.Review import Comments
from models.checklists import Checklist
from models.Revision import Revision
from models.HistoricalComments import HistoricalComments
from models.Reference import ReferenceDocument


from api.v1.router import router
app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(router, prefix="/api")

@app.get("/")
def read_root():
    return {"message": "FastAPI PostgreSQL working"}