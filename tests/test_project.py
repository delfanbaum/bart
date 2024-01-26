import pytest
from bart.config import MarkupLanguages
from bart.exceptions import MissingProjectRootException, NotInProjectException, ProjectDirExistsException
from bart.project import BartProject


class TestBartProject:
    """
    Tests around project-level functionality
    """

    def test_not_in_project(self):
        """
        If you're not in a project, raise an exception
        """

        with pytest.raises(NotInProjectException):
            BartProject()

    def test_init_missing_root(self, tmp_path):
        """
        Tests that we can find project files, but no root (unusual, but we need
        that root!)
        """
        project_file = tmp_path / '01-test.adoc'
        project_file.touch()

        with pytest.raises(MissingProjectRootException):
            BartProject(tmp_path)

    def test_begin(self, tmp_path):
        """
        You can start a new project given a path (made a Path by the cli) and a
        project name and that a "project root" is created
        """
        new_project = BartProject((tmp_path / "test"), new=True, project_name="Test")
        assert new_project
        assert "00-test.adoc" in [p.name for p in new_project.documents]
        assert new_project.root.name == "00-test.adoc"


    def test_begin_but_dir_exists(self, tmp_path):
        """
        You can start a new project given a path (made a Path by the cli) and a
        project name and that a "project root" is created
        """
        (tmp_path / "test").mkdir()

        with pytest.raises(ProjectDirExistsException):
            BartProject(tmp_path, new=True, project_name="Test")

    def test_project_defaults(self, test_project_adoc):
        """
        We read in a project with a (default by design) config
        """

        assert test_project_adoc.project_dir.stem == 'test'
        assert test_project_adoc.config.markup == MarkupLanguages.ASCIIDOC  # smoke default test
        assert test_project_adoc.documents
        assert test_project_adoc.root.name.split('-')[0] == "00"

    def test_get_docs(self, test_project_adoc):
        """
        The expected documents are in the test_project
        """

        assert len(test_project_adoc.documents) == 4


    def test_add_document(self, test_project_adoc):
        """
        We can add a document and it has the correct prefix
        """
        new_doc = test_project_adoc.add_document(name="test")
        # was created
        assert new_doc.is_file()
        # that it sorts last
        assert test_project_adoc.get_project_docs()[-1] == new_doc
        # has the correct prefix (we subtract 1 for the project root
        assert int(new_doc.name.split('-')[0]) == \
            len(test_project_adoc.get_project_docs()) - 1
