from pathlib import Path
from typing import Optional
from bart.models import Project, Document
from tinydb import TinyDB  # type: ignore
from .settings import (
    DEFAULT_DB_PATH,
    DEFAULT_SERIALIZER
)


class Bart:
    """
    "API" class for the app; all actions go through this class
    """

    def __init__(self, db_path: Path = DEFAULT_DB_PATH):
        self.db_path: Path = db_path
        self.db: TinyDB = TinyDB(self.db_path, storage=DEFAULT_SERIALIZER)
        self.project_table = self.db.table("project")
        self.docs_table = self.db.table("documents")

    def create_project(self, name, markup_language, numbering):
        project = Project(name, markup_language, numbering)
        self.project_table.insert(project.__dict__)

    def read_project(self):
        """
        Reads the project from the database
        """
        pass

    def add_document(self,
                     doc: Document,
                     manifest_index: Optional[int]):
        """
        Adds a document to the project, optionally inserts it into
        the project manifest at a specific point
        """
        pass

    def update_document(self, doc: Document):
        """
        Updates document information
        """
        pass

    def remove_document(self, doc_id):
        pass

    def combine_documents(self, docs: list[Document]):
        pass

    def add_notes_for_document(self):
        pass

    def update_manifest(self):
        pass
