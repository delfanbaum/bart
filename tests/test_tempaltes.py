import pytest
from bart.templates import write_template, named_document_template


@pytest.mark.parametrize("markup,heading_mark", [
        ("asciidoc", "= "),
        ("markdown", "# "),
        ("text", "")
    ])
def test_named_document_template(markup, heading_mark):
    """
    For each markup, it should prepend the title with the appropriate
    heading marker (or none)
    """
    assert named_document_template(markup, "My project") == f"{heading_mark}My project"


class TestWriteTemplate:
    """
    Tests the writing of various templates
    """

    def test_write_named_document_template(self, tmp_path):
        """
        We write a named_document_template
        """
        test_doc = tmp_path / "test.adoc"
        write_template(named_document_template,
                       test_doc,
                       markup="asciidoc",
                       document_name="Test")

        with test_doc.open('rt') as f:
            assert f.read() == """= Test"""
