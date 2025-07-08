import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

def main():
	load_dotenv()

	verbose = "--verbose" in sys.argv
	args = [arg for arg in sys.argv[1:] if not arg.startswith("--verbose")]   

	api_key = os.getenv("GEMINI_API_KEY") 
	if not api_key:
		print("Please set the GEMINI_API_KEY environment variable in .env")
		sys.exit(1)

	if not args:
		print("Usage: python main.py <prompt> [--verbose]")
		print("Example: python main.py \"What is the capital of France?\"")
		sys.exit(1)

	client = genai.Client(api_key=api_key)
	prompt = str.join(" ", args)

	if verbose:
		print(f"User prompt: {prompt}")

	messages = [
		types.Content(role="user", parts=[types.Part(text=prompt)]),
	]

	generate_response(client, messages, verbose)

schema_get_files_info = types.FunctionDeclaration(
	name="get_files_info",
	description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
	parameters=types.Schema(
		type=types.Type.OBJECT,
		properties={
			"directory": types.Schema(
				type=types.Type.STRING,
				description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
			),
		},
	),
)

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

available_functions = types.Tool(
	function_declarations=[
		schema_get_files_info,
		schema_get_file_content,
		schema_run_python_file,
		schema_write_file,
	]
)

def generate_response(client, messages, verbose):
	system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

	res = client.models.generate_content(
		model="gemini-2.0-flash-001",
		contents=messages,
		config=types.GenerateContentConfig(
			system_instruction=system_prompt,
			tools=[available_functions],
		)
	) 

	if verbose:
		print(f"Prompt tokens: {res.usage_metadata.prompt_token_count}")
		print(f"Response tokens: {res.usage_metadata.candidates_token_count}")

	if res.function_calls:
		for function_call_part in res.function_calls:
			print(f"Calling function: {function_call_part.name}({function_call_part.args})")

	print("Response:")
	print(res.text)

if __name__ == "__main__":
    main()
