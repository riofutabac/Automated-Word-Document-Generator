from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QListWidget, QFileDialog, 
    QMessageBox, QProgressBar, QLabel, QHBoxLayout
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from core.pdf_processor import PDFProcessor  # Aquí está la clase del core
import os

class PDFProcessingWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        # Configuración de la ventana principal
        self.setWindowTitle("Procesador de Archivos PDF")
        self.setGeometry(300, 300, 600, 400)

        # Layout principal
        layout = QVBoxLayout()

        # Título principal
        title_label = QLabel("Procesador de Archivos PDF")
        title_label.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)

        # Botones en la parte superior
        button_layout = QHBoxLayout()

        self.load_files_btn = QPushButton("Cargar Archivos PDF")
        self.load_files_btn.setStyleSheet("background-color: #4CAF50; color: white; font-size: 14px;")
        button_layout.addWidget(self.load_files_btn)

        self.clear_list_btn = QPushButton("Limpiar Lista")
        self.clear_list_btn.setStyleSheet("background-color: #ff9800; color: white; font-size: 14px;")
        button_layout.addWidget(self.clear_list_btn)

        layout.addLayout(button_layout)

        # Lista de archivos
        self.file_list = QListWidget()
        layout.addWidget(self.file_list)

        # Barra de progreso
        self.progress_bar = QProgressBar()
        layout.addWidget(self.progress_bar)

        # Botón para procesar archivos
        self.process_btn = QPushButton("Procesar Archivos PDF")
        self.process_btn.setStyleSheet("background-color: #f44336; color: white; font-size: 14px;")
        layout.addWidget(self.process_btn)

        # Configurar el layout
        self.setLayout(layout)

        # Conexión de botones con funciones
        self.load_files_btn.clicked.connect(self.load_files)
        self.clear_list_btn.clicked.connect(self.clear_file_list)
        self.process_btn.clicked.connect(self.process_files)

        self.files_to_process = []

    def load_files(self):
        files, _ = QFileDialog.getOpenFileNames(self, "Seleccionar Archivos PDF", "", "PDF Files (*.pdf)")
        for file in files:
            if file.endswith('.pdf'):
                self.files_to_process.append(file)
                self.file_list.addItem(os.path.basename(file))
            else:
                QMessageBox.warning(self, "Archivo no compatible", f"El archivo {file} no es un documento PDF y no se cargará.")

    def clear_file_list(self):
        self.files_to_process = []
        self.file_list.clear()
        self.progress_bar.setValue(0)

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
