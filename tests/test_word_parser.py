import unittest
import os
import sys

# Ensure the src directory is in the sys.path to find the core module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from core.word_parser import WordParser

class TestWordParser(unittest.TestCase):
    def setUp(self):
        # Uso de la ruta correcta para el archivo de Word
        self.word_path = os.path.abspath('docs/plantilla.docx')
        self.parser = WordParser(self.word_path)

    def test_get_placeholders(self):
        placeholders = self.parser.get_placeholders()
        print(f'Placeholders detectados: {placeholders}')  # Impresión adicional para verificar
        self.assertIsInstance(placeholders, list)
        
        # Comprobar que los placeholders fueron detectados correctamente
        self.assertGreater(len(placeholders), 0)
        for placeholder in placeholders:
            self.assertRegex(placeholder, r'\w+')

if __name__ == '__main__':
    unittest.main()
