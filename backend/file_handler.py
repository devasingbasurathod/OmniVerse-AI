"""File upload, validation, and preview."""

from pathlib import Path

import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
UPLOADS_DIR = BASE_DIR / "uploads"
REPORTS_DIR = BASE_DIR / "reports"

ALLOWED_EXTENSIONS = {
    "csv": "csv",
    "xlsx": "excel",
    "xls": "excel",
    "pdf": "pdf",
    "png": "image",
    "jpg": "image",
    "jpeg": "image",
    "gif": "image",
    "webp": "image",
}


def ensure_dirs():
    """Create upload and report directories."""
    UPLOADS_DIR.mkdir(exist_ok=True)
    REPORTS_DIR.mkdir(exist_ok=True)


def get_file_type(filename):
    """Return file category from extension."""
    ext = Path(filename).suffix.lower().lstrip(".")
    return ALLOWED_EXTENSIONS.get(ext)


def is_allowed_file(filename):
    """Check if file extension is supported."""
    return get_file_type(filename) is not None


def save_uploaded_file(uploaded_file, user_id):
    """Save uploaded file to disk. Returns (path, file_type) or (None, error)."""
    ensure_dirs()
    if not is_allowed_file(uploaded_file.name):
        return None, "Unsupported file type."

    file_type = get_file_type(uploaded_file.name)
    safe_name = f"{user_id}_{uploaded_file.name}"
    file_path = UPLOADS_DIR / safe_name

    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    return str(file_path), file_type


def load_dataframe(file_path, file_type):
    """Load CSV or Excel into a DataFrame."""
    if file_type == "csv":
        return pd.read_csv(file_path)
    if file_type == "excel":
        return pd.read_excel(file_path)
    return None


def extract_pdf_text(file_path, max_pages=5):
    """Extract text from PDF (first few pages)."""
    try:
        from pypdf import PdfReader

        reader = PdfReader(file_path)
        pages = reader.pages[:max_pages]
        text = "\n".join(page.extract_text() or "" for page in pages)
        return text.strip() or "No readable text found in PDF."
    except Exception as exc:
        return f"Could not read PDF: {exc}"


def get_preview_data(file_path, file_type):
    """Return preview content based on file type."""
    if file_type in ("csv", "excel"):
        df = load_dataframe(file_path, file_type)
        return {"kind": "dataframe", "data": df}

    if file_type == "pdf":
        text = extract_pdf_text(file_path)
        return {"kind": "text", "data": text}

    if file_type == "image":
        return {"kind": "image", "data": file_path}

    return {"kind": "unknown", "data": None}
