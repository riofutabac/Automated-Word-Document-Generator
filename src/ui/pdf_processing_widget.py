from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QListWidget, QFileDialog, QMessageBox, QProgressBar
from core.pdf_processor import PDFProcessor  # Aquí está la clase del core
import os

class PDFProcessingWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        self.load_files_btn = QPushButton("Cargar Archivos PDF")
        self.process_btn = QPushButton("Procesar Archivos PDF")
        self.file_list = QListWidget()
        self.progress_bar = QProgressBar()

        layout.addWidget(self.load_files_btn)
        layout.addWidget(self.file_list)
        layout.addWidget(self.process_btn)
        layout.addWidget(self.progress_bar)
        self.setLayout(layout)

        self.load_files_btn.clicked.connect(self.load_files)
        self.process_btn.clicked.connect(self.process_files)
        self.files_to_process = []

    def load_files(self):
        files, _ = QFileDialog.getOpenFileNames(self, "Seleccionar Archivos PDF", "", "PDF Files (*.pdf)")
        for file in files:
            if file.endswith('.pdf'):
                self.files_to_process.append(file)
                self.file_list.addItem(file)
            else:
                QMessageBox.warning(self, "Archivo no compatible", f"El archivo {file} no es un documento PDF y no se cargará.")

    def process_files(self):
        if not self.files_to_process:
            QMessageBox.warning(self, "Error", "No hay archivos para procesar.")
            return

        output_dir = QFileDialog.getExistingDirectory(self, "Seleccionar Carpeta de Destino")
        if not output_dir:
            return

        self.progress_bar.setValue(0)
        processor = PDFProcessor(max_workers=4)
        total_files = len(self.files_to_process)

        def update_progress(index, total):
            progress_percentage = int((index / total) * 100)
            self.progress_bar.setValue(progress_percentage)

        processed_files, empty_files = processor.batch_process_pdfs(self.files_to_process, output_dir, progress_callback=update_progress)

        if empty_files:
            QMessageBox.warning(self, "Archivos Vacíos", f"Los siguientes archivos están vacíos y fueron omitidos:\n" + "\n".join(empty_files))

        if processed_files:
            QMessageBox.information(self, "Proceso Completo", "Archivos procesados exitosamente.")
        else:
            QMessageBox.warning(self, "Error", "No se pudieron procesar los archivos.")
