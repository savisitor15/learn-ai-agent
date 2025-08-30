import os
from pathlib import Path
from .common import _limit_directory

def _file_output(parent_dir):
    p = Path(parent_dir)
    output = ""
    for v in p.iterdir():
        fi = v.stat()
        output += f' - {v.name}: file_size={fi.st_size} bytes, is_dir={"True" if v.is_dir() else "False"}\n'
    return output

def _file_info_heading(directory):
    if directory == ".":
        return "Result for current directory:\n"
    return f"Result for '{directory}' directory:\n"


def get_files_info(working_directory, directory="."):
    try:
        full_path = os.path.join(working_directory, directory)
        if _limit_directory(working_directory, full_path):
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        if not os.path.isdir(full_path):
            return f'Error: "{directory}" is not a directory'
        return _file_info_heading(directory) + _file_output(full_path)
    except Exception as err:
        return f'Error: {err}, {type(err)}'
