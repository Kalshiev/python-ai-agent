import os

def get_files_info(working_directory, directory="."):
    full_path = os.path.join(working_directory, directory)

    if not os.path.exists(directory):
        raise Exception(f'Error: "{directory}" is not a directory')
    
    if not check_path(working_directory, directory):
        raise Exception(f'Error: Cannot list "{directory}" as it is outside the permitted working directory')
    
    files_in_dir = os.listdir(full_path)

    formatted_files = []

    for file in files_in_dir:
        formatted = f"{file}: file_size={os.path.getsize(file)} bytes, is_dir={os.path.isdir(file)}"
        formatted_files.append(formatted)
    
    return "\n".join(formatted_files)

def check_path(working_dir, dir):
    abs_parent = os.path.abspath(working_dir)
    abs_sub = os.path.abspath(dir)
    return abs_sub.startswith(abs_parent)