"""
Notevera AI – Study Planner service
Generates study schedules based on topics and exam dates.
"""
from datetime import datetime, timedelta
from typing import Dict, List


def generate_study_plan(topics: List[str], exam_date: str = "") -> Dict:
    """Generate a study plan with daily tasks."""
    today = datetime.now()

    # Parse exam date
    if exam_date:
        try:
            exam_dt = datetime.strptime(exam_date, "%Y-%m-%d")
        except ValueError:
            exam_dt = today + timedelta(days=14)
    else:
        exam_dt = today + timedelta(days=14)

    total_days = max((exam_dt - today).days, 1)
    days_per_topic = max(total_days // max(len(topics), 1), 1)

    tasks = []
    schedule = []
    current_date = today

    for i, topic in enumerate(topics):
        # Phase 1: Learn (day 1 of topic)
        learn_date = (current_date + timedelta(days=0)).strftime("%Y-%m-%d")
        tasks.append({
            "title": f"📖 Study: {topic}",
            "description": f"Read through all notes and material on {topic}. Understand core concepts.",
            "due_date": learn_date,
            "type": "learn",
        })

        # Phase 2: Watch lecture (day 1-2)
        watch_date = (current_date + timedelta(days=min(1, days_per_topic - 1))).strftime("%Y-%m-%d")
        tasks.append({
            "title": f"🎥 Watch lecture: {topic}",
            "description": f"Watch recommended YouTube lectures on {topic}.",
            "due_date": watch_date,
            "type": "watch",
        })

        # Phase 3: Practice (day 2-3)
        practice_date = (current_date + timedelta(days=min(2, days_per_topic - 1))).strftime("%Y-%m-%d")
        tasks.append({
            "title": f"✍️ Practice: {topic}",
            "description": f"Solve practice problems and attempt quiz questions on {topic}.",
            "due_date": practice_date,
            "type": "practice",
        })

        # Phase 4: Revise (last day)
        revise_date = (current_date + timedelta(days=days_per_topic - 1)).strftime("%Y-%m-%d")
        tasks.append({
            "title": f"🔄 Revise: {topic}",
            "description": f"Quick revision of {topic}. Review bullet points and key concepts.",
            "due_date": revise_date,
            "type": "revise",
        })

        schedule.append({
            "topic": topic,
            "start_date": current_date.strftime("%Y-%m-%d"),
            "end_date": (current_date + timedelta(days=days_per_topic - 1)).strftime("%Y-%m-%d"),
            "days": days_per_topic,
        })

        current_date += timedelta(days=days_per_topic)

    # Add final revision day
    if topics:
        final_date = (exam_dt - timedelta(days=1)).strftime("%Y-%m-%d")
        tasks.append({
            "title": "🎯 Final Revision - All Topics",
            "description": "Complete review of all topics. Focus on weak areas.",
            "due_date": final_date,
            "type": "final_revision",
        })
        tasks.append({
            "title": "🧠 Oral Exam Practice",
            "description": "Practice answering questions verbally for all topics.",
            "due_date": final_date,
            "type": "oral_practice",
        })

    return {
        "topics": topics,
        "exam_date": exam_date or exam_dt.strftime("%Y-%m-%d"),
        "total_days": total_days,
        "schedule": schedule,
        "tasks": tasks,
        "daily_hours_recommended": min(max(len(topics) * 1.5, 2), 8),
    }
