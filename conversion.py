# Converting other file types (pdf, docx, csv, xlsx) to txt
import os
import io
import pandas
from PyPDF2 import PdfReader
from docx import Document

def extract_text(file):
    # Getting the extension type in a separate variable to convert depending on extension type
    extension = os.path.splitext(file.filename)[1].lower()

    if extension == ".txt":
        return file.read().decode("utf-8")

    elif extension == ".pdf":
        pdf = PdfReader(file)
        text = ""

        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"

        return text

    elif extension == "'.docx":
        doc = Document(file)
        #Return list of all paragraphs, loop through all paragraphs, extract text from each, make a list of strings
        #Join combines all paragraph strings into one string, seperated by newlines
        return "\n".join([para.text for para in doc.paragraphs])

    elif extension == ".csv":
        df = pandas.read_csv(file)
        return df.to_string()

    elif extension in [".xlsx", ".xls"]:
        df = pandas.read_excel(file)
        return df.to_string()

    else:
        raise ValueError(f"Unsupported file type: {extension}")