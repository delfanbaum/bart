from pathlib import Path
from typing import Optional

from bart.config import BartConfig


class BartProject:

    def __init__(self, project_dir: Path = Path.cwd()) -> None:
        self.project_dir = project_dir
        self.config = BartConfig(self.project_dir)
        self.documents = self.get_project_docs()


    def get_project_docs(self) -> Optional[list[Path]]:
        """
        Collects the project files for further operations
        """
        project_files = (
                list(self.project_dir.glob(
                    f"[0-9][0-0]-*.{self.config.markup_ext}")).sort()
                )

        return project_files
    

    def reorder_documents(self, reordered_docs: list[Path]) -> None:
        pass


