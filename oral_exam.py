"""
Notevera AI – Oral Exam Practice routes
"""
import json
from fastapi import APIRouter, HTTPException, Depends, Body
from database import database
from models.tables import notes
from routes.auth import get_current_user
from services.quiz_generator import generate_oral_questions, evaluate_answer

router = APIRouter(prefix="/oral-exam", tags=["Oral Exam"])


@router.post("/generate-questions")
async def generate_questions(
    data: dict = Body(...),
    current_user=Depends(get_current_user),
):
    note_id = data.get("note_id")
    topic = data.get("topic", "")
    num_questions = data.get("num_questions", 5)

    context = ""
    if note_id:
        row = await database.fetch_one(
            notes.select().where(
                (notes.c.id == note_id) & (notes.c.user_id == current_user["id"])
            )
        )
        if row:
            try:
                content = json.loads(row._mapping["content"])
                context = content.get("summary", "") + " " + " ".join(
                    [c.get("explanation", "") for c in content.get("key_concepts", [])]
                )
                topic = topic or content.get("topic", content.get("title", ""))
            except Exception:
                context = row._mapping["content"]

    if not topic:
        raise HTTPException(status_code=400, detail="Provide a topic or note_id")

    questions = generate_oral_questions(topic, context, num_questions)
    return {"topic": topic, "questions": questions}


@router.post("/evaluate")
async def evaluate_student_answer(
    data: dict = Body(...),
    current_user=Depends(get_current_user),
):
    question = data.get("question", "")
    answer = data.get("answer", "")
    expected = data.get("expected_answer", "")

    if not question or not answer:
        raise HTTPException(status_code=400, detail="Provide question and answer")

    result = evaluate_answer(question, answer, expected)
    return result
