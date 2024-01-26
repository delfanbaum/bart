from pathlib import Path

from bart.config import BartConfig
from bart.exceptions import NotInProjectException, MissingProjectRootException, ProjectDirExistsException
from bart.templates import named_document_template, write_template
from bart.utilites import get_next_doc_number, get_valid_pathname


class BartProject:

    def __init__(self,
                 project_dir: Path = Path.cwd(),
                 new: bool = False,
                 project_name: str = "") -> None:
        self.project_dir = project_dir
        self.config = BartConfig(self.project_dir)

        if new:  # have to "seed" the project before getting docs
            self.begin(project_name)

        self.documents = self.get_project_docs()
        self.root = self.documents[0]

        if not int(self.root.name.split('-')[0]) == 0:
            raise MissingProjectRootException


    def begin(self, project_name):
        """
        "Seeds" a new project with a 00- "root" file and title
        """

        numbering = get_next_doc_number(None, self.config.doc_levels, 0)

        if self.project_dir.exists():
            raise ProjectDirExistsException
        else:
            self.project_dir.mkdir()

        project_root = (self.project_dir / (numbering + "-" +
                                            get_valid_pathname(project_name) + "." +
                                            self.config.markup.extension()))
        write_template(named_document_template,
                       project_root,
                       markup=self.config.markup,
                       document_name=project_name,
                       heading_level=1
                       )


    def get_project_docs(self) -> list[Path]:
        """
        Collects the project files for further operations
        """
        project_files = (
                list(self.project_dir.glob(
                    f"[0-9]*.{self.config.markup.extension()}"))
                )

        if not project_files:
            raise NotInProjectException

        project_files.sort()
        return project_files
    

    def add_document(self, name: str, level: int=1) -> Path:
        """
        Adds a document at the "section" level (what
        config.doc_numbering) is set to
        """
        last_doc = self.get_project_docs()[-1]

        # i.e., 1, 10, 100, etc.
        add_position  = 10 ** (self.config.doc_levels - 1)
        next_number = get_next_doc_number(last_doc,
                                          self.config.doc_levels,
                                          add_position)
        new_document = (self.project_dir /
                        f"{next_number}-{get_valid_pathname(name)}.{self.config.markup.extension()}")

        write_template(named_document_template,
                       new_document,
                       markup=self.config.markup,
                       document_name=name,
                       heading_level=level
                       )
        return new_document
