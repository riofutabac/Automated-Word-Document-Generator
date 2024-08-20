# core/pdf_converter.py
import concurrent.futures
import os
from docx2pdf import convert

class PDFConverter:
    def __init__(self, max_workers=4):
        self.max_workers = max_workers

    def convert_file(self, input_file, output_file):
        try:
            convert(input_file, output_file)
        except Exception as e:
            print(f"Error al convertir {input_file} a PDF: {e}")

    def batch_convert_to_pdf(self, input_files, output_dir, progress_callback=None):
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = []
            for i, input_file in enumerate(input_files):
                output_file = os.path.join(output_dir, os.path.splitext(os.path.basename(input_file))[0] + ".pdf")
                futures.append(executor.submit(self.convert_file, input_file, output_file))
                if progress_callback:
                    progress_callback(i + 1, len(input_files))

            for future in concurrent.futures.as_completed(futures):
                try:
                    future.result()
                except Exception as e:
                    print(f"Error en la conversión: {e}")
