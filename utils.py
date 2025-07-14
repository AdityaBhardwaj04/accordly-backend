# utils.py
import os
from docx import Document
from PyPDF2 import PdfReader

def extract_text_from_file(file_path: str) -> str:
    ext = os.path.splitext(file_path)[1].lower()

    if ext == ".txt":
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()

    elif ext == ".docx":
        doc = Document(file_path)
        return "\n".join([p.text for p in doc.paragraphs])

    elif ext == ".pdf":
        reader = PdfReader(file_path)
        return "\n".join([page.extract_text() or "" for page in reader.pages])

    else:
        raise ValueError(f"Unsupported file format: {ext}")
