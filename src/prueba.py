import sys
import os
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QVBoxLayout, QPushButton, QFileDialog, 
    QMessageBox, QListWidget, QProgressBar
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from docx2pdf import convert

class WordToPDFConverter(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Convertidor de Word a PDF")
        self.setGeometry(300, 300, 500, 400)

        # Layout principal
        self.layout = QVBoxLayout()

        # Etiqueta principal
        self.instruction_label = QLabel("Seleccione los archivos de Word para convertir", self)
        font = QFont("Arial", 14)
        self.instruction_label.setFont(font)
        self.instruction_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.instruction_label)

        # Lista para mostrar archivos seleccionados
        self.file_list_widget = QListWidget(self)
        self.layout.addWidget(self.file_list_widget)

        # Etiqueta para mostrar el total de archivos cargados
        self.total_files_label = QLabel("Total de archivos: 0", self)
        font = QFont("Arial", 12)
        self.total_files_label.setFont(font)
        self.total_files_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.total_files_label)

        # Barra de progreso
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setValue(0)
        self.layout.addWidget(self.progress_bar)

        # Botón para cargar archivos
        load_button = QPushButton("Cargar archivos", self)
        load_button.setStyleSheet("background-color: #4CAF50; color: white; font-size: 14px;")
        load_button.clicked.connect(self.load_files)
        self.layout.addWidget(load_button)

        # Botón para seleccionar la ubicación de guardado
        self.save_path_button = QPushButton("Seleccionar ubicación de guardado", self)
        self.save_path_button.setStyleSheet("background-color: #008CBA; color: white; font-size: 14px;")
        self.save_path_button.clicked.connect(self.select_save_directory)
        self.layout.addWidget(self.save_path_button)

        # Botón para convertir archivos
        convert_button = QPushButton("Convertir a PDF", self)
        convert_button.setStyleSheet("background-color: #f44336; color: white; font-size: 14px;")
        convert_button.clicked.connect(self.convert_to_pdf)
        self.layout.addWidget(convert_button)

        # Botón para limpiar la lista de archivos
        clear_button = QPushButton("Limpiar lista", self)
        clear_button.setStyleSheet("background-color: #ff9800; color: white; font-size: 14px;")
        clear_button.clicked.connect(self.clear_file_list)
        self.layout.addWidget(clear_button)

        self.setLayout(self.layout)
        self.input_files = []
        self.save_directory = ""

    def load_files(self):
        file_paths, _ = QFileDialog.getOpenFileNames(self, "Seleccionar archivos de Word", "", "Documentos Word (*.docx *.doc)")
        if file_paths:
            self.input_files.extend(file_paths)
            self.update_file_list_widget()

    def select_save_directory(self):
        self.save_directory = QFileDialog.getExistingDirectory(self, "Seleccionar ubicación de guardado")
        if self.save_directory:
            QMessageBox.information(self, "Ubicación seleccionada", f"Archivos PDF se guardarán en: {self.save_directory}")

    def update_file_list_widget(self):
        self.file_list_widget.clear()
        for file_path in self.input_files:
            self.file_list_widget.addItem(os.path.basename(file_path))
        self.total_files_label.setText(f"Total de archivos: {len(self.input_files)}")

    def clear_file_list(self):
        self.input_files = []
        self.file_list_widget.clear()
        self.total_files_label.setText("Total de archivos: 0")
        self.progress_bar.setValue(0)

    def convert_to_pdf(self):
        if not self.input_files:
            QMessageBox.warning(self, "No hay archivos", "Por favor, cargue al menos un archivo de Word para convertir.")
            return

        if not self.save_directory:
            QMessageBox.warning(self, "No hay ubicación de guardado", "Por favor, seleccione una ubicación para guardar los archivos PDF.")
            return

        total_files = len(self.input_files)
        for i, word_file_path in enumerate(self.input_files):
            pdf_file_name = os.path.splitext(os.path.basename(word_file_path))[0] + ".pdf"
            pdf_file_path = os.path.join(self.save_directory, pdf_file_name)
            convert(word_file_path, pdf_file_path)
            # Actualizar barra de progreso
            progress = int((i + 1) / total_files * 100)
            self.progress_bar.setValue(progress)

        QMessageBox.information(self, "Conversión completada", "Los archivos han sido convertidos exitosamente.")
        self.clear_file_list()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = WordToPDFConverter()
    ex.show()
    sys.exit(app.exec())
