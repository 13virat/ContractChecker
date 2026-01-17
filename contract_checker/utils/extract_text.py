import fitz  # PyMuPDF
import chardet
import docx

def extract_from_txt(file):
    raw = file.read()
    encoding = chardet.detect(raw)['encoding'] or 'utf-8'
    return raw.decode(encoding, errors='ignore')


def extract_from_docx(file):
    doc = docx.Document(file)
    return "\n".join(p.text for p in doc.paragraphs)


def extract_from_pdf(file):
    text = ""
    file_bytes = file.read()

    with fitz.open(stream=file_bytes, filetype="pdf") as doc:
        for page in doc:
            text += page.get_text()

    return text.strip()
