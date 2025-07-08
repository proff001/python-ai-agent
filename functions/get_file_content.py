import os

def get_file_content(working_directory, file_path):
	work_dir = os.path.abspath(working_directory)
	file = os.path.abspath(os.path.join(working_directory, file_path))

	if not file.startswith(work_dir):
		return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

	if not os.path.isfile(file):
		return f'Error: File not found or is not a regular file: "{file_path}"'

	max_chars = os.getenv("MAX_CHARS") or 10000

	if not max_chars:
		return f'Error: MAX_CHARS environment variable not set'

	try:
		with open(file, "r") as f:
			file_content = f.read(max_chars)

			if f.read(1) != "":
				file_content += f'[...File "{file_path}" truncated at 10000 characters]'

		return file_content
	except Exception as e:
		return f'Error listing files: {e}'
