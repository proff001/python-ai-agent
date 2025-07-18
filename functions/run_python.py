import os
import subprocess

from google.genai import types


def run_python_file(working_directory, file_path):
    work_dir = os.path.abspath(working_directory)
    file = os.path.abspath(os.path.join(working_directory, file_path))

    if not file.startswith(work_dir):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

    if not os.path.exists(file):
        return f'Error: File "{file_path}" not found.'

    if not file_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'

    try:
        process = subprocess.run(["python", file], timeout=30, capture_output=True)

        output = process.stdout.decode("utf-8")
        error = process.stderr.decode("utf-8")

        if not output:
            output = "No output produced."

        result = f"STDOUT:\n{output}\nSTDERR:\n{error}"

        if process.returncode != 0:
            result += f"Process exited with code {process.returncode}"

        return result

    except Exception as e:
        return f"Error: executing Python file: {e}"


schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs a Python file, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the Python file, relative to the working directory.",
            ),
        },
    ),
)
