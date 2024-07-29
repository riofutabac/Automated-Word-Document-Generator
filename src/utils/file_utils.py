#utils.fileutils
import os
import re

def create_output_directory(directory_path):
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)

def generate_output_filename(base_name, index):
    sanitized_name = re.sub(r'\s+', '_', base_name)  # Reemplaza espacios con guiones bajos
    return f"{sanitized_name}_{index}.docx"