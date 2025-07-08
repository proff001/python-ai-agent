import os

def get_files_info(working_directory, directory=None):
	work_dir = os.path.abspath(working_directory)
	dir = work_dir

	if directory:
		dir = os.path.abspath(os.path.join(working_directory, directory))

	if not dir.startswith(work_dir):
		return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

	if not os.path.isdir(dir):
		return f'Error: "{directory}" is not a directory'
	
	try:
		file_stats = []

		for file in os.listdir(dir):
			file_path = os.path.join(dir, file)
			file_size = os.path.getsize(file_path)
			file_is_dir = os.path.isdir(file_path)

			file_stats.append(f"- {file}: file_size={file_size} bytes, is_dir={file_is_dir}")

		return "\n".join(file_stats)
	except Exception as e:
		return f'Error listing files: {e}'
