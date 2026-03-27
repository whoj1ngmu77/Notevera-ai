"""
Notevera AI – PDF text extraction utility
"""


def extract_pdf_text(filepath: str) -> str:
    """Extract text from a PDF file."""
    try:
        from PyPDF2 import PdfReader
        reader = PdfReader(filepath)
        text_parts = []
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text_parts.append(page_text)
        return "\n\n".join(text_parts)
    except Exception as e:
        return f"[PDF extraction failed: {str(e)}]"
