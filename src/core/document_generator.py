from docx import Document
import re

class DocumentGenerator:
    def __init__(self, template_path):
        self.template = Document(template_path)

    def generate_document(self, data):
        doc = self.template
        for p in doc.paragraphs:
            self.replace_placeholders(p, data)
        for table in doc.tables:
            for row in table.rows:
                for cell in row.cells:
                    self.replace_placeholders(cell, data)
        return doc

    def replace_placeholders(self, container, data):
        for key, value in data.items():
            if isinstance(value, (int, float)):
                value = str(value)
            placeholder = '{{' + key + '}}'
            container.text = container.text.replace(placeholder, value)

    def save_document(self, doc, output_path):
        doc.save(output_path)
