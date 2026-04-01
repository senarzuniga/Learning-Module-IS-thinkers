"""
File handler — extracts text content from uploaded PDF and TXT files.
"""

import io
from typing import Optional

MAX_CHARS = 15000  # Limit file content to avoid exceeding token limits


def extract_file_content(file_bytes: bytes, filename: str) -> Optional[str]:
    """
    Extract text content from an uploaded file.

    Supports PDF and TXT file formats.

    Args:
        file_bytes: Raw bytes of the uploaded file.
        filename: Original filename (used to determine file type).

    Returns:
        Extracted text content as a string, or None if extraction fails.

    Raises:
        ValueError: If the file type is not supported.
    """
    filename_lower = filename.lower()

    if filename_lower.endswith(".txt"):
        return _extract_txt(file_bytes)
    elif filename_lower.endswith(".pdf"):
        return _extract_pdf(file_bytes)
    else:
        raise ValueError(
            f"Unsupported file type: '{filename}'. "
            "Please upload a PDF or TXT file."
        )


def _extract_txt(file_bytes: bytes) -> str:
    """Extract text from a plain text file."""
    try:
        text = file_bytes.decode("utf-8")
    except UnicodeDecodeError:
        text = file_bytes.decode("latin-1", errors="replace")

    return _truncate(text)


def _extract_pdf(file_bytes: bytes) -> str:
    """Extract text from a PDF file using pypdf."""
    try:
        import pypdf
    except ImportError:
        raise ImportError(
            "pypdf is required to process PDF files. "
            "Install it with: pip install pypdf"
        )

    reader = pypdf.PdfReader(io.BytesIO(file_bytes))
    pages_text = []

    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            pages_text.append(page_text)

    full_text = "\n\n".join(pages_text)

    if not full_text.strip():
        return "[PDF contained no extractable text — it may be image-based.]"

    return _truncate(full_text)


def _truncate(text: str) -> str:
    """Truncate text to the maximum allowed character count."""
    if len(text) > MAX_CHARS:
        truncated = text[:MAX_CHARS]
        return truncated + f"\n\n[Content truncated at {MAX_CHARS:,} characters]"
    return text
