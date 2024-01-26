from pathlib import Path
from bart.config import BartConfig
import shutil
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

@pytest.fixture()
def test_project_adoc(tmp_path) -> Path:
    """
    Test project with various adoc files with a default config
    """
    test_dir = tmp_path / 'test'
    test_dir.mkdir()

    default_config = BartConfig(use_default=True)
    test_config = test_dir / '.bart.toml'
    default_config.write_to(test_config)

    shutil.copytree('tests/projects/adoc',
                    test_dir,
                    dirs_exist_ok=True)
    return test_dir

