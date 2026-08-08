import os
import subprocess

def run_python_file(working_directory: str, file_path: str, args: list[str] | None = None) -> str:
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))
        valid_target_file = os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs

        if not os.path.isfile(target_file):
            return f'Error: "{file_path}" does not exist or is not a regular file'

        if not file_path.endswith('.py'):
            return f'Error: "{file_path}" is not a Python file'
        
        if not valid_target_file:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        else:
            command = ["python", target_file]
            if args:
                command.extend(args)
            result = subprocess.run(command, cwd=working_dir_abs, capture_output=True, text=True, timeout=30)
            output =""
            if result.returncode:
                output += f"Process exited with code {result.returncode}"

            if not result.stdout and not result.stderr: 
                output += "No output produced"
            else:
                if result.stdout:
                    output += f"STDOUT: {result.stdout}"
                else:
                    output += f"STDERR: {result.stderr}"
        return output
    except Exception as e:
        return f"Error: executing Python file: {e}"

schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "Run or Excute the python file",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "File path to run from, relative to the working directory (default is the working directory itself)",
                },
                "args": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Additional arguments to pass to the Python file",
                }
            },
        },
    },
}