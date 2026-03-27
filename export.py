"""
Notevera AI – PDF export routes
"""
import json
import io
from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import StreamingResponse
from database import database
from models.tables import notes
from routes.auth import get_current_user
from fpdf import FPDF

router = APIRouter(prefix="/export", tags=["Export"])


class NotesPDF(FPDF):
    def header(self):
        self.set_font("Helvetica", "B", 14)
        self.set_text_color(106, 27, 154)
        self.cell(0, 10, "Notevera AI - Study Notes", ln=True, align="C")
        self.ln(4)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, f"Page {self.page_no()}/{{nb}}", align="C")


@router.get("/notes/{note_id}/pdf")
async def export_note_pdf(note_id: int, current_user=Depends(get_current_user)):
    row = await database.fetch_one(
        notes.select().where(
            (notes.c.id == note_id) & (notes.c.user_id == current_user["id"])
        )
    )
    if not row:
        raise HTTPException(status_code=404, detail="Note not found")

    m = dict(row._mapping)
    try:
        content = json.loads(m["content"])
    except Exception:
        content = {"title": m["title"], "summary": m["content"]}

    pdf = NotesPDF()
    pdf.alias_nb_pages()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=20)

    # Title
    pdf.set_font("Helvetica", "B", 20)
    pdf.set_text_color(44, 0, 100)
    title = content.get("title", "Untitled")
    pdf.cell(0, 12, title.encode('latin-1', 'replace').decode('latin-1'), ln=True)
    pdf.ln(3)

    # Topic
    if content.get("topic"):
        pdf.set_font("Helvetica", "I", 12)
        pdf.set_text_color(100, 100, 100)
        topic = content["topic"]
        pdf.cell(0, 8, f"Topic: {topic}".encode('latin-1', 'replace').decode('latin-1'), ln=True)
        pdf.ln(3)

    # Summary
    if content.get("summary"):
        pdf.set_font("Helvetica", "B", 13)
        pdf.set_text_color(44, 0, 100)
        pdf.cell(0, 8, "Summary", ln=True)
        pdf.set_font("Helvetica", "", 11)
        pdf.set_text_color(50, 50, 50)
        summary = content["summary"]
        pdf.multi_cell(0, 6, summary.encode('latin-1', 'replace').decode('latin-1'))
        pdf.ln(4)

    # Key Concepts
    concepts = content.get("key_concepts", [])
    if concepts:
        pdf.set_font("Helvetica", "B", 13)
        pdf.set_text_color(44, 0, 100)
        pdf.cell(0, 8, "Key Concepts", ln=True)
        pdf.ln(2)
        for c in concepts:
            pdf.set_font("Helvetica", "B", 11)
            pdf.set_text_color(75, 0, 130)
            term = c.get("term", "")
            pdf.cell(0, 7, f"  * {term}".encode('latin-1', 'replace').decode('latin-1'), ln=True)
            pdf.set_font("Helvetica", "", 10)
            pdf.set_text_color(50, 50, 50)
            explanation = c.get("explanation", "")
            pdf.multi_cell(0, 5, f"    {explanation}".encode('latin-1', 'replace').decode('latin-1'))
            pdf.ln(2)

    # Definitions
    definitions = content.get("definitions", [])
    if definitions:
        pdf.set_font("Helvetica", "B", 13)
        pdf.set_text_color(44, 0, 100)
        pdf.cell(0, 8, "Definitions", ln=True)
        pdf.ln(2)
        for d in definitions:
            pdf.set_font("Helvetica", "B", 11)
            pdf.set_text_color(75, 0, 130)
            term = d.get("term", "")
            pdf.cell(0, 7, f"  {term}:".encode('latin-1', 'replace').decode('latin-1'), ln=True)
            pdf.set_font("Helvetica", "", 10)
            pdf.set_text_color(50, 50, 50)
            defn = d.get("definition", "")
            pdf.multi_cell(0, 5, f"    {defn}".encode('latin-1', 'replace').decode('latin-1'))
            pdf.ln(2)

    # Formulas
    formulas = content.get("formulas", [])
    if formulas:
        pdf.set_font("Helvetica", "B", 13)
        pdf.set_text_color(44, 0, 100)
        pdf.cell(0, 8, "Formulas", ln=True)
        pdf.ln(2)
        for f in formulas:
            pdf.set_font("Helvetica", "", 11)
            pdf.set_text_color(50, 50, 50)
            pdf.cell(0, 7, f"  * {f}".encode('latin-1', 'replace').decode('latin-1'), ln=True)

    # Bullet Points
    bullets = content.get("bullet_points", [])
    if bullets:
        pdf.ln(3)
        pdf.set_font("Helvetica", "B", 13)
        pdf.set_text_color(44, 0, 100)
        pdf.cell(0, 8, "Key Points", ln=True)
        pdf.ln(2)
        pdf.set_font("Helvetica", "", 10)
        pdf.set_text_color(50, 50, 50)
        for b in bullets:
            pdf.multi_cell(0, 5, f"  - {b}".encode('latin-1', 'replace').decode('latin-1'))

    # Study Tasks
    study_tasks = content.get("study_tasks", [])
    if study_tasks:
        pdf.ln(3)
        pdf.set_font("Helvetica", "B", 13)
        pdf.set_text_color(44, 0, 100)
        pdf.cell(0, 8, "Recommended Study Tasks", ln=True)
        pdf.ln(2)
        pdf.set_font("Helvetica", "", 10)
        pdf.set_text_color(50, 50, 50)
        for idx, t in enumerate(study_tasks, 1):
            pdf.cell(0, 7, f"  {idx}. {t}".encode('latin-1', 'replace').decode('latin-1'), ln=True)

    buf = io.BytesIO()
    pdf_bytes = pdf.output()
    buf.write(pdf_bytes)
    buf.seek(0)

    safe_title = "".join(c for c in title if c.isalnum() or c in " _-").strip().replace(" ", "_")
    return StreamingResponse(
        buf,
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="Notevera_{safe_title}.pdf"'},
    )
