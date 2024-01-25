from pathlib import Path
from typing import Optional

from bart.config import BartConfig
from bart.templates import project_root_template


class BartProject:

    def __init__(self, project_dir: Path = Path.cwd()) -> None:
        self.project_dir = project_dir
        self.config = BartConfig(self.project_dir)
        self.documents = self.get_project_docs()


    def begin(self, project_name):
        """
        "Seeds" a new project with a 00- file and title
        """
        numbering = "0" * (self.config.doc_numbering + 1)

        if not self.project_dir.is_dir():
            self.project_dir.mkdir()

        project_root = (self.project_dir / (numbering + "-" +
                                            self.project_dir.name + "." +
                                            self.config.markup_ext))
        with project_root.open('wt') as f:
            f.write(project_root_template(self.config.markup,
                                          project_name))


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


