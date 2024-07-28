from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QPushButton, QWidget, QMessageBox, QDateTimeEdit, QLabel, QHBoxLayout, QLineEdit, QComboBox, QDialog
from PyQt6.QtCore import QDateTime
from ui.file_loader import load_word_file, load_excel_file, select_output_directory
from core.document_generator import DocumentGenerator
from core.excel_parser import ExcelParser
from core.word_parser import WordParser
from utils.date_utils import increment_datetime, format_datetime
from utils.file_utils import create_output_directory, generate_output_filename
from ui.progress_dialog import ProgressDialog
from ui.missing_columns_dialog import MissingColumnsDialog
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

        self.column_selector = QComboBox()
        layout.addWidget(QLabel("Seleccionar columna para nombre de archivo:"))
        layout.addWidget(self.column_selector)

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
            self.update_column_selector()

    def update_column_selector(self):
        excel_parser = ExcelParser(self.excel_file_path)
        columns = excel_parser.get_columns()
        self.column_selector.clear()
        self.column_selector.addItem("Por defecto (documento_1, documento_2, ...)")
        self.column_selector.addItems(columns)

    # ui/main_windows.py


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
        
        static_values = {}
        increment_columns = set()

        if missing_columns:
            dialog = MissingColumnsDialog(missing_columns, self)
            if dialog.exec() == QDialog.DialogCode.Accepted:
                values = dialog.get_values()
                for column, (value, increment) in values.items():
                    static_values[column] = value
                    if increment:
                        increment_columns.add(column)
            else:
                return  # User cancelled the operation

        data_list = excel_parser.get_data()
        doc_generator = DocumentGenerator(self.word_template_path)
        
        progress_dialog = ProgressDialog(self)
        progress_dialog.setRange(0, len(data_list))
        progress_dialog.show()

        start_datetime = self.datetime_edit.dateTime().toPyDateTime()
        selected_column = self.column_selector.currentText()

        try:
            for index, row_data in enumerate(data_list):
                # Crear una copia de los datos de la fila para no modificar el original
                data = row_data.copy()
                
                # Agregar valores estáticos y manejar incrementos
                for column, value in static_values.items():
                    if column in increment_columns:
                        try:
                            data[column] = str(int(value) + index)
                        except ValueError:
                            data[column] = value
                    else:
                        data[column] = value

                # Agregar fecha
                data['fecha'] = format_datetime(start_datetime)
                
                # Generar nombre de archivo
                if selected_column == "Por defecto (documento_1, documento_2, ...)":
                    output_filename = f"documento_{index + 1}"
                else:
                    output_filename = self.filename_format.text().replace("{{columna}}", str(data.get(selected_column, "")))
                
                output_path = os.path.join(output_dir, generate_output_filename(output_filename, index + 1))
                
                # Generar y guardar el documento
                doc = doc_generator.generate_document(data)
                doc_generator.save_document(doc, output_path)
                
                # Incrementar la fecha para el siguiente documento
                start_datetime = increment_datetime(start_datetime, 1)
                
                # Actualizar la barra de progreso
                progress_dialog.update_progress(index + 1)
            
            QMessageBox.information(self, "Proceso Completo", f"Se generaron {len(data_list)} documentos exitosamente en {output_dir}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Ocurrió un error durante la generación de documentos: {str(e)}")
        finally:
            progress_dialog.close()
