# core/excel_parser.py

import pandas as pd

class ExcelParser:
    def __init__(self, excel_path):
        self.df = pd.read_excel(excel_path)

    def get_columns(self):
        return list(self.df.columns)

    def get_data(self):
        return self.df.to_dict('records')
    
    def validate_columns(self, required_columns):
        missing_columns = set(required_columns) - set(self.get_columns())
        return list(missing_columns)