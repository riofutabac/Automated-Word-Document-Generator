# ui/mainwindow.py

from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QPushButton, QWidget, QMessageBox, QLineEdit, QComboBox, QDialog, QLabel, QCheckBox
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

        self.filename_format = QLineEdit("documento_{{nombre}}")
        layout.addWidget(QLabel("Formato de nombre de archivo:"))
        layout.addWidget(self.filename_format)

        self.column_selector = QComboBox()
        layout.addWidget(QLabel("Seleccionar columna para nombre de archivo:"))
        layout.addWidget(self.column_selector)
        
        self.enumerate_checkbox = QCheckBox("Incluir enumeración al final del nombre del archivo")
        self.enumerate_checkbox.setChecked(True)
        layout.addWidget(self.enumerate_checkbox)

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
        minute_columns = set()
        hour_columns = set()

        start_datetime = datetime.now()
        use_current_time = True

        if missing_columns:
            dialog = MissingColumnsDialog(missing_columns, self)
            if dialog.exec() == QDialog.DialogCode.Accepted:
                values, use_current_time, start_datetime = dialog.get_values()
                for column, (value, increment, is_minute, is_hour) in values.items():
                    static_values[column] = value
                    if increment:
                        increment_columns.add(column)
                    if is_minute:
                        minute_columns.add(column)
                    if is_hour:
                        hour_columns.add(column)
            else:
                return  # User cancelled the operation

        data_list = excel_parser.get_data()
        doc_generator = DocumentGenerator(self.word_template_path)
        
        progress_dialog = ProgressDialog(self)
        progress_dialog.setRange(0, len(data_list))
        progress_dialog.show()

        selected_column = self.column_selector.currentText()
        include_enumeration = self.enumerate_checkbox.isChecked()

        try:
            for index, data in enumerate(data_list):
                for column, value in static_values.items():
                    if column in increment_columns:
                        try:
                            data[column] = str(int(value) + index)
                        except ValueError:
                            data[column] = value
                    else:
                        data[column] = value

                if use_current_time:
                    current_datetime = datetime.now()
                    data['fecha'] = format_datetime(current_datetime)
                    data['hora'] = current_datetime.hour
                    data['minuto'] = current_datetime.minute
                else:
                    data['fecha'] = format_datetime(start_datetime)
                    data['hora'] = start_datetime.hour
                    data['minuto'] = start_datetime.minute

                for column in minute_columns:
                    if column in data:
                        minute_value = int(data[column])
                        if minute_value >= 60:
                            hour_increment = minute_value // 60
                            minute_value = minute_value % 60
                            start_datetime = increment_datetime(start_datetime, hour_increment * 60)
                        data[column] = str(minute_value)

                for column in hour_columns:
                    if column in data:
                        hour_value = int(data[column])
                        if hour_value >= 24:
                            day_increment = hour_value // 24
                            hour_value = hour_value % 24
                            start_datetime = increment_datetime(start_datetime, day_increment * 1440)
                        data[column] = str(hour_value)

                output_filename = self.filename_format.text()
                for key, value in data.items():
                    placeholder = f"{{{{{key}}}}}"
                    if placeholder in output_filename:
                        output_filename = output_filename.replace(placeholder, str(value).replace(" ", "_"))

                if include_enumeration:
                    output_filename = generate_output_filename(output_filename, index + 1)
                else:
                    output_filename = f"{output_filename}.docx"

                output_path = os.path.join(output_dir, output_filename)
                
                doc = doc_generator.generate_document(data)
                doc_generator.save_document(doc, output_path)
                start_datetime = increment_datetime(start_datetime, 1)
                progress_dialog.update_progress(index + 1)
            QMessageBox.information(self, "Proceso Completo", f"Se generaron {len(data_list)} documentos exitosamente en {output_dir}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Ocurrió un error durante la generación de documentos: {str(e)}")
        finally:
            progress_dialog.close()
