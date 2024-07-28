#ui.progress dialog
from PyQt6.QtWidgets import QProgressDialog
from PyQt6.QtCore import Qt

class ProgressDialog(QProgressDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Generando Documentos")
        self.setWindowModality(Qt.WindowModality.WindowModal)
        self.setMinimumDuration(0)
        self.setCancelButton(None)
        self.setRange(0, 100)

    def update_progress(self, value):
        self.setValue(value)