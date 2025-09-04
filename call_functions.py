from google.genai import types

from functions.get_files_info import schema_get_files_info, get_files_info
from functions.run_python_file import schema_run_python_file, run_python_file
from functions.get_file_content import schema_get_file_content, get_file_content
from functions.write_file import schema_write_file, write_file

functions_defined = {
    "run_python_file": run_python_file,
    "write_file": write_file,
    "get_file_content": get_file_content,
    "get_files_info": get_files_info,
}

available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_write_file,
            schema_get_file_content,
            schema_run_python_file
        ]
    )
