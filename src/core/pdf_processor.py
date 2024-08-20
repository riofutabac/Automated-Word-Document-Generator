import os
from PyPDF2 import PdfMerger, PdfReader
from PyPDF2.errors import EmptyFileError
from PyQt6.QtWidgets import QMessageBox

class PDFProcessor:
    def __init__(self, max_workers=4):
        self.max_workers = max_workers

    def batch_process_pdfs(self, files_to_process, output_dir, progress_callback=None):
        merger = PdfMerger()
        empty_files = []
        processed_files = []
        for i, file_path in enumerate(files_to_process):
            try:
                # Validar que el archivo no esté vacío
                with open(file_path, "rb") as file:
                    reader = PdfReader(file)
                    if len(reader.pages) == 0:
                        raise EmptyFileError(f"El archivo {file_path} está vacío y no se puede procesar.")
                # Si no hay error, agregar el archivo al merger
                merger.append(file_path)
                processed_files.append(file_path)
            except EmptyFileError as e:
                empty_files.append(file_path)
                continue  # Saltar este archivo y continuar con los demás
            except Exception as e:
                print(f"Error al procesar el archivo {file_path}: {e}")
                continue

            if progress_callback:
                progress_callback(i + 1, len(files_to_process))

        if not processed_files:
            return [], empty_files

        output_file_path = os.path.join(output_dir, "merged_pdf.pdf")
        with open(output_file_path, "wb") as output_file:
            merger.write(output_file)
        
        return processed_files, empty_files