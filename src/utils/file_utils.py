#utils.fileutils
import os

def create_output_directory(path):
    if not os.path.exists(path):
        os.makedirs(path)

def generate_output_filename(base_name, index, extension='.docx'):
    return f"{base_name}_{index}{extension}"