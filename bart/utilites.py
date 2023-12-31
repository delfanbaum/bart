def get_valid_pathname(name) -> str:
    """
    TODO: handle commas, colons, etc.
    """
    s = str(name).strip().replace(' ', '-')
    return s.lower()
