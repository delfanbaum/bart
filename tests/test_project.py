import pytest
from bart.config import MarkupLanguages
from bart.exceptions import NotInProjectException
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

    
    def test_project_begin(self, tmp_path):
        """
        You can start a new project given a path (made a Path by the cli) and a
        project name and that a "project root" is created
        """
        new_project = BartProject(tmp_path, new=True, project_name="Test")
        assert new_project
        assert "00-test.adoc" in [p.name for p in new_project.documents]
        assert new_project.root.name == "00-test.adoc"


    def test_project_defaults(self, test_project_adoc):
        """
        We read in a project with a (default by design) config
        """
        b = BartProject(test_project_adoc)

        assert b.project_dir == test_project_adoc
        assert b.config.markup == MarkupLanguages.ASCIIDOC  # smoke default test
        assert b.documents
        assert b.root.name.split('-')[0] == "00"

    def test_project_get_docs(self, test_project_adoc):
        """
        The expected documents are in the test_project
        """
        b = BartProject(test_project_adoc)

        assert len(b.documents) == 4


