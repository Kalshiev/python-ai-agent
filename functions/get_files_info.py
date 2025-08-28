import os

def get_files_info(working_directory, directory="."):
    try:
        full_path = os.path.join(working_directory, directory)

        if not os.path.isdir(full_path):
            return f'Error: "{directory}" is not a directory'
        
        if not os.path.abspath(full_path).startswith(os.path.abspath(working_directory)):
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        
        files_in_dir = os.listdir(full_path)

        formatted_files = []

        for file in files_in_dir:
            file_path = os.path.join(full_path, file)
            file_size = os.path.getsize(file_path)
            file_is_dir = os.path.isdir(file_path)
            formatted = f"- {file}: file_size={file_size} bytes, is_dir={file_is_dir}"
            formatted_files.append(formatted)
        
        return "\n".join(formatted_files)
    except Exception as e:
        return f"Error: {e}"