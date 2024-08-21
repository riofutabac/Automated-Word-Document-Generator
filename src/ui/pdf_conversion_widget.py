# src/main.py (GUI)
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QListWidget, QFileDialog, QMessageBox, QProgressBar
from core.pdf_converter import PDFConverter
import os

class PDFConversionWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        self.load_files_btn = QPushButton("Cargar Archivos Word")
        self.convert_btn = QPushButton("Convertir a PDF")
        self.file_list = QListWidget()
        self.progress_bar = QProgressBar()

        layout.addWidget(self.load_files_btn)
        layout.addWidget(self.file_list)
        layout.addWidget(self.convert_btn)
        layout.addWidget(self.progress_bar)
        self.setLayout(layout)

        self.load_files_btn.clicked.connect(self.load_files)
        self.convert_btn.clicked.connect(self.convert_files)
        self.files_to_convert = []

    def load_files(self):
        files, _ = QFileDialog.getOpenFileNames(self, "Seleccionar Archivos Word", "", "Word Files (*.docx)")
        for file in files:
            if file.endswith('.docx'):
                self.files_to_convert.append(file)
                self.file_list.addItem(file)
            else:
                QMessageBox.warning(self, "Archivo no compatible", f"El archivo {file} no es un documento de Word y no se cargará.")

    def convert_files(self):
        if not self.files_to_convert:
            QMessageBox.warning(self, "Error", "No hay archivos para convertir.")
            return

        output_dir = QFileDialog.getExistingDirectory(self, "Seleccionar Carpeta de Destino")
        if not output_dir:
            return

        self.progress_bar.setValue(0)
        converter = PDFConverter(max_workers=4, retry_attempts=3)
        total_files = len(self.files_to_convert)

        def update_progress(index, total):
            progress_percentage = int((index / total) * 100)
            self.progress_bar.setValue(progress_percentage)

        try:
            converter.batch_convert_to_pdf(self.files_to_convert, output_dir, progress_callback=update_progress)
            QMessageBox.information(self, "Proceso Completo", "Archivos convertidos exitosamente.")
        except Exception as e:
            QMessageBox.critical(self, "Error Crítico", f"Ocurrió un error durante la conversión: {e}")