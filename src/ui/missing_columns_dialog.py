from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QCheckBox, QPushButton

class MissingColumnsDialog(QDialog):
    def __init__(self, missing_columns, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Columnas Faltantes")
        self.layout = QVBoxLayout(self)
        self.missing_columns = missing_columns
        self.inputs = {}
        self.increment_checkboxes = {}

        for column in missing_columns:
            label = QLabel(f"Valor para '{column}':")
            input_field = QLineEdit()
            increment_checkbox = QCheckBox("Incrementar")
            self.inputs[column] = input_field
            self.increment_checkboxes[column] = increment_checkbox
            self.layout.addWidget(label)
            self.layout.addWidget(input_field)
            self.layout.addWidget(increment_checkbox)

        self.confirm_button = QPushButton("Confirmar")
        self.confirm_button.clicked.connect(self.accept)
        self.layout.addWidget(self.confirm_button)

    def get_values(self):
        return {column: (self.inputs[column].text(), self.increment_checkboxes[column].isChecked()) 
                for column in self.missing_columns}
