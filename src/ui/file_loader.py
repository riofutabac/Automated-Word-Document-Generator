#ui.fileloader
from PyQt6.QtWidgets import QFileDialog

def load_word_file(parent):
    file_name, _ = QFileDialog.getOpenFileName(parent, "Seleccionar Plantilla Word", "", "Word Files (*.docx)")
    return file_name

def load_excel_file(parent):
    file_name, _ = QFileDialog.getOpenFileName(parent, "Seleccionar Archivo Excel", "", "Excel Files (*.xlsx *.xls)")
    return file_name

def select_output_directory(parent):
    return QFileDialog.getExistingDirectory(parent, "Seleccionar carpeta de destino")
