#ui.mainwidnows
from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QPushButton, QWidget, QMessageBox, QDateTimeEdit, QLabel, QHBoxLayout, QLineEdit
from PyQt6.QtCore import QDateTime
from ui.file_loader import load_word_file, load_excel_file, select_output_directory
from core.document_generator import DocumentGenerator
from core.excel_parser import ExcelParser
from core.word_parser import WordParser
from utils.date_utils import increment_datetime, format_datetime
from utils.file_utils import create_output_directory, generate_output_filename
from ui.progress_dialog import ProgressDialog
import os
from datetime import datetime

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Generador de Documentos")
        self.setGeometry(100, 100, 600, 400)

        self.word_template_path = ""
        self.excel_file_path = ""

        layout = QVBoxLayout()
        
        self.load_word_btn = QPushButton("Cargar Plantilla Word")
        self.load_excel_btn = QPushButton("Cargar Archivo Excel")
        self.generate_btn = QPushButton("Generar Documentos")

        layout.addWidget(self.load_word_btn)
        layout.addWidget(self.load_excel_btn)
        layout.addWidget(self.generate_btn)

        datetime_layout = QHBoxLayout()
        self.datetime_edit = QDateTimeEdit(QDateTime.currentDateTime())
        self.datetime_edit.setDisplayFormat("dd/MM/yyyy HH:mm")
        datetime_layout.addWidget(QLabel("Fecha y hora inicial:"))
        datetime_layout.addWidget(self.datetime_edit)
        layout.addLayout(datetime_layout)

        self.filename_format = QLineEdit("documento_{{nombre}}")
        layout.addWidget(QLabel("Formato de nombre de archivo:"))
        layout.addWidget(self.filename_format)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.load_word_btn.clicked.connect(self.load_word_template)
        self.load_excel_btn.clicked.connect(self.load_excel_file)
        self.generate_btn.clicked.connect(self.generate_documents)

    def load_word_template(self):
        self.word_template_path = load_word_file(self)
        if self.word_template_path:
            QMessageBox.information(self, "Plantilla Cargada", f"Plantilla Word cargada: {self.word_template_path}")

    def load_excel_file(self):
        self.excel_file_path = load_excel_file(self)
        if self.excel_file_path:
            QMessageBox.information(self, "Archivo Cargado", f"Archivo Excel cargado: {self.excel_file_path}")

    def generate_documents(self):
        if not self.word_template_path or not self.excel_file_path:
            QMessageBox.warning(self, "Error", "Por favor, carga una plantilla Word y un archivo Excel antes de continuar.")
            return

        output_dir = select_output_directory(self)
        if not output_dir:
            return

        create_output_directory(output_dir)

        word_parser = WordParser(self.word_template_path)
        placeholders = word_parser.get_placeholders()

        excel_parser = ExcelParser(self.excel_file_path)
        missing_columns = excel_parser.validate_columns(placeholders)
        
        if missing_columns:
            QMessageBox.warning(self, "Columnas faltantes", f"Las siguientes columnas no están en el Excel: {', '.join(missing_columns)}")
            return

        data_list = excel_parser.get_data()
        doc_generator = DocumentGenerator(self.word_template_path)
        
        progress_dialog = ProgressDialog(self)
        progress_dialog.setRange(0, len(data_list))
        progress_dialog.show()

        start_datetime = self.datetime_edit.dateTime().toPython()
        
        try:
            for index, data in enumerate(data_list):
                data['fecha'] = format_datetime(start_datetime)
                output_path = os.path.join(output_dir, generate_output_filename(self.filename_format.text().format(**data), index + 1))
                doc = doc_generator.generate_document(data)
                doc_generator.save_document(doc, output_path)
                start_datetime = increment_datetime(start_datetime, 1)
                progress_dialog.update_progress(index + 1)
            QMessageBox.information(self, "Proceso Completo", f"Se generaron {len(data_list)} documentos exitosamente en {output_dir}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Ocurrió un error durante la generación de documentos: {str(e)}")
        finally:
            progress_dialog.close()
