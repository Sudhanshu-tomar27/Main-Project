from docx import Document
import os


SAVE_FOLDER = "saved_files"

os.makedirs(
    SAVE_FOLDER,
    exist_ok=True
)


def create_docx(text, filename):

    if not filename.endswith(".docx"):
        filename += ".docx"


    path = os.path.join(
        SAVE_FOLDER,
        filename
    )


    doc = Document()


    doc.add_heading(
        "AI Generated Document",
        level=1
    )


    doc.add_paragraph(
        text
    )


    doc.save(path)


    return path