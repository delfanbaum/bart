import pytest
from bart.api import Bart


@pytest.fixture()
def bart_env_db(tmp_path_factory):
    """
    A test environment, yielding the db path
    """
    dir = tmp_path_factory.mktemp("tests")
    yield dir / ".bart.json"


@pytest.fixture()
def bart_with_project(tmp_path):
    """
    a Bart instance with a project already created
    """
    db_path = tmp_path / "test.db.json"
    bart = Bart(db_path)
    bart.create_project("test-project", "text")
    yield bart
