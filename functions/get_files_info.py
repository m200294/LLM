import os


def get_files_info(working_directory: str, directory: str = ".") -> str:
    try:
        working_path = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_path, directory))

        valid_target = os.path.commonpath([working_path, target_dir]) == working_path

        if not valid_target:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        if not os.path.isdir(target_dir):
            return f'Error: "{directory}" is not a directory'

        info_list = []

        for child in os.listdir(target_dir):
            full_path = os.path.join(target_dir, child)
            info_list.append(
                f"- {child}: file_size={os.path.getsize(full_path)} bytes, is_dir={os.path.isdir(full_path)}"
            )

        return "\n".join(info_list)

    except Exception as e:
        return f"Error: {e}"


schema_get_files_info = {
    "type": "function",
    "function": {
        "name": "get_files_info",
        "description": "Lists files in a specified directory relative to the working directory, providing file size and directory status",
        "parameters": {
            "type": "object",
            "properties": {
                "directory": {
                    "type": "string",
                    "description": "Directory path to list files from, relative to the working directory (default is the working directory itself)",
                },
            },
        },
    },
}
