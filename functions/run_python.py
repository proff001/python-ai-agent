import os
import subprocess

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
			result += f"\Process exited with code {process.returncode}"

		return result

	except Exception as e:
		return f"Error: executing Python file: {e}"