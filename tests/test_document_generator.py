import unittest
from docx import Document
from docx.document import Document as DocumentType  # Explicitly import the Document class type
import sys
import os

# Ensure the src directory is in the sys.path to find the core module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from core.document_generator import DocumentGenerator


class TestDocumentGenerator(unittest.TestCase):
    def setUp(self):
        # Use absolute paths to ensure files are correctly found
        self.template_path = os.path.abspath('docs/plantilla.docx')
        self.output_path = os.path.abspath('docs/Pruebas/output.docx')
        self.data = {
            'nombre': 'John Doe',
            'cedula': '1234567890',
            'fecha': '2024-08-12',
            'hora': '20',
            'minuto': '00',
            'codigopostal': '12345'
        }
        self.generator = DocumentGenerator(self.template_path)

    def test_generate_document(self):
        doc = self.generator.generate_document(self.data)
        print(f'Tipo de doc: {type(doc).__name__}')  # Print the actual type name of doc
        self.assertIsInstance(doc, DocumentType)  # Ensure doc is an instance of Document
        
        # Verify that placeholders were replaced
        for p in doc.paragraphs:
            self.assertNotIn('{{nombre}}', p.text)
            self.assertNotIn('{{cedula}}', p.text)
            self.assertNotIn('{{fecha}}', p.text)
            self.assertNotIn('{{hora}}', p.text)
            self.assertNotIn('{{minuto}}', p.text)
            self.assertNotIn('{{codigopostal}}', p.text)

    def test_save_document(self):
        doc = self.generator.generate_document(self.data)
        self.generator.save_document(doc, self.output_path)
        
        saved_doc = Document(self.output_path)
        print(f'Tipo de saved_doc: {type(saved_doc).__name__}')  # Print the actual type name of saved_doc
        self.assertIsInstance(saved_doc, DocumentType)  # Ensure saved_doc is an instance of Document


if __name__ == '__main__':
    unittest.main()
