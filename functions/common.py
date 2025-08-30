import os


def _limit_directory(working_directory:str, full_path:str) -> bool:
    ap = os.path.abspath(full_path)
    wp = os.path.abspath(working_directory)
    if os.path.commonprefix([ap, wp]) != wp:
        return True
    return False
