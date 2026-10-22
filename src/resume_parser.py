import io
from typing import Tuple
from pypdf import PdfReader


def extract_text_from_pdf(pdf_file: io.BytesIO, max_size_mb: float = 5.0) -> Tuple[str, str]:
    """
    Extracts plain text from an uploaded PDF file stream.
    Validates file size and handles unreadable/scanned PDFs.
    
    Returns:
        Tuple[str, str]: (extracted_text, error_warning_message)
    """
    if pdf_file is None:
        return "", "No file provided."

    # Validate file size
    pdf_file.seek(0, io.SEEK_END)
    size_bytes = pdf_file.tell()
    pdf_file.seek(0)
    
    if size_bytes > max_size_mb * 1024 * 1024:
        return "", f"File size exceeds the {max_size_mb:.1f} MB limit."

    try:
        reader = PdfReader(pdf_file)
        if len(reader.pages) == 0:
            return "", "The uploaded PDF appears to have no pages."

        text_content = []
        for page in reader.pages:
            extracted = page.extract_text()
            if extracted:
                text_content.append(extracted)

        full_text = "\n".join(text_content).strip()

        if not full_text:
            return "", "No readable text found. If this is an image/scanned PDF, OCR processing is required."

        return full_text, ""

    except Exception as e:
        return "", f"Failed to parse PDF file: {str(e)}"
