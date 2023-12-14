from pathlib import Path
from tinydb import Query  # type: ignore
from bart.api import Bart


class TestBartApi:
    """
    Tests around API functionality via the Bart object
    """

    def test_initalization_new_project(self, tmp_path):
        """
        We create an API object and a database and insert a project if one
        isn't there already
        """
        db_path = tmp_path / "test.db.json"
        bart = Bart(db_path)
        bart.create_project("test-project", "text")
        Project = Query()
        assert db_path.is_file()
        assert bart.project_table.search(Project.name == "test-project")

    def test_initalization_existing_project(self):
        """
        If the database already exists, we can read it in
        """
        db_path = Path.cwd() / "tests/test_data/empty-project.json"
        bart = Bart(db_path)
        Project = Query()
        assert bart.project_table.search(Project.name == "test-project")

    def test_add_document_new_document_string(self, bart_with_project):
        """
        If the document doesn't exist, we add it, and add it to the manifest at
        the end
        """
        bart = bart_with_project
        file_path = str(bart.db_path.parent) + "file.txt"
        doc = bart.add_document(file_path)

        # runtime updates
        assert bart.project.manifest == [doc.id]

        # file updates
        assert Path(file_path).is_file()

        # database updates
        assert bart.project_table.get(doc_id=1)["manifest"] == [doc.id]
        assert len(bart.docs_table) == 1

    def test_add_document_new_document_path(self, bart_with_project):
        """
        If the document doesn't exist, we add it, and add it to the manifest at
        the end
        """
        bart = bart_with_project
        file_path = bart.db_path.parent / "file.txt"
        doc = bart.add_document(file_path)

        # runtime updates
        assert bart.project.manifest == [doc.id]

        # file updates
        assert Path(file_path).is_file()

        # database updates
        assert bart.project_table.get(doc_id=1)["manifest"] == [doc.id]
        assert len(bart.docs_table) == 1

    def test_add_document_existing_document(self, bart_with_project):
        """
        If the document does exist, we add its path to the project
        """
        bart = bart_with_project
        file = bart.db_path.parent / "test.txt"
        with file.open('wt') as f:
            f.write("Don't delete me!")
        bart.add_document(file)
        assert len(bart.docs_table) == 1

    def test_update_document(self):
        """
        We can update the fields on a document
        """
        pass

    def test_remove_document_delete_false(self):
        pass

    def test_remove_document_delete_true(self):
        pass
