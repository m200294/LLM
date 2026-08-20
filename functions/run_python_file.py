import os
import subprocess


def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    try:
        working_path = os.path.abspath(working_directory)
        file = os.path.normpath(os.path.join(working_path, file_path))
        valid_file = os.path.commonpath([working_path, file]) == working_path

        if not valid_file:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(file):
            return f'Error: "{file_path}" does not exist or is not a regular file'

        if not file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'

        command = ["python", file]
        if args:
            command.extend(args)

        results = subprocess.run(
            command, capture_output=True, text=True, timeout=30, cwd=working_directory
        )

        output = ""

        if results.returncode != 0:
            output += f"Process exited with code {results.returncode}"

        if not results.stdout and not results.stderr:
            output += " No output produced"
        else:
            output += f" STDOUT:{results.stdout}, STDERR: {results.stderr}"

        return output

    except Exception as e:
        return f"Error: executing Python file: {e}"


schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": " executes the Python file with optional arguments, returns stdout/stderr, and times out at 30 seconds",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "The name of the file you want to run a command on",
                },
                "args": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "a list of arguments you would like to run on the file",
                },
            },
            "required": ["file_path"],
        },
    },
}
