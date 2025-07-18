import os

from google.genai import types


def get_file_content(working_directory, file_path):
    work_dir = os.path.abspath(working_directory)
    file = os.path.abspath(os.path.join(working_directory, file_path))

    if not file.startswith(work_dir):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

    if not os.path.isfile(file):
        return f'Error: File not found or is not a regular file: "{file_path}"'

    try:
        with open(file, "r") as f:
            file_content = f.read(10000)

            if f.read(1) != "":
                file_content += f'[...File "{file_path}" truncated at 10000 characters]'

        return file_content
    except Exception as e:
        return f"Error listing files: {e}"


schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads the content of a file, up to 10000 characters, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file, relative to the working directory.",
            ),
        },
    ),
)
