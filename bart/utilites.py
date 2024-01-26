import re


def get_valid_pathname(name) -> str:
    """
    TODO: handle commas, colons, etc.
    """
    s = re.sub(r'[^a-zA-Z\d]', '-', name)
    s = re.sub(r'-+', '-', s)
    return s.lower().strip()
