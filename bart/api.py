from pathlib import Path
from typing import Optional, Union
from bart.models import Project, Document
from tinydb import TinyDB  # type: ignore
from .settings import (
    DEFAULT_DB_PATH,
    DEFAULT_SERIALIZER
)


class MissingDatabaseException(Exception):
    """
    The database for the project is missing; use this to ask the user if they
    want to create one
    """
    pass


class Bart:
    """
    "API" class for the app; all actions go through this class
    """

    def __init__(self, db_path: Path = DEFAULT_DB_PATH):
        self.db_path: Path = db_path
        self.db: TinyDB = TinyDB(self.db_path, storage=DEFAULT_SERIALIZER)
        self.project_table = self.db.table("project")
        self.docs_table = self.db.table("documents")

    def get_project(self):
        if not self.db_path.exists():
            raise MissingDatabaseException

        self.project = Project(**self.project_table.get(doc_id=1))
        self.docs = [Document(**doc) for doc in self.docs_table.all()]

    def create_project(self, name, markup_language, **kwargs):
        if not self.db:  # i.e., no data, create a project
            project = Project(name, markup_language, **kwargs)
            self.project_table.insert(project.__dict__)

    def add_document(self,
                     file_path: Union[str, Path],
                     manifest_index: Optional[int] = None):
        """
        Adds a document to the project, optionally inserts it into
        the project manifest at a specific point
        """
        self.get_project()

        if type(file_path) is not Path:
            file_path = Path(file_path)

        doc = Document(text_path=file_path)
        doc.id = self.docs_table.insert(doc.__dict__)

        if not manifest_index:
            manifest_index = len(self.project.manifest)

        self.project.manifest.insert(manifest_index, doc.id)

        self.project_table.update({"manifest": self.project.manifest})
        return doc

    def update_document(self, doc: Document):
        """
        Updates document information
        """
        pass

    def remove_document(self,
                        doc_id: int,
                        delete_document: bool = False):
        pass

    def combine_documents(self, docs: list[Document]):
        pass

    def add_notes_for_document(self):
        pass

    def update_manifest(self):
        pass
