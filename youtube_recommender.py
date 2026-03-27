"""
Notevera AI – YouTube Recommender service
"""
from typing import Dict, List


def recommend_lectures(topic: str) -> List[Dict]:
    """Recommend YouTube lectures based on topic."""
    search_query = topic.replace(" ", "+")
    return [
        {
            "title": f"{topic} - Full Course Lecture",
            "channel": "Academic Learning Hub",
            "url": f"https://www.youtube.com/results?search_query={search_query}+full+course+lecture",
            "views": "1.2M views",
            "thumbnail": f"https://img.youtube.com/vi/dQw4w9WgXcQ/mqdefault.jpg",
        },
        {
            "title": f"{topic} Explained - Easy Tutorial",
            "channel": "Study Simply",
            "url": f"https://www.youtube.com/results?search_query={search_query}+explained+tutorial",
            "views": "890K views",
            "thumbnail": f"https://img.youtube.com/vi/dQw4w9WgXcQ/mqdefault.jpg",
        },
        {
            "title": f"{topic} - Quick Revision in 15 Minutes",
            "channel": "Exam Prep Pro",
            "url": f"https://www.youtube.com/results?search_query={search_query}+quick+revision",
            "views": "456K views",
            "thumbnail": f"https://img.youtube.com/vi/dQw4w9WgXcQ/mqdefault.jpg",
        },
    ]
