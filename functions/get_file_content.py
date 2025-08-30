import os
from .config import MAX_CHARS
from .common import _limit_directory


def get_file_content(working_directory, file_path):
    try:
        file_contents = ""
        full_path = os.path.join(working_directory, file_path)
        if _limit_directory(working_directory, full_path):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(full_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        with open(full_path) as fp:
            file_contents = fp.read(MAX_CHARS)
            if len(file_contents) == MAX_CHARS and fp.tell() != 0:
                ermesg = f'[...File "{file_path}" truncated at 10000 characters]'
                file_contents = file_contents[:len(file_contents)-len(ermesg)] + ermesg
        return file_contents

    except Exception as err:
        return f'Error: {err}, {type(err)}'
