"""
Notevera AI – Settings routes
"""
from fastapi import APIRouter, Depends, Body
from database import database
from models.tables import settings as settings_table
from routes.auth import get_current_user

router = APIRouter(prefix="/settings", tags=["Settings"])


@router.get("/")
async def get_settings(current_user=Depends(get_current_user)):
    row = await database.fetch_one(
        settings_table.select().where(settings_table.c.user_id == current_user["id"])
    )
    if not row:
        return {"theme": "dark", "calendar_integration": False, "notifications": True}
    m = dict(row._mapping)
    return {
        "theme": m["theme"],
        "calendar_integration": m["calendar_integration"],
        "notifications": m["notifications"],
    }


@router.put("/")
async def update_settings(data: dict = Body(...), current_user=Depends(get_current_user)):
    row = await database.fetch_one(
        settings_table.select().where(settings_table.c.user_id == current_user["id"])
    )

    update_vals = {}
    if "theme" in data:
        update_vals["theme"] = data["theme"]
    if "calendar_integration" in data:
        update_vals["calendar_integration"] = data["calendar_integration"]
    if "notifications" in data:
        update_vals["notifications"] = data["notifications"]

    if row:
        await database.execute(
            settings_table.update().where(settings_table.c.user_id == current_user["id"]).values(**update_vals)
        )
    else:
        await database.execute(
            settings_table.insert().values(user_id=current_user["id"], **update_vals)
        )

    return {"message": "Settings updated"}
