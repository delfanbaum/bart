from pathlib import Path

from bart.exceptions import ProjectFileExistsException


def write_template(template, path: Path, **kwargs):
    """
    Writes a template to a given path. If something already exists at that path,
    raise an exception (to be handled later by the cli app)
    """
    if path.exists():
        raise ProjectFileExistsException


    text = template(**kwargs)
    with path.open('wt') as f:
        f.write(text)


def named_document_template(markup: str,
                            document_name: str,
                            heading_level: int = 1):

    match markup:
        case "asciidoc":
            return f"""{"=" * heading_level} {document_name}"""
        case "markdown":
            return f"""{"#" * heading_level} {document_name}"""
        case _:
            return f"{document_name}"
