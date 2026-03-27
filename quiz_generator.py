"""
Notevera AI – Quiz / Oral Exam Question Generator
Generates questions and evaluates answers using built-in logic.
"""
import re
import random
from typing import Dict, List


def generate_oral_questions(topic: str, context: str = "", num_questions: int = 5) -> List[Dict]:
    """Generate oral exam practice questions based on topic and context."""
    # Template-based question generation
    base_questions = [
        {
            "question": f"What is {topic}? Explain in your own words.",
            "expected_answer": f"{topic} is a concept that involves understanding its core principles, applications, and significance in the broader field of study.",
            "difficulty": "easy",
            "type": "define",
        },
        {
            "question": f"What are the key components or principles of {topic}?",
            "expected_answer": f"The key components of {topic} include its fundamental principles, main characteristics, and how they interrelate to form a complete understanding of the subject.",
            "difficulty": "medium",
            "type": "explain",
        },
        {
            "question": f"How would you explain {topic} to someone who has never heard of it?",
            "expected_answer": f"I would explain {topic} by starting with its basic definition, then providing real-world examples, and finally connecting it to concepts the person already understands.",
            "difficulty": "easy",
            "type": "simplify",
        },
        {
            "question": f"What are the real-world applications of {topic}?",
            "expected_answer": f"Real-world applications of {topic} include practical uses in industry, research, and everyday life, demonstrating its relevance and importance.",
            "difficulty": "medium",
            "type": "apply",
        },
        {
            "question": f"Compare and contrast the different aspects of {topic}.",
            "expected_answer": f"When comparing aspects of {topic}, we can examine the similarities and differences in approaches, methodologies, and outcomes, leading to a deeper understanding.",
            "difficulty": "hard",
            "type": "compare",
        },
        {
            "question": f"What challenges or limitations exist within {topic}?",
            "expected_answer": f"Key challenges in {topic} include limitations in current understanding, practical constraints, and areas where further research or development is needed.",
            "difficulty": "hard",
            "type": "analyze",
        },
        {
            "question": f"How does {topic} relate to other concepts you've studied?",
            "expected_answer": f"{topic} connects to related subjects through shared principles, complementary theories, and overlapping applications in the field.",
            "difficulty": "medium",
            "type": "connect",
        },
        {
            "question": f"If you were to teach a class on {topic}, what would your main points be?",
            "expected_answer": f"Main teaching points would cover: definition and background, core concepts, practical examples, hands-on exercises, and assessment of understanding.",
            "difficulty": "hard",
            "type": "synthesize",
        },
    ]

    # If we have context, try to generate more specific questions
    if context:
        sentences = [s.strip() for s in re.split(r'(?<=[.!?])\s+', context) if len(s.strip()) > 20]
        for s in sentences[:3]:
            # Create a question about this specific point
            base_questions.append({
                "question": f"Explain the following concept in detail: {s[:100]}",
                "expected_answer": s,
                "difficulty": "medium",
                "type": "explain",
            })

    random.shuffle(base_questions)
    return base_questions[:num_questions]


def evaluate_answer(question: str, answer: str, expected_answer: str = "") -> Dict:
    """Evaluate a student's answer against expected answer."""
    if not answer.strip():
        return {
            "score": 0,
            "confidence": 0,
            "feedback": "No answer was provided. Please try to answer the question.",
            "missing_points": ["The entire answer is missing"],
            "strengths": [],
        }

    answer_words = set(answer.lower().split())
    expected_words = set(expected_answer.lower().split()) if expected_answer else set()

    # Calculate basic similarity
    if expected_words:
        common = answer_words & expected_words
        stopwords = {'the', 'a', 'an', 'is', 'are', 'was', 'were', 'it', 'in', 'on', 'at',
                     'to', 'of', 'for', 'and', 'or', 'but', 'not', 'with', 'this', 'that',
                     'be', 'has', 'have', 'had', 'do', 'does', 'did', 'will', 'would', 'can',
                     'could', 'should', 'may', 'might', 'shall', 'from', 'by', 'as'}
        meaningful_common = common - stopwords
        meaningful_expected = expected_words - stopwords
        if meaningful_expected:
            overlap_ratio = len(meaningful_common) / len(meaningful_expected)
        else:
            overlap_ratio = 0.5
    else:
        overlap_ratio = 0.5  # No expected answer, give moderate score

    # Length bonus/penalty
    answer_len = len(answer.split())
    length_factor = 1.0
    if answer_len < 5:
        length_factor = 0.5
    elif answer_len < 10:
        length_factor = 0.7
    elif answer_len > 20:
        length_factor = 1.1
    elif answer_len > 50:
        length_factor = 1.2

    # Calculate score (0-100)
    raw_score = overlap_ratio * length_factor * 100
    score = min(max(int(raw_score), 5), 100)

    # Generate feedback
    strengths = []
    missing_points = []

    if score >= 70:
        strengths.append("Good understanding of the core concept")
        if answer_len > 20:
            strengths.append("Detailed and thorough response")
        if answer_len > 50:
            strengths.append("Excellent depth of explanation")
    elif score >= 40:
        strengths.append("Partial understanding demonstrated")
        missing_points.append("Try to provide more detailed explanations")
        missing_points.append("Include specific examples to support your answer")
    else:
        missing_points.append("The answer needs significant improvement")
        missing_points.append("Review the study notes on this topic")
        missing_points.append("Try to address the main points of the question")

    if expected_answer and expected_words:
        key_missed = (expected_words - stopwords - answer_words)
        for word in list(key_missed)[:3]:
            if len(word) > 4:
                missing_points.append(f"Consider mentioning: {word}")

    confidence = min(score + 10, 100) if score > 30 else score

    feedback_messages = {
        (80, 101): "Excellent answer! You have a strong grasp of this topic. 🌟",
        (60, 80): "Good answer! You covered most key points. Try adding more detail. 👍",
        (40, 60): "Decent attempt. You understand the basics but missed some important points. 📚",
        (20, 40): "This answer needs more work. Review your notes and try again. 💪",
        (0, 20): "This topic needs more study. Go through the notes carefully and practice again. 📖",
    }

    feedback = "Keep trying!"
    for (low, high), msg in feedback_messages.items():
        if low <= score < high:
            feedback = msg
            break

    return {
        "score": score,
        "confidence": confidence,
        "feedback": feedback,
        "strengths": strengths,
        "missing_points": missing_points,
    }
