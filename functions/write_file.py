import os
from .common import _limit_directory
from google.genai import types


schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Write text to a provided file path, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to be written, relative to the working directory.",
            ),
            "content": types.Schema(
                type = types.Type.STRING,
                description="Text to be written into the provided file path"
            ),
        },
        required=["file_path", "content"]
    ),
)

def write_file(working_directory, file_path, content):
    full_path = os.path.join(working_directory, file_path)
    if _limit_directory(working_directory, full_path):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    try:
        if not os.path.exists(os.path.dirname(full_path)):
            os.mkdir(os.path.dirname(full_path)) # create the parent directory
        with open(full_path, "w") as fp:
            bytes_written = fp.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as err:
        return f'Error: {err}, {type(err)}'
        