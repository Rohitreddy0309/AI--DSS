from sqlalchemy.orm import Session
from models.vendors import Vendors
from repositories import vendor_repository
import base64
from repositories.vendor_repository import add_new_vendor
import os
from dotenv import load_dotenv
import requests
load_dotenv()

import shutil
from fastapi import UploadFile




GROQ_API_KEY = os.getenv("GROQ_API_KEY")

API_URL = os.getenv("API_URL")

headers = {
    "Authorization": f"Bearer {GROQ_API_KEY}",
    "Content-Type": "application/json"
}

UPLOAD_FOLDER = "uploads"

async def save_pdf(file: UploadFile):

    # create uploads folder if not exists
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

    file_path = os.path.join(UPLOAD_FOLDER, file.File_name)

    # save file
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {
        "file_name": file.File_name,
        "file_path": file_path
    }


def list_all_vendor(db):
    vendors= vendor_repository.get_all_vendors(db)
    return vendors


async def upload_vendor_file(vendor_name, file, db):
    """Handle complete upload logic."""

    # create uploads folder if it doesn't exist
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

    # create file path
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)

    # read uploaded file
    file_bytes = await file.read()

    # save file locally
    with open(file_path, "wb") as f:
        f.write(file_bytes)

    # convert file to base64 for model input
    image_base64 = base64.b64encode(file_bytes).decode("utf-8")

    payload = {
        "model": "meta-llama/llama-4-scout-17b-16e-instruct",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Analyze this building architecture drawing and list pros and cons."
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{image_base64}"
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

    vendor = Vendors(
        vendor_name=vendor_name,
        File_name=file.filename,
        comments=comments
    )

    saved_vendor = add_new_vendor(db, vendor)

    return {
        "file_id": saved_vendor.file_id,
        "vendor_name": saved_vendor.vendor_name,
        "File_name": saved_vendor.File_name,
        "comments": saved_vendor.comments
    }