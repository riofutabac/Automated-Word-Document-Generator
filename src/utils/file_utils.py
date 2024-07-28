#utils.fileutils
import os

def create_output_directory(path):
    if not os.path.exists(path):
        os.makedirs(path)

def generate_output_filename(base_name, index, extension='.docx'):
    safe_base_name = "".join([c if c.isalnum() else "_" for c in str(base_name)])
    return f"{safe_base_name}_{index}{extension}"
