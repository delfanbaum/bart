import re
from pathlib import Path
from typing import Optional


def get_valid_pathname(name) -> str:
    """
    TODO: handle commas, colons, etc.
    """
    s = re.sub(r'[^a-zA-Z\d]', '-', name)
    s = re.sub(r'-+', '-', s)
    return s.lower().strip()


def get_next_doc_number(last_doc: Optional[Path],
                        project_levels: int,
                        add_position: int) -> str:
    """
    Given a document path and the section document numbering,
    return the "next" chapter or section 
    """
    if not last_doc:
        next_number = "0" * project_levels
    else:
        next_number = f"{int(last_doc.name.split('-')[0]) + add_position}"
    
    if project_levels == 1:  # special case for 01, 02, etc.
        return next_number.zfill(2)
    else:
        return next_number.zfill(project_levels)

def get_doc_position(project, doc: Path):
    """
    Gets the "position" of the document, i.e., is it a main doc? Is it a
    sub-doc? Etc.
    """
    doc_level = doc.name.split('-')[0]

    if (project.config.doc_levels == 1 or
        doc_level.find('0') == -1):
        return 1
