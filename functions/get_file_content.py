import os
from config import MAX_CHAR


def get_file_content(working_directory: str, file_path: str) -> str:
    try:
        working_path = os.path.abspath(working_directory)
        file = os.path.normpath(os.path.join(working_path, file_path))
        valid_file = os.path.commonpath([working_path, file]) == working_path

        if not valid_file:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(file):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        with open(file) as r:
            content = r.read(MAX_CHAR)
            if r.read(1):
                content += f'[...File "{file_path}" truncated at {MAX_CHAR} characters]'
            return content

    except Exception as e:
        return f"Error: {e}"


schema_get_file_content = {
    "type": "function",
    "function": {
        "name": "get_file_content",
        "description": f"retrive the contents of a file inside the working directory, with max char of {MAX_CHAR}",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "The name of the file that you want to get the content of",
                },
            },
            "required": ["file_path"],
        },
    },
}
