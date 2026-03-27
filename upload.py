"""
Notevera AI – Upload & process study materials
"""
import os
import json
from datetime import datetime
from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Depends
from database import database
from models.tables import materials
from routes.auth import get_current_user
from utils.pdf_parser import extract_pdf_text
from utils.ocr_processor import extract_image_text
from utils.youtube_transcript import extract_youtube_transcript

router = APIRouter(prefix="/upload", tags=["Upload"])

UPLOAD_DIR = os.path.join(os.path.dirname(__file__), "..", "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/file")
async def upload_file(
    file: UploadFile = File(...),
    title: str = Form("Untitled Material"),
    current_user=Depends(get_current_user),
):
    content = await file.read()
    filename = file.filename or "unknown"
    ext = filename.rsplit(".", 1)[-1].lower() if "." in filename else ""

    # Save file
    save_path = os.path.join(UPLOAD_DIR, f"{current_user['id']}_{datetime.now().timestamp()}_{filename}")
    with open(save_path, "wb") as f:
        f.write(content)

    extracted_text = ""
    source_type = "file"

    if ext == "pdf":
        source_type = "pdf"
        extracted_text = extract_pdf_text(save_path)
    elif ext in ("png", "jpg", "jpeg", "webp", "bmp"):
        source_type = "image"
        extracted_text = extract_image_text(save_path)
    elif ext in ("txt", "md"):
        source_type = "text"
        extracted_text = content.decode("utf-8", errors="ignore")
    else:
        extracted_text = content.decode("utf-8", errors="ignore")

    # Save to DB
    insert_q = materials.insert().values(
        user_id=current_user["id"],
        title=title,
        source_type=source_type,
        extracted_text=extracted_text,
        original_filename=filename,
    )
    material_id = await database.execute(insert_q)

    return {
        "id": material_id,
        "title": title,
        "source_type": source_type,
        "text_preview": extracted_text[:500],
        "text_length": len(extracted_text),
    }


@router.post("/text")
async def upload_text(
    title: str = Form("Pasted Notes"),
    text: str = Form(...),
    current_user=Depends(get_current_user),
):
    insert_q = materials.insert().values(
        user_id=current_user["id"],
        title=title,
        source_type="text",
        extracted_text=text,
        original_filename="",
    )
    material_id = await database.execute(insert_q)
    return {"id": material_id, "title": title, "source_type": "text", "text_length": len(text)}


@router.post("/youtube")
async def upload_youtube(
    title: str = Form("YouTube Lecture"),
    url: str = Form(...),
    current_user=Depends(get_current_user),
):
    transcript = extract_youtube_transcript(url)
    if not transcript:
        raise HTTPException(status_code=400, detail="Could not extract transcript from this video")

    insert_q = materials.insert().values(
        user_id=current_user["id"],
        title=title,
        source_type="youtube",
        extracted_text=transcript,
        original_filename=url,
    )
    material_id = await database.execute(insert_q)
    return {"id": material_id, "title": title, "source_type": "youtube", "text_length": len(transcript)}


@router.get("/materials")
async def list_materials(current_user=Depends(get_current_user)):
    query = materials.select().where(materials.c.user_id == current_user["id"]).order_by(materials.c.created_at.desc())
    rows = await database.fetch_all(query)
    return [
        {
            "id": r._mapping["id"],
            "title": r._mapping["title"],
            "source_type": r._mapping["source_type"],
            "text_length": len(r._mapping["extracted_text"]),
            "original_filename": r._mapping["original_filename"],
            "created_at": str(r._mapping["created_at"]),
        }
        for r in rows
    ]


@router.get("/materials/{material_id}")
async def get_material(material_id: int, current_user=Depends(get_current_user)):
    query = materials.select().where(
        (materials.c.id == material_id) & (materials.c.user_id == current_user["id"])
    )
    row = await database.fetch_one(query)
    if not row:
        raise HTTPException(status_code=404, detail="Material not found")
    m = dict(row._mapping)
    return {
        "id": m["id"],
        "title": m["title"],
        "source_type": m["source_type"],
        "extracted_text": m["extracted_text"],
        "original_filename": m["original_filename"],
        "created_at": str(m["created_at"]),
    }
