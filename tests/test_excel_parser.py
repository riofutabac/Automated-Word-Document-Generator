import unittest
import os
import sys

# Ensure the src directory is in the sys.path to find the core module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from core.excel_parser import ExcelParser

class TestExcelParser(unittest.TestCase):
    def setUp(self):
        # Uso de la ruta correcta para el archivo Excel
        self.excel_path = os.path.abspath('docs/datos_70_registros.xlsx')
        self.parser = ExcelParser(self.excel_path)
        self.placeholders = ['name', 'date', 'address']

    def test_get_columns(self):
        columns = self.parser.get_columns()
        print("\n--- Columnas Obtenidas ---")
        print(columns)
        self.assertIsInstance(columns, list)
        self.assertGreater(len(columns), 0)

    def test_validate_columns(self):
        missing_columns = self.parser.validate_columns(self.placeholders)
        print("\n--- Columnas Faltantes ---")
        if missing_columns:
            print(f"Las siguientes columnas faltan: {missing_columns}")
        else:
            print("No faltan columnas.")
        self.assertIsInstance(missing_columns, list)
        
        # Comprobar que la lista de columnas faltantes es correcta
        for col in missing_columns:
            self.assertNotIn(col, self.parser.get_columns())

    def test_get_data(self):
        data = self.parser.get_data()
        print("\n--- Datos Obtenidos ---")
        if data:
            print(f"Cantidad de filas obtenidas: {len(data)}")
            print("Primera fila de datos:", data[0])  # Muestra la primera fila para ejemplo
        else:
            print("No se obtuvieron datos.")
        self.assertIsInstance(data, list)
        self.assertGreater(len(data), 0)

if __name__ == '__main__':
    unittest.main()
