from pathlib import Path
from bart.project import BartProject


class TestBartProject:
    """
    Tests around project-level functionality
    """

    def test_init_no_project(self):
        """
        Smoke test
        """
        b = BartProject()
        assert b
        assert b.project_dir == Path.cwd()
        assert b.config.markup == "asciidoc"
        assert not b.documents
