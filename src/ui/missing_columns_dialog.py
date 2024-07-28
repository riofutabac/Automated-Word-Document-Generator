from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QCheckBox, QPushButton, QHBoxLayout
from PyQt6.QtCore import Qt

class MissingColumnsDialog(QDialog):
    def __init__(self, missing_columns, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Columnas Faltantes")
        self.layout = QVBoxLayout(self)
        self.missing_columns = missing_columns
        self.inputs = {}
        self.increment_checkboxes = {}
        self.minute_checkboxes = {}
        self.hour_checkboxes = {}

        self.minute_selected = False
        self.hour_selected = False

        for column in missing_columns:
            row_layout = QHBoxLayout()

            label = QLabel(f"Valor para '{column}':")
            input_field = QLineEdit()
            increment_checkbox = QCheckBox("Incrementar")
            minute_checkbox = QCheckBox("Minuto")
            hour_checkbox = QCheckBox("Hora")

            self.inputs[column] = input_field
            self.increment_checkboxes[column] = increment_checkbox
            self.minute_checkboxes[column] = minute_checkbox
            self.hour_checkboxes[column] = hour_checkbox

            increment_checkbox.stateChanged.connect(self.validate_checkboxes)
            minute_checkbox.stateChanged.connect(self.validate_checkboxes)
            hour_checkbox.stateChanged.connect(self.validate_checkboxes)

            row_layout.addWidget(label)
            row_layout.addWidget(input_field)
            row_layout.addWidget(increment_checkbox)
            row_layout.addWidget(minute_checkbox)
            row_layout.addWidget(hour_checkbox)

            self.layout.addLayout(row_layout)

        self.confirm_button = QPushButton("Confirmar")
        self.confirm_button.clicked.connect(self.validate_and_accept)
        self.layout.addWidget(self.confirm_button)

    def validate_checkboxes(self):
        for column, minute_checkbox in self.minute_checkboxes.items():
            hour_checkbox = self.hour_checkboxes[column]
            if minute_checkbox.isChecked():
                hour_checkbox.setChecked(False)
                hour_checkbox.setEnabled(False)
                self.minute_selected = True
            else:
                hour_checkbox.setEnabled(True)
                self.minute_selected = False

        for column, hour_checkbox in self.hour_checkboxes.items():
            minute_checkbox = self.minute_checkboxes[column]
            if hour_checkbox.isChecked():
                minute_checkbox.setChecked(False)
                minute_checkbox.setEnabled(False)
                self.hour_selected = True
            else:
                minute_checkbox.setEnabled(True)
                self.hour_selected = False

    def validate_and_accept(self):
        for column, input_field in self.inputs.items():
            value = input_field.text()
            if self.minute_checkboxes[column].isChecked() or self.hour_checkboxes[column].isChecked():
                try:
                    int(value)
                except ValueError:
                    QMessageBox.warning(self, "Error", f"El valor para '{column}' debe ser un número.")
                    return

        self.accept()

    def get_values(self):
        return {
            column: (
                self.inputs[column].text(),
                self.increment_checkboxes[column].isChecked(),
                self.minute_checkboxes[column].isChecked(),
                self.hour_checkboxes[column].isChecked()
            ) for column in self.missing_columns
        }
