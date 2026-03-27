"""
Notevera AI – AI Notes generation service and routes
"""
import json
from pydantic import BaseModel
from fastapi import APIRouter, HTTPException, Depends, Body
from database import database
from models.tables import notes, materials
from routes.auth import get_current_user
from services.ai_notes_generator import generate_structured_notes

router = APIRouter(prefix="/notes", tags=["Notes"])


class GenerateNotesRequest(BaseModel):
    material_id: int

@router.post("/generate")
async def generate_notes(
    req: GenerateNotesRequest,
    current_user=Depends(get_current_user),
):
    mid = req.material_id

    # Fetch material
    query = materials.select().where(
        (materials.c.id == mid) & (materials.c.user_id == current_user["id"])
    )
    mat = await database.fetch_one(query)
    if not mat:
        raise HTTPException(status_code=404, detail="Material not found")

    text = mat._mapping["extracted_text"]
    if not text.strip():
        raise HTTPException(status_code=400, detail="No text content in this material")

    structured = generate_structured_notes(text, mat._mapping["title"])

    # Save to DB
    insert_q = notes.insert().values(
        user_id=current_user["id"],
        material_id=mid,
        title=structured["title"],
        content=json.dumps(structured),
    )
    note_id = await database.execute(insert_q)

    return {"id": note_id, **structured}


@router.post("/generate-from-text")
async def generate_notes_from_text(
    data: dict = Body(...),
    current_user=Depends(get_current_user),
):
    text = data.get("text", "")
    title = data.get("title", "Untitled Notes")
    if not text.strip():
        raise HTTPException(status_code=400, detail="No text provided")

    structured = generate_structured_notes(text, title)

    insert_q = notes.insert().values(
        user_id=current_user["id"],
        material_id=None,
        title=structured["title"],
        content=json.dumps(structured),
    )
    note_id = await database.execute(insert_q)

    return {"id": note_id, **structured}


@router.get("/")
async def list_notes(current_user=Depends(get_current_user)):
    query = notes.select().where(notes.c.user_id == current_user["id"]).order_by(notes.c.created_at.desc())
    rows = await database.fetch_all(query)
    result = []
    for r in rows:
        m = dict(r._mapping)
        try:
            content = json.loads(m["content"])
        except Exception:
            content = {"title": m["title"]}
        result.append({
            "id": m["id"],
            "title": m["title"],
            "topic": content.get("topic", ""),
            "summary_preview": content.get("summary", "")[:200],
            "created_at": str(m["created_at"]),
        })
    return result


@router.get("/{note_id}")
async def get_note(note_id: int, current_user=Depends(get_current_user)):
    query = notes.select().where(
        (notes.c.id == note_id) & (notes.c.user_id == current_user["id"])
    )
    row = await database.fetch_one(query)
    if not row:
        raise HTTPException(status_code=404, detail="Note not found")
    m = dict(row._mapping)
    try:
        content = json.loads(m["content"])
    except Exception:
        content = {"title": m["title"], "content": m["content"]}
    return {"id": m["id"], "created_at": str(m["created_at"]), **content}


@router.delete("/{note_id}")
async def delete_note(note_id: int, current_user=Depends(get_current_user)):
    query = notes.delete().where(
        (notes.c.id == note_id) & (notes.c.user_id == current_user["id"])
    )
    await database.execute(query)
    return {"message": "Note deleted"}
