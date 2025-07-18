import os

from google.genai import types


def write_file(working_directory, file_path, content):
    work_dir = os.path.abspath(working_directory)
    file = os.path.abspath(os.path.join(working_directory, file_path))
    dir = os.path.split(file)[0]

    if not file.startswith(work_dir):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

    if not os.path.exists(dir):
        try:
            os.makedirs(dir)
        except Exception as e:
            return f'Error creating directory "{file_path}": {e}'

    try:
        with open(file, "w") as f:
            f.write(content)

        return (
            f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        )
    except Exception as e:
        return f'Error writing to "{file_path}": {e}'


schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes the provided content to a file, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file, relative to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to write to the file.",
            ),
        },
    ),
)
