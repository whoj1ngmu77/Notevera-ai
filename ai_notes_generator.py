"""
Notevera AI – AI Notes Generator (built-in, no external API needed)
Generates structured notes by analysing the text content.
"""
import re
from typing import Dict, List


def _extract_sentences(text: str) -> List[str]:
    """Split text into sentences."""
    sentences = re.split(r'(?<=[.!?])\s+', text.strip())
    return [s.strip() for s in sentences if len(s.strip()) > 10]


def _extract_key_terms(text: str) -> List[str]:
    """Extract potential key terms (capitalized phrases, repeated important words)."""
    # Find capitalized multi-word phrases
    phrases = re.findall(r'[A-Z][a-z]+(?:\s+[A-Z][a-z]+)+', text)
    # Find words that appear frequently (simplified)
    words = re.findall(r'\b[A-Za-z]{4,}\b', text.lower())
    word_freq = {}
    for w in words:
        word_freq[w] = word_freq.get(w, 0) + 1
    top_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:15]
    stopwords = {'this', 'that', 'with', 'from', 'have', 'been', 'were', 'they', 'their',
                 'will', 'would', 'could', 'should', 'about', 'which', 'when', 'what',
                 'some', 'other', 'more', 'also', 'than', 'then', 'these', 'those',
                 'into', 'only', 'very', 'such', 'each', 'most', 'both', 'between'}
    filtered = [w for w, c in top_words if w not in stopwords and c >= 2]
    unique_phrases = list(set(phrases))[:5]
    combined = unique_phrases + [w.title() for w in filtered[:8]]
    return combined[:10]


def _create_bullet_points(sentences: List[str]) -> List[str]:
    """Create bullet point summaries from sentences."""
    bullets = []
    for s in sentences[:15]:
        # Shorten long sentences
        if len(s) > 150:
            s = s[:147] + "..."
        bullets.append(s)
    return bullets


def _detect_definitions(text: str) -> List[Dict[str, str]]:
    """Try to detect definitions in the text."""
    definitions = []
    patterns = [
        r'([A-Z][a-zA-Z\s]+?)\s+(?:is defined as|is|refers to|means)\s+(.+?\.)',
        r'([A-Z][a-zA-Z\s]+?):\s+(.+?\.)',
    ]
    for pattern in patterns:
        matches = re.findall(pattern, text)
        for term, defn in matches[:8]:
            term = term.strip()
            defn = defn.strip()
            if len(term) > 3 and len(defn) > 10 and len(term) < 60:
                definitions.append({"term": term, "definition": defn})
    return definitions[:6]


def _detect_formulas(text: str) -> List[str]:
    """Detect mathematical formulas."""
    formulas = []
    patterns = [
        r'[A-Za-z]+\s*=\s*[A-Za-z0-9\s\+\-\*\/\(\)\^]+',
        r'(?:formula|equation):\s*(.+)',
    ]
    for pat in patterns:
        matches = re.findall(pat, text, re.IGNORECASE)
        formulas.extend([m.strip() for m in matches if len(m.strip()) > 3])
    return formulas[:5]


def _detect_topic(text: str, title: str) -> str:
    """Detect the main topic from the text."""
    if title and title not in ("Untitled", "Untitled Material", "Pasted Notes"):
        return title
    # Use first sentence as topic hint
    sentences = _extract_sentences(text)
    if sentences:
        first = sentences[0]
        if len(first) < 80:
            return first.rstrip(".")
        return first[:77].rstrip() + "..."
    return "General Study Notes"


def generate_structured_notes(text: str, title: str = "Untitled") -> Dict:
    """Generate structured study notes from extracted text."""
    sentences = _extract_sentences(text)
    key_terms = _extract_key_terms(text)
    topic = _detect_topic(text, title)

    # Create summary (first few sentences or condensed version)
    summary_sentences = sentences[:5]
    summary = " ".join(summary_sentences) if summary_sentences else text[:500]

    # Key concepts with explanations
    key_concepts = []
    for term in key_terms[:8]:
        # Find sentence containing this term
        explanation = ""
        for s in sentences:
            if term.lower() in s.lower():
                explanation = s
                break
        if not explanation:
            explanation = f"An important concept related to {topic}."
        key_concepts.append({"term": term, "explanation": explanation})

    # Bullet points
    bullet_points = _create_bullet_points(sentences)

    # Definitions
    definitions = _detect_definitions(text)

    # Formulas
    formulas = _detect_formulas(text)

    # Headings (from structure or generated)
    headings = [topic]
    for term in key_terms[:3]:
        headings.append(f"Understanding {term}")
    headings.append("Summary & Review")

    # Study tasks
    study_tasks = [
        f"Read and understand the core concept of {topic}",
        f"Review all {len(key_concepts)} key concepts thoroughly",
        "Create flashcards for all definitions",
        "Solve practice problems related to the topic",
        "Watch a recommended lecture for deeper understanding",
        "Attempt a self-quiz on the material",
        "Revise bullet point summaries before exam",
    ]

    return {
        "title": title if title not in ("Untitled", "Untitled Material") else topic,
        "topic": topic,
        "headings": headings,
        "summary": summary,
        "key_concepts": key_concepts,
        "bullet_points": bullet_points,
        "definitions": definitions,
        "formulas": formulas,
        "study_tasks": study_tasks,
        "recommended_lectures": [
            {
                "title": f"{topic} - Complete Lecture",
                "channel": "Academic Learning Hub",
                "url": f"https://www.youtube.com/results?search_query={topic.replace(' ', '+')}+lecture",
                "thumbnail": "",
            },
            {
                "title": f"{topic} Explained Simply",
                "channel": "Study With Me",
                "url": f"https://www.youtube.com/results?search_query={topic.replace(' ', '+')}+explained",
                "thumbnail": "",
            },
            {
                "title": f"{topic} - Quick Revision",
                "channel": "Exam Prep Pro",
                "url": f"https://www.youtube.com/results?search_query={topic.replace(' ', '+')}+revision",
                "thumbnail": "",
            },
        ],
    }
