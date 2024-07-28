#core.excel parser
import pandas as pd

class ExcelParser:
    def __init__(self, excel_path):
        self.df = pd.read_excel(excel_path)

    def get_columns(self):
        return list(self.df.columns)

    def get_data(self):
        return self.df.to_dict('records')