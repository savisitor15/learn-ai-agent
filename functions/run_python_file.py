from .common import _limit_directory
import os
import subprocess

def run_python_file(working_directory, file_path, args=[]):
    full_path = os.path.join(working_directory, file_path)
    if _limit_directory(working_directory, full_path):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not os.path.exists(full_path):
        return f'Error: File "{file_path}" not found.'
    if not file_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'
    try:
        process = subprocess.run(args=['python', file_path] + args, capture_output=True, text=True, timeout=30, cwd=working_directory)
        output = ""
        if len(process.stderr) != 0:
            output = f"STDERR: {process.stderr}"
        if len(process.stdout) != 0:
            if len(output) > 0:
                output = output + "\n"
            output = output + f"STDOUT: {process.stdout}"
        if len(output) == 0:
            output = "No output produced."
        if process.returncode != 0:
            if len(output) > 0:
                output = output + "\n"
            output = output + f"Process exited with code {process.returncode}"
        return output
    except Exception as err:
        return f"Error: executing Python file: {err}"

