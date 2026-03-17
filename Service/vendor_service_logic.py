from sqlalchemy.orm import Session
from models.vendors import Vendors
from repositories.vendor_repository import add_new_vendor
from repositories import vendor_repository

import base64
import os
import requests
from dotenv import load_dotenv
from utils.pdf_generator import create_pdf
import mimetypes
import shutil
from fastapi import UploadFile

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
API_URL = os.getenv("API_URL")

headers = {
    "Authorization": f"Bearer {GROQ_API_KEY}",
    "Content-Type": "application/json"
}

UPLOAD_FOLDER = "uploads"


def list_all_vendor(db):
    return vendor_repository.get_all_vendors(db)


async def save_pdf(file: UploadFile):
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

    file_path = os.path.join(UPLOAD_FOLDER, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {
        "file_name": file.filename,
        "file_path": file_path
    }


async def upload_vendor_file(vendor_name, file: UploadFile, db):
    """Handle complete upload logic."""

    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

    file_path = os.path.join(UPLOAD_FOLDER, file.filename)

    file_bytes = await file.read()

    # save file
    with open(file_path, "wb") as f:
        f.write(file_bytes)

    # base64 conversion
    image_base64 = base64.b64encode(file_bytes).decode("utf-8")

    mime_type, _ = mimetypes.guess_type(file_path)

    payload = {
        "model": "meta-llama/llama-4-scout-17b-16e-instruct",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": """
You are a professional architectural design reviewer.

Analyze the building architecture drawing and generate a professional design review.

Return the result in this format:

Overview:
Write 2-3 sentences describing the layout and purpose of the drawing.

Pros:
- Write 4 clear advantages of the design.

Cons:
- Write 4 possible issues or design limitations.

Recommendations:
- Write 3 practical improvement suggestions.

Rules:
- Use bullet points starting with "-"
- Do not use numbering
- Keep sentences clear and professional
"""
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:{mime_type};base64,{image_base64}"
                        }
                    }
                ]
            }
        ]
    }

   
    try:
        response = requests.post(
            API_URL,
            headers=headers,
            json=payload,
            timeout=120
        )

        if response.status_code == 200:
            result = response.json()
            comments = result["choices"][0]["message"]["content"]
        else:
            comments = f"Groq error {response.status_code}"

    except Exception as e:
        comments = str(e)


    pdf_data = {
        "vendor_name": vendor_name,
        "File_name": file.filename,
        "comments": comments
    }

    pdf_name = create_pdf(pdf_data)

    vendor = Vendors(
        vendor_name=vendor_name,
        File_name=file.filename,
        comments=pdf_name   # store PDF name
    )

    saved_vendor = add_new_vendor(db, vendor)

    return {
        "file_id": saved_vendor.file_id,
        "vendor_name": saved_vendor.vendor_name,
        "File_name": saved_vendor.File_name,
        "pdf_file": pdf_name
    }