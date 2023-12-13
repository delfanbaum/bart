from datetime import datetime
from pathlib import Path
from freezegun import freeze_time
from bart.models import DEFAULT_DB_PATH, Document, Project


class TestProjectDefaults:
    """
    Tests for the Project class functionality, inc'l database actions.
    """

    @freeze_time("2023-12-13")
    def test_creation_and_field_access(self):
        """ smoke test """
        new_project = Project(
                name="My New Project",
                markup="text",
                number_documents=True
                )

        assert new_project
        assert new_project.title == "My New Project"
        assert new_project.markup == "text"
        assert new_project.db_path == DEFAULT_DB_PATH
        assert new_project.word_count_tracker["2023-12-13"] == 0
        assert new_project.number_documents


class TestProjectDocumentActions:
    """
    Tests for actions pertaining to documents
    """

    def test_add_document(self, fresh_project):
        """
        When a document is added, it should be put in the manifest, it should
        be added to the database, and it should be updated with its new
        database ID
        """
        doc = Document(text_path=Path("somefile.txt"))
        fresh_project.add_document(doc)
        assert doc.id  # we don't care what this is as long as it's there
        assert fresh_project.manifest == [doc]
        assert fresh_project.db
