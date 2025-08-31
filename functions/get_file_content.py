import os
from functions.config import MAX_CHARS
from google.genai import types

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Gets content of the specified file, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(type=types.Type.STRING, description="Relative path to the file"),
            "working_directory": types.Schema(type=types.Type.STRING, description="Base working dir"),
        },
        required=["file_path"],
    ),
)

def get_file_content(working_directory, file_path):
    try:
        full_path = os.path.join(working_directory, file_path)

        if not os.path.realpath(full_path).startswith(os.path.realpath(working_directory)):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(full_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        with open(full_path, 'r') as file:
            content = file.read(MAX_CHARS + 1)
            if len(content) > MAX_CHARS:
                return f"{content[:MAX_CHARS]} [...File \"{file_path}\" truncated at {MAX_CHARS} characters]"
            return content
    except Exception as e:
        return f"Error: {e}"