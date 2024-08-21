import os
from docx2pdf import convert

class PDFConverter:
    def convert_to_pdf(self, input_file, output_file):
        if not os.path.exists(input_file):
            raise FileNotFoundError(f"El archivo {input_file} no existe.")
        convert(input_file, output_file)
