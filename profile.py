"""
Notevera AI – Profile routes
"""
from fastapi import APIRouter, Depends, Body
from database import database
from models.tables import users, materials, notes, study_tasks
from routes.auth import get_current_user
import sqlalchemy

router = APIRouter(prefix="/profile", tags=["Profile"])


@router.get("/")
async def get_profile(current_user=Depends(get_current_user)):
    return {
        "id": str(current_user["id"]),
        "name": current_user["name"],
        "email": current_user["email"],
        "avatar": current_user.get("avatar", ""),
        "created_at": str(current_user.get("created_at", "")),
    }


@router.put("/")
async def update_profile(data: dict = Body(...), current_user=Depends(get_current_user)):
    update_vals = {}
    if "name" in data:
        update_vals["name"] = data["name"]
    if "avatar" in data:
        update_vals["avatar"] = data["avatar"]

    if update_vals:
        await database.execute(
            users.update().where(users.c.id == current_user["id"]).values(**update_vals)
        )

    return {"message": "Profile updated"}


@router.get("/stats")
async def get_stats(current_user=Depends(get_current_user)):
    uid = current_user["id"]

    mat_count = await database.fetch_one(
        sqlalchemy.select(sqlalchemy.func.count()).select_from(materials).where(materials.c.user_id == uid)
    )
    notes_count = await database.fetch_one(
        sqlalchemy.select(sqlalchemy.func.count()).select_from(notes).where(notes.c.user_id == uid)
    )
    tasks_done = await database.fetch_one(
        sqlalchemy.select(sqlalchemy.func.count()).select_from(study_tasks).where(
            (study_tasks.c.user_id == uid) & (study_tasks.c.completed == True)
        )
    )

    return {
        "materials": list(mat_count._mapping.values())[0] if mat_count else 0,
        "notes": list(notes_count._mapping.values())[0] if notes_count else 0,
        "tasks_completed": list(tasks_done._mapping.values())[0] if tasks_done else 0,
        "streak": 1,
    }
