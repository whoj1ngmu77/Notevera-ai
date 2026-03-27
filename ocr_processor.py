"""
Notevera AI – OCR text extraction from images
Falls back to a simple message if Tesseract is not installed.
"""


def extract_image_text(filepath: str) -> str:
    """Extract text from an image using OCR."""
    try:
        import pytesseract
        from PIL import Image
        image = Image.open(filepath)
        text = pytesseract.image_to_string(image)
        return text.strip() if text.strip() else "[No text detected in image]"
    except ImportError:
        return "[OCR requires pytesseract and Tesseract to be installed. Please install them or paste the text manually.]"
    except Exception as e:
        return f"[OCR failed: {str(e)}. Please paste the text manually.]"
