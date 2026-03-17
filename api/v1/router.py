from fastapi import APIRouter, UploadFile, File, Form, Depends
import os
import base64
from Service import vendor_service_logic
from sqlalchemy.orm import Session
from dotenv import load_dotenv
from core.database import get_db
from models.vendors import Vendors

load_dotenv()

router = APIRouter()

@router.post("/upload/")
async def upload_file(
    vendor_name: str = Form(...),
    File_name: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """Upload endpoint."""
    mime_type = File_name.content_type   # detects jpg/png/webp automatically

    result = await vendor_service_logic.upload_vendor_file(
        vendor_name,
        File_name,
        db
    )

    return {
        "message": "Saved successfully",
        "data": result
    }

@router.get("/get all vendors/")
def get_all_analysis( db: Session = Depends(get_db)):
    return vendor_service_logic.list_all_vendor(db)
    
