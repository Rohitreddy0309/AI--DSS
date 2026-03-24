from fastapi import FastAPI
from core.database import engine, Base
from models import vendors
from api.v1.router import router
from fastapi.responses import FileResponse
import os
from models.Users import Users
from models.Companies import Companies
from models.Projects import Project
from models.Transmittals import Transmittals
from models.deliverables import Deliverables
from models.Review import Comments
from models.checklists import Checklist
from models import checklist_items
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

@app.get("/download/{pdf_name}")
def download_pdf(pdf_name: str):

    path = os.path.join("reports", pdf_name)

    return FileResponse(
        path=path,
        media_type="application/pdf",
        filename=pdf_name
    )
@app.get("/")
def read_root():
    return {"message": "FastAPI PostgreSQL working"}
