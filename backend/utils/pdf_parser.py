# === Begin File: backend/utils/pdf_parser.py ===
import fitz  # PyMuPDF

def extract_text_from_pdf(file_path: str) -> str:
    """
    Extracts all text from a PDF file using PyMuPDF.
    """
    text = ""
    with fitz.open(file_path) as doc:
        for page in doc:
            text += page.get_text()
    return text.strip()
# === End File: backend/utils/pdf_parser.py ===