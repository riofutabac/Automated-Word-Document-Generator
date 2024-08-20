from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QPushButton, QWidget, QMessageBox, QLineEdit, QComboBox, QDialog, QLabel, QCheckBox, QHBoxLayout, QStackedWidget, QMenuBar, QMenu
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
from ui.pdf_conversion_widget import PDFConversionWidget  # Importa tu widget de conversión de PDF
from ui.pdf_processing_widget import PDFProcessingWidget  # Importa correctamente tu widget de unir PDFs


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Generador de Documentos")
        self.setGeometry(100, 100, 600, 400)

        # Crear el menú de la barra de menús
        menubar = self.menuBar()
        main_menu = menubar.addMenu("Menú Principal")
        welcome_action = main_menu.addAction("Bienvenida")
        main_functionality_action = main_menu.addAction("Generador de Documentos")

        pdf_conversion_action = main_menu.addAction("Conversión a PDF")
        pdf_merge_action = main_menu.addAction("Unir PDFs")

        # Conectar las acciones del menú a las funciones correspondientes
        welcome_action.triggered.connect(self.show_welcome_screen)
        main_functionality_action.triggered.connect(self.show_main_functionality)

        pdf_conversion_action.triggered.connect(self.show_pdf_conversion)
        pdf_merge_action.triggered.connect(self.show_pdf_merge)

        # Crear el QStackedWidget para gestionar las diferentes pantallas
        self.stacked_widget = QStackedWidget()

        # Crear las diferentes pantallas
        self.welcome_screen = self.create_welcome_screen()
        self.main_functionality_screen = self.create_main_functionality_screen()
      
        self.pdf_conversion_screen = PDFConversionWidget()
        self.pdf_merge_screen = PDFProcessingWidget()  # Crear instancia del widget de unir PDFs

        # Añadir las pantallas al QStackedWidget
        self.stacked_widget.addWidget(self.welcome_screen)
        self.stacked_widget.addWidget(self.pdf_conversion_screen)
        self.stacked_widget.addWidget(self.pdf_merge_screen)
        self.stacked_widget.addWidget(self.main_functionality_screen)

        # Configurar la pantalla de bienvenida como la inicial
        self.setCentralWidget(self.stacked_widget)
        self.stacked_widget.setCurrentWidget(self.welcome_screen)
        

    def create_welcome_screen(self):
        widget = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Bienvenido al Generador de Documentos"))
        widget.setLayout(layout)
        return widget

    def create_main_functionality_screen(self):
        widget = QWidget()
        layout = QVBoxLayout()

        # Botones de carga
        self.load_word_btn = QPushButton("Cargar Plantilla Word")
        self.load_excel_btn = QPushButton("Cargar Archivo Excel")
        self.generate_btn = QPushButton("Generar Documentos")

        layout.addWidget(self.load_word_btn)
        layout.addWidget(self.load_excel_btn)

        # Mostrar nombres de archivos cargados
        self.word_file_label = QLabel("")
        self.excel_file_label = QLabel("")
        layout.addWidget(self.word_file_label)
        layout.addWidget(self.excel_file_label)

        # Formato de nombre de archivo
        self.filename_format = QLineEdit("documento")
        layout.addWidget(QLabel("Formato de nombre de archivo:"))
        layout.addWidget(self.filename_format)

        # Separador personalizado
        self.separator_input = QLineEdit("_")
        layout.addWidget(QLabel("Separador personalizado:"))
        layout.addWidget(self.separator_input)

        # Checkbox para habilitar selección de columna
        self.use_column_checkbox = QCheckBox("Usar columna del Excel para nombres de archivo")
        layout.addWidget(self.use_column_checkbox)

        # Selector de columnas
        self.column_selector = QComboBox()
        self.column_selector.setEnabled(False)
        layout.addWidget(QLabel("Seleccionar columna para nombre de archivo:"))
        layout.addWidget(self.column_selector)

        self.enumerate_checkbox = QCheckBox("Incluir enumeración al final del nombre del archivo")
        self.enumerate_checkbox.setChecked(True)
        layout.addWidget(self.enumerate_checkbox)

        # Ejemplo de nombre de archivo
        self.example_label = QLabel("")
        layout.addWidget(QLabel("Ejemplo de nombre de archivo:"))
        layout.addWidget(self.example_label)

        # Botón para generar documentos
        layout.addWidget(self.generate_btn)

        widget.setLayout(layout)

        # Conectar los botones con sus funciones correspondientes
        self.load_word_btn.clicked.connect(self.load_word_template)
        self.load_excel_btn.clicked.connect(self.load_excel_file)
        self.generate_btn.clicked.connect(self.generate_documents)
        self.use_column_checkbox.stateChanged.connect(self.toggle_column_selector)
        self.filename_format.textChanged.connect(self.update_example_filename)
        self.column_selector.currentIndexChanged.connect(self.update_example_filename)
        self.separator_input.textChanged.connect(self.update_example_filename)
        self.enumerate_checkbox.stateChanged.connect(self.update_example_filename)

        return widget

    def show_welcome_screen(self):
        self.stacked_widget.setCurrentWidget(self.welcome_screen)

    def show_main_functionality(self):
        self.stacked_widget.setCurrentWidget(self.main_functionality_screen)

    def show_pdf_conversion(self):
        self.stacked_widget.setCurrentWidget(self.pdf_conversion_screen)  # Método para mostrar la pantalla de conversión de PDF
    def show_pdf_merge(self):
        self.stacked_widget.setCurrentWidget(self.pdf_merge_screen)
    # Aquí se incluyen las funciones originales relacionadas con la funcionalidad principal
    def load_word_template(self):
        self.word_template_path = load_word_file(self)
        if self.word_template_path:
            self.word_file_label.setText(f"Plantilla Word cargada: {self.word_template_path}")

    def load_excel_file(self):
        self.excel_file_path = load_excel_file(self)
        if self.excel_file_path:
            self.excel_file_label.setText(f"Archivo Excel cargado: {self.excel_file_path}")
            self.update_column_selector()

    def update_column_selector(self):
        excel_parser = ExcelParser(self.excel_file_path)
        columns = excel_parser.get_columns()
        self.column_selector.clear()
        self.column_selector.addItems(columns)
        self.update_example_filename()

    def toggle_column_selector(self):
        self.column_selector.setEnabled(self.use_column_checkbox.isChecked())
        self.update_example_filename()

    def update_example_filename(self):
        base_name = self.filename_format.text()
        separator = self.separator_input.text()
        if self.use_column_checkbox.isChecked():
            selected_column = self.column_selector.currentText()
            example_name = f"{base_name}{separator}{{valor_de_{selected_column}}}"
        else:
            example_name = base_name
        if self.enumerate_checkbox.isChecked():
            example_name += f"{separator}1"
        self.example_label.setText(example_name)

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
        numeric_columns = set()

        start_datetime = datetime.now()
        use_current_time = True

        if missing_columns:
            dialog = MissingColumnsDialog(missing_columns, self)
            if dialog.exec() == QDialog.DialogCode.Accepted:
                values, use_current_time, start_datetime = dialog.get_values()
                for column, (value, increment, is_minute, is_hour, is_numeric) in values.items():
                    static_values[column] = value
                    if increment:
                        increment_columns.add(column)
                    if is_minute:
                        minute_columns.add(column)
                    if is_hour:
                        hour_columns.add(column)
                    if is_numeric:
                        numeric_columns.add(column)
                print(f"Static values: {static_values}")  # Depuración adicional
            else:
                return  # User cancelled the operation

        data_list = excel_parser.get_data()
        doc_generator = DocumentGenerator(self.word_template_path)

        progress_dialog = ProgressDialog(self)
        progress_dialog.setRange(0, len(data_list))
        progress_dialog.show()

        selected_column = self.column_selector.currentText()
        include_enumeration = self.enumerate_checkbox.isChecked()
        separator = self.separator_input.text()

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
                    data['hora'] = str(current_datetime.hour).zfill(2)
                    data['minuto'] = str(current_datetime.minute).zfill(2)
                else:
                    data['fecha'] = format_datetime(start_datetime)
                    data['hora'] = str(start_datetime.hour).zfill(2)
                    data['minuto'] = str(start_datetime.minute).zfill(2)

                print(f"Data for document {index}: {data}")  # Añadir mensaje de depuración

                output_filename = self.filename_format.text()
                if self.use_column_checkbox.isChecked() and selected_column in data:
                    output_filename += f"{separator}{data[selected_column]}"
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
