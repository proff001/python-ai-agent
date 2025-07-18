from google.genai import types

from functions.get_file_content import get_file_content
from functions.get_files_info import get_files_info
from functions.run_python import run_python_file
from functions.write_file import write_file


def handle_function_call(function_call_part, verbose=False):
    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_call_part.name}")

    response = {}

    match function_call_part.name:
        case "get_files_info":
            response["result"] = get_files_info(
                "./calculator", **function_call_part.args
            )
        case "get_file_content":
            response["result"] = get_file_content(
                "./calculator", **function_call_part.args
            )
        case "run_python_file":
            response["result"] = run_python_file(
                "./calculator", **function_call_part.args
            )
        case "write_file":
            response["result"] = write_file("./calculator", **function_call_part.args)
        case _:
            response.error = f"Unknown function: {function_call_part.name}"

    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_call_part.name, response=response
            )
        ],
    )
