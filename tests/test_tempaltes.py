import pytest
from bart.templates import project_root_template


@pytest.mark.parametrize("markup,heading_mark", [
        ("asciidoc", "= "),
        ("markdown", "# "),
        ("text", "")
    ])
def test_project_root_template(markup, heading_mark):
    """
    For each markup, it should prepend the title with the appropriate
    heading marker (or none)
    """
    assert project_root_template(markup, "My project") == f"{heading_mark}My project"
