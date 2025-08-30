import os
from .common import _limit_directory

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
        