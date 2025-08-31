import os
import sys
import subprocess
from google.genai import types

schema_run_python = types.FunctionDeclaration(
    name="run_python",
    description="Executes a Python script in the specified directory, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(type=types.Type.STRING, description="Relative path to the file"),
            "working_directory": types.Schema(type=types.Type.STRING, description="Base working dir"),
            "args": types.Schema(type=types.Type.ARRAY, items=types.Schema(type=types.Type.STRING), description="Arguments to pass to the script"),
        },
        required=["file_path"],
    ),
)

def run_python(working_directory, file_path, args=[]):
    try:
        base = os.path.realpath(working_directory)
        target = os.path.realpath(os.path.join(working_directory, file_path))
        if os.path.commonpath([base, target]) != base:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        if not os.path.exists(target):
            return f'Error: File "{file_path}" not found.'

        if not file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file.'

        completed_process = subprocess.run(
            [sys.executable, target] + args,
            capture_output=True,
            cwd=working_directory,
            text=True,
            timeout=30
            )

        if completed_process.returncode != 0:
            return f"Process exited with code {completed_process.returncode}\nSTDOUT: {completed_process.stdout}\nSTDERR: {completed_process.stderr}"

        if len(completed_process.stdout) == 0 and len(completed_process.stderr) == 0:
            return "No output produced."

        return f"STDOUT: {completed_process.stdout}\nSTDERR: {completed_process.stderr}"

    except Exception as e:
        return f"Error: executing Python file: {e}"