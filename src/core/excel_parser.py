# core/excel_parser.py

import pandas as pd

class ExcelParser:
    def __init__(self, excel_path):
        self.excel_path = excel_path
        self.data_frame = pd.read_excel(excel_path, dtype=str)  # Asegurar que todos los datos se leen como texto

    def get_columns(self):
        return self.data_frame.columns.tolist()

    def validate_columns(self, placeholders):
        missing_columns = [col for col in placeholders if col not in self.data_frame.columns]
        return missing_columns

    def get_data(self):
        return self.data_frame.to_dict(orient='records')
