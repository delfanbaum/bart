from pathlib import Path
import pytest


@pytest.fixture()
def test_adoc(tmp_path) -> Path:
    """
    Empty asciidoc file path for testing
    """
    test_dir = tmp_path / 'test'
    test_dir.mkdir()
    test_file = test_dir / 'test.adoc'
    test_file.touch()
    return test_file
