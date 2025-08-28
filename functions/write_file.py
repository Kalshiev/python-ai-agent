import os

def write_file(working_directory, file_path, content):
    try:
        file_complete_path = os.path.join(working_directory, file_path)

        if not os.path.realpath(file_complete_path).startswith(os.path.realpath(working_directory)):
            return f"Error: Cannot write to \"{file_complete_path}\" as it is outside of the permitted working directory"
    
        if not os.path.exists(os.path.dirname(file_complete_path)):
            os.makedirs(os.path.dirname(file_complete_path))

        with open(file_complete_path, 'w') as file:
            file.write(content)
            return f"Successfully wrote to \"{file_complete_path}\" ({len(content)} characters written)"
    except Exception as e:
        return f"Error: {str(e)}"