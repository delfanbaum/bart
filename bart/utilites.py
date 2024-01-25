from pathlib import Path
from typing import Optional

from bart.user_config import get_config


def get_valid_pathname(name) -> str:
    """
    TODO: handle commas, colons, etc.
    """
    s = str(name).strip().replace(' ', '-')
    return s.lower()


def get_project_files(project_dir: Path = Path.cwd()) -> Optional[list[Path]]:
    """
    Collects the project files for further operations
    """
    project_extension = get_config().project_extension
    project_files = (
            list(project_dir.glob(f"[0-9][0-0]-*.{project_extension}")).sort()
            )

    return project_files
