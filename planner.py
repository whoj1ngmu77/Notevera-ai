"""
Notevera AI – Study Planner routes
"""
import json
from fastapi import APIRouter, HTTPException, Depends, Body
from database import database
from models.tables import study_plans, study_tasks, notes
from routes.auth import get_current_user
from services.study_planner import generate_study_plan

router = APIRouter(prefix="/planner", tags=["Study Planner"])


@router.post("/generate")
async def create_plan(
    data: dict = Body(...),
    current_user=Depends(get_current_user),
):
    note_ids = data.get("note_ids", [])
    exam_date = data.get("exam_date", "")
    title = data.get("title", "Study Plan")

    # Gather topics from notes
    topics = []
    for nid in note_ids:
        row = await database.fetch_one(
            notes.select().where((notes.c.id == nid) & (notes.c.user_id == current_user["id"]))
        )
        if row:
            try:
                content = json.loads(row._mapping["content"])
                topics.append(content.get("title", row._mapping["title"]))
            except Exception:
                topics.append(row._mapping["title"])

    if not topics:
        topics = [title]

    plan = generate_study_plan(topics, exam_date)

    plan_id = await database.execute(
        study_plans.insert().values(
            user_id=current_user["id"],
            title=title,
            exam_date=exam_date,
            plan_data=json.dumps(plan),
        )
    )

    # Create study tasks
    for task in plan.get("tasks", []):
        await database.execute(
            study_tasks.insert().values(
                user_id=current_user["id"],
                plan_id=plan_id,
                title=task["title"],
                description=task.get("description", ""),
                due_date=task.get("due_date", ""),
                completed=False,
            )
        )

    return {"id": plan_id, **plan}


@router.get("/plans")
async def list_plans(current_user=Depends(get_current_user)):
    query = study_plans.select().where(study_plans.c.user_id == current_user["id"]).order_by(study_plans.c.created_at.desc())
    rows = await database.fetch_all(query)
    return [
        {
            "id": r._mapping["id"],
            "title": r._mapping["title"],
            "exam_date": r._mapping["exam_date"],
            "created_at": str(r._mapping["created_at"]),
        }
        for r in rows
    ]


@router.get("/plans/{plan_id}")
async def get_plan(plan_id: int, current_user=Depends(get_current_user)):
    row = await database.fetch_one(
        study_plans.select().where(
            (study_plans.c.id == plan_id) & (study_plans.c.user_id == current_user["id"])
        )
    )
    if not row:
        raise HTTPException(status_code=404, detail="Plan not found")
    m = dict(row._mapping)
    plan_data = json.loads(m["plan_data"])
    return {"id": m["id"], "title": m["title"], "exam_date": m["exam_date"], **plan_data}


@router.get("/tasks")
async def list_tasks(current_user=Depends(get_current_user)):
    query = study_tasks.select().where(study_tasks.c.user_id == current_user["id"]).order_by(study_tasks.c.due_date)
    rows = await database.fetch_all(query)
    return [
        {
            "id": r._mapping["id"],
            "title": r._mapping["title"],
            "description": r._mapping["description"],
            "due_date": r._mapping["due_date"],
            "completed": r._mapping["completed"],
            "plan_id": r._mapping["plan_id"],
        }
        for r in rows
    ]


@router.patch("/tasks/{task_id}")
async def toggle_task(task_id: int, data: dict = Body(...), current_user=Depends(get_current_user)):
    row = await database.fetch_one(
        study_tasks.select().where(
            (study_tasks.c.id == task_id) & (study_tasks.c.user_id == current_user["id"])
        )
    )
    if not row:
        raise HTTPException(status_code=404, detail="Task not found")

    completed = data.get("completed", not row._mapping["completed"])
    await database.execute(
        study_tasks.update().where(study_tasks.c.id == task_id).values(completed=completed)
    )
    return {"id": task_id, "completed": completed}
