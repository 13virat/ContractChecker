import fitz  # PyMuPDF
import pytesseract
from pdf2image import convert_from_bytes
from PIL import Image
import chardet
import docx
import io

def extract_from_txt(file):
    raw = file.read()
    encoding = chardet.detect(raw)['encoding']
    return raw.decode(encoding)

def extract_from_docx(file):
    doc = docx.Document(file)
    return "\n".join([p.text for p in doc.paragraphs])

def extract_from_pdf(file):
    try:
        file_bytes = file.read()
        doc = fitz.open(stream=file_bytes, filetype="pdf")
        full_text = ""

        for page in doc:
            txt = page.get_text()
            if txt.strip():
                full_text += txt
            else:
                pix = page.get_pixmap()
                img = Image.open(io.BytesIO(pix.tobytes()))
                full_text += pytesseract.image_to_string(img)
        doc.close()

        # OCR fallback if text too short
        if len(full_text.strip()) < 50:
            return extract_text_from_image_pdf(file_bytes)

        return full_text

    except Exception as e:
        return extract_text_from_image_pdf(file.read())

def extract_text_from_image_pdf(file_bytes):
    text = ""
    images = convert_from_bytes(file_bytes)
    for img in images:
        text += pytesseract.image_to_string(img) + "\n"
    return text
