# core/pdf_converter.py
import concurrent.futures
import os
from docx2pdf import convert
from time import sleep

class PDFConverter:
    def __init__(self, max_workers=4, retry_attempts=3):
        self.max_workers = max_workers
        self.retry_attempts = retry_attempts

    def convert_file(self, input_file, output_file):
        for attempt in range(self.retry_attempts):
            try:
                convert(input_file, output_file)
                return  # Si tiene éxito, salir del bucle
            except Exception as e:
                print(f"Intento {attempt + 1}/{self.retry_attempts} fallido al convertir {input_file} a PDF: {e}")
                sleep(1)  # Esperar un momento antes de reintentar
        # Si todos los intentos fallan, lanzar una excepción
        raise Exception(f"Error definitivo al convertir {input_file} a PDF después de {self.retry_attempts} intentos.")

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
                    raise e  # Elevar la excepción para manejo en nivel superior
                