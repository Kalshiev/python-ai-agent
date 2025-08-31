import os
from google.genai import types

schema_write_file_content = types.FunctionDeclaration(
    name="write_file_content",
    description="Writes content to a file in the specified directory, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(type=types.Type.STRING, description="Relative path to the file"),
            "working_directory": types.Schema(type=types.Type.STRING, description="Base working dir"),
            "content": types.Schema(type=types.Type.STRING, description="Content to write to the file"),
        },
        required=["file_path"],
    ),
)

def write_file_content(working_directory, file_path, content):
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