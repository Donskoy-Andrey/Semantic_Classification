import io
from striprtf.striprtf import rtf_to_text
from PyPDF2 import PdfReader
import pandas as pd
import docx2txt


class ParserFile:
    @staticmethod
    def read_txt(file):
        contents = file.file.read()
        return contents.decode('utf-8')

    @staticmethod
    def read_rtf(file):
        contents = file.file.read()
        text_rtf = contents.decode('UTF-8')
        extracted_text = rtf_to_text(text_rtf)
        return extracted_text

    @staticmethod
    def read_pdf(file):
        contents = file.file.read()
        pdf_reader = PdfReader(io.BytesIO(contents))
        extracted_text = ''
        for page in pdf_reader.pages:
            extracted_text += page.extract_text()
        return extracted_text

    @staticmethod
    def read_xlsx(file):
        contents = file.file.read()
        extracted_text = pd.read_excel(
            io.BytesIO(contents)
        ).fillna(" ").to_string()
        return extracted_text

    @staticmethod
    def read_docx(file):
        contents = file.file.read()
        extracted_text = docx2txt.process(
            io.BytesIO(contents)
        )
        return extracted_text
