from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QCheckBox, QPushButton, QHBoxLayout, QMessageBox, QDateTimeEdit
from PyQt6.QtCore import Qt, QDateTime

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
        self.numeric_checkboxes = {}

        # Bloque de selección de fecha y hora
        datetime_layout = QHBoxLayout()
        self.datetime_edit = QDateTimeEdit(QDateTime.currentDateTime())
        self.datetime_edit.setDisplayFormat("dd/MM/yyyy HH:mm")
        self.datetime_edit.setFixedWidth(200)  # Ajustar el ancho para que la hora sea visible
        self.confirm_time_button = QPushButton("Confirmar")
        self.confirm_time_button.setFixedWidth(100)  # Ajustar el ancho del botón
        datetime_layout.addWidget(QLabel("Fecha y hora inicial:"))
        datetime_layout.addWidget(self.datetime_edit)
        datetime_layout.addWidget(self.confirm_time_button)
        self.layout.addLayout(datetime_layout)
        self.confirm_time_button.clicked.connect(self.lock_time_settings)

        for column in missing_columns:
            row_layout = QHBoxLayout()

            label = QLabel(f"Valor para '{column}':")
            input_field = QLineEdit()
            input_field.setEnabled(False)
            increment_checkbox = QCheckBox("Incrementar")
            increment_checkbox.setEnabled(False)
            minute_checkbox = QCheckBox("Minuto")
            minute_checkbox.setEnabled(False)
            hour_checkbox = QCheckBox("Hora")
            hour_checkbox.setEnabled(False)
            numeric_checkbox = QCheckBox("Numérico")
            numeric_checkbox.setEnabled(True)

            self.inputs[column] = input_field
            self.increment_checkboxes[column] = increment_checkbox
            self.minute_checkboxes[column] = minute_checkbox
            self.hour_checkboxes[column] = hour_checkbox
            self.numeric_checkboxes[column] = numeric_checkbox

            minute_checkbox.stateChanged.connect(lambda _, c=column: self.update_checkbox_state(c, "minute"))
            hour_checkbox.stateChanged.connect(lambda _, c=column: self.update_checkbox_state(c, "hour"))
            numeric_checkbox.stateChanged.connect(lambda _, c=column: self.update_checkbox_state(c, "numeric"))

            row_layout.addWidget(label)
            row_layout.addWidget(input_field)
            row_layout.addWidget(increment_checkbox)
            row_layout.addWidget(minute_checkbox)
            row_layout.addWidget(hour_checkbox)
            row_layout.addWidget(numeric_checkbox)

            self.layout.addLayout(row_layout)

        self.confirm_button = QPushButton("Confirmar")
        self.confirm_button.setEnabled(False)
        self.confirm_button.clicked.connect(self.validate_and_accept)
        self.layout.addWidget(self.confirm_button)

    def lock_time_settings(self):
        self.datetime_edit.setEnabled(False)
        self.confirm_time_button.setEnabled(False)
        self.confirm_button.setEnabled(True)
        for input_field in self.inputs.values():
            input_field.setEnabled(True)
        for increment_checkbox in self.increment_checkboxes.values():
            increment_checkbox.setEnabled(True)
        for minute_checkbox in self.minute_checkboxes.values():
            minute_checkbox.setEnabled(True)
        for hour_checkbox in self.hour_checkboxes.values():
            hour_checkbox.setEnabled(True)
        for numeric_checkbox in self.numeric_checkboxes.values():
            numeric_checkbox.setEnabled(True)

    def update_checkbox_state(self, column, type):
        if type == "minute":
            if self.minute_checkboxes[column].isChecked():
                self.inputs[column].setText(str(self.datetime_edit.dateTime().time().minute()))
                self.inputs[column].setEnabled(False)
                self.hour_checkboxes[column].setEnabled(False)
                self.numeric_checkboxes[column].setChecked(True)
                self.numeric_checkboxes[column].setEnabled(False)
                self.increment_checkboxes[column].setEnabled(True)
            else:
                self.inputs[column].setEnabled(True)
                self.hour_checkboxes[column].setEnabled(True)
                self.increment_checkboxes[column].setEnabled(False)
                self.numeric_checkboxes[column].setEnabled(True)
                self.numeric_checkboxes[column].setChecked(False)

        elif type == "hour":
            if self.hour_checkboxes[column].isChecked():
                self.inputs[column].setText(str(self.datetime_edit.dateTime().time().hour()))
                self.inputs[column].setEnabled(False)
                self.minute_checkboxes[column].setEnabled(False)
                self.numeric_checkboxes[column].setChecked(True)
                self.numeric_checkboxes[column].setEnabled(False)
                self.increment_checkboxes[column].setEnabled(True)
            else:
                self.inputs[column].setEnabled(True)
                self.minute_checkboxes[column].setEnabled(True)
                self.increment_checkboxes[column].setEnabled(False)
                self.numeric_checkboxes[column].setEnabled(True)
                self.numeric_checkboxes[column].setChecked(False)

        elif type == "numeric":
            if self.numeric_checkboxes[column].isChecked():
                if not self.inputs[column].text().isdigit():
                    QMessageBox.warning(self, "Error", f"El valor para '{column}' debe ser numérico.")
                    self.numeric_checkboxes[column].setChecked(False)
                else:
                    self.increment_checkboxes[column].setEnabled(True)
            else:
                self.increment_checkboxes[column].setEnabled(False)

    def validate_and_accept(self):
        # Ahora simplemente verificamos que todos los campos tengan un valor válido
        for column, input_field in self.inputs.items():
            if self.numeric_checkboxes[column].isChecked() and not input_field.text().isdigit():
                QMessageBox.warning(self, "Error", f"El valor para '{column}' debe ser numérico.")
                return
        self.accept()

    def get_values(self):
        values = {
            column: (
                self.inputs[column].text(),
                self.increment_checkboxes[column].isChecked(),
                self.minute_checkboxes[column].isChecked(),
                self.hour_checkboxes[column].isChecked(),
                self.numeric_checkboxes[column].isChecked()
            ) for column in self.missing_columns
        }
        use_current_time = any([
            self.minute_checkboxes[column].isChecked() or
            self.hour_checkboxes[column].isChecked() or
            self.increment_checkboxes[column].isChecked()
            for column in self.missing_columns
        ])  # Only use the current time if any related checkbox is checked

        # Imprimir el valor de use_current_time
        print(f"use_current_time: {use_current_time}")

        start_datetime = self.datetime_edit.dateTime().toPyDateTime() if use_current_time else None
        return values, use_current_time, start_datetime
