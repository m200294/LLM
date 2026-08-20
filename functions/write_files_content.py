import os


def write_file(working_directory: str, file_path: str, content: str) -> str:
    try:
        working_path = os.path.abspath(working_directory)
        file = os.path.normpath(os.path.join(working_path, file_path))
        valid_file = os.path.commonpath([working_path, file]) == working_path

        if not valid_file:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        if os.path.isdir(file):
            return f'Error: Cannot write to "{file_path}" as it is a directory'

        os.makedirs(os.path.dirname(file), exist_ok=True)

        with open(file, "w") as f:
            f.write(content)
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except Exception as e:
        return f"Error: {e}"


schema_write_file = {
    "type": "function",
    "function": {
        "name": "write_file",
        "description": "overwrites a files contents, creates missing parent directories and file starting from the working directory",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "The name of the file that you want to rewrite the content of",
                },
                "content": {
                    "type": "string",
                    "description": "The content you want to rewrite the file with",
                },
            },
            "required": ["file_path", "content"],
        },
    },
}
